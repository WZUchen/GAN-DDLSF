import argparse
import os

import joblib
import numpy as np
import torch.cuda

from torch.utils.data import DataLoader, TensorDataset
from torch import autograd, nn
from tqdm import tqdm
from model import *
import datetime

os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
torch.backends.cudnn.enabled = True
torch.backends.cudnn.benchmark = True

cuda = True if torch.cuda.is_available() else False
FloatTensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor
LongTensor = torch.cuda.LongTensor if cuda else torch.LongTensor


def weights_init(m):
    if isinstance(m, (nn.Linear, nn.Conv2d, nn.ConvTranspose2d)):
        nn.init.xavier_uniform_(m.weight)
        if m.bias is not None:
            nn.init.constant_(m.bias, 0.0)


def count_element(label):
    n_x = (label == 1).sum(dim=1)
    return n_x


def noising(imgs):
    imgs = imgs.numpy()
    B = imgs.shape[0]
    mask = (imgs < 0.01)
    a = np.random.normal(10 ** -3, 10 ** -2.5, (B, 1, 42, 3))
    noise = mask * abs(a)
    imgs_after_noising = imgs + noise
    imgs_after_noising = torch.tensor(imgs_after_noising)
    return imgs_after_noising


def get_onehot(x, num_class_ga, num_class_n):
    m = x.shape[0]
    output = []
    output2 = []
    for i in range(m):
        x_i = x[i]
        temp = np.zeros((num_class_ga,))
        temp2 = np.zeros((num_class_n,))
        temp[x_i[0] - 1] = 1
        temp2[x_i[1] - 1] = 1
        output.append(temp)
        output2.append(temp2)
    output = np.array(output)
    output2 = np.array(output2)
    return output, output2


def to_categorical(y, num_columns):
    """Returns one-hot encoded Tensor"""
    y_cat = torch.zeros((y.shape[0], num_columns))
    y_cat[range(y.shape[0]), y] = 1.0
    return y_cat


def make_fake_label_ga_n(fake_c_ga_int, fake_c_n_int):
    batch_size = fake_c_ga_int.shape[0]
    ga_label_fake = []
    n_label_fake = []
    for i in range(batch_size):
        n_ga = fake_c_ga_int[i] + 1
        n_n = fake_c_n_int[i] + 1
        ga_label_fake_i = np.array([1] * (n_ga) + [0] * (20 - n_ga))
        n_label_fake_i = np.array([1] * (n_n) + [0] * (20 - n_n))
        np.random.shuffle(ga_label_fake_i)
        np.random.shuffle(n_label_fake_i)
        ga_label_fake.append(ga_label_fake_i.reshape(1, 20, 1))
        n_label_fake.append(n_label_fake_i.reshape(1, 20, 1))
    return np.vstack(ga_label_fake), np.vstack(n_label_fake)

def calc_gradient_penalty(netD, real_data, fake_data):
    batch_size = real_data.size(0)
    alpha = torch.rand(batch_size, 1)
    alpha = alpha.expand(batch_size, int(real_data.nelement() / batch_size)).contiguous().view(batch_size, 1, 42, 3)
    alpha = alpha.cuda() if cuda else alpha
    interpolates = alpha * real_data + ((1 - alpha) * fake_data)
    if cuda:
        interpolates = interpolates.cuda()
    interpolates = autograd.Variable(interpolates, requires_grad=True)
    feature, disc_interpolates = netD(interpolates)
    gradients = autograd.grad(outputs=disc_interpolates, inputs=interpolates,
                              grad_outputs=torch.ones(disc_interpolates.size()).cuda() if cuda else torch.ones(
                                  disc_interpolates.size()),
                              create_graph=True, retain_graph=True, only_inputs=True)[0]
    gradients = gradients.view(gradients.size(0), -1)
    gradient_penalty = ((gradients.norm(2, dim=1) - 1) ** 2).mean() * 10
    return gradient_penalty


def adjust_learning_rate(optimizer, epoch, initial_lr):
    lr = initial_lr * (0.95 ** (epoch // 10))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="GaN-GEN")
    parser.add_argument('--n_epochs', type=int, default=501, help='number of epochs of training')
    parser.add_argument('--batch_size', type=int, default=32, help='size of the batches')
    parser.add_argument('--d_lr', type=float, default=0.00005, help='adam: learning rate')
    parser.add_argument('--q_lr', type=float, default=0.000025)
    parser.add_argument('--g_lr', type=float, default=0.00005)
    parser.add_argument('--b1', type=float, default=0.5, help='adam: decay of first order momentum of gradient')
    parser.add_argument('--b2', type=float, default=0.999, help='adam: decay of first order momentum of gradient')
    parser.add_argument('--latent_dim', type=int, default=105, help='dimensionality of the latent space')
    parser.add_argument('--model_save_dir', type=str, default='../data/keypoints/model_cwgan_GaN/')
    parser.add_argument('--load_model', type=bool, default=False)
    parser.add_argument('--load_generator', type=str)
    parser.add_argument('--load_discriminator', type=str)
    parser.add_argument('--load_q', type=str)
    parser.add_argument('--constraint_epoch', type=int, default=10000)
    parser.add_argument('--gen_dir', type=str, default='../data/keypoints/gen_image_cwgan_GaN/')
    parser.add_argument('--log_dir',type=str,default='../data/log/')
    parser.add_argument('--training_data', type=str, default='../data/preprocess_data/Training_Data/Labeled/unique_GaN_v1.pickle')
    parser.add_argument('--input_dim', type=str, default=64 + 20 + 20 + 1)
    opt = parser.parse_args()

    job_name = os.path.basename(os.path.normpath(opt.model_save_dir))
    log_filename = 'train_log_' + job_name + '.txt'
    print(job_name,log_filename)
    print(opt)

    current_date = datetime.datetime.now().strftime("%Y%m%d")

    date_specific_save_dir = os.path.join(opt.model_save_dir, current_date)
    if not os.path.exists(date_specific_save_dir):
        os.makedirs(date_specific_save_dir)

    date_specific_gen_dir = os.path.join(opt.gen_dir, current_date)
    if not os.path.exists(date_specific_gen_dir):
        os.makedirs(date_specific_gen_dir)

    log_specific_dir = os.path.join(opt.log_dir, current_date)
    if not os.path.exists(log_specific_dir):
        os.makedirs(log_specific_dir)

    adversarial_loss = torch.nn.MSELoss()
    categorical_loss = torch.nn.CrossEntropyLoss()
    continuous_loss = torch.nn.MSELoss()

    generator = Generator(opt)
    discriminator = Discriminator()
    net_Q = QHead_GaN()

    if cuda:
        generator.cuda()
        discriminator.cuda()
        net_Q.cuda()
        adversarial_loss.cuda()
        categorical_loss.cuda()
        continuous_loss.cuda()

    train_data = np.load(opt.training_data, allow_pickle=True)
    dataloader = torch.utils.data.DataLoader(train_data, batch_size=opt.batch_size, shuffle=True)

    optimizer_G = torch.optim.Adam(generator.parameters(), lr=opt.g_lr, betas=(opt.b1, opt.b2))
    optimizer_D = torch.optim.Adam(discriminator.parameters(), lr=opt.d_lr, betas=(opt.b1, opt.b2))
    optimizer_Q = torch.optim.Adam(net_Q.parameters(), lr=opt.q_lr, betas=(opt.b1, opt.b2))

    if opt.load_model:
        generator.load_state_dict(torch.load(opt.load_generator))
        discriminator.load_state_dict(torch.load(opt.load_discriminator))
        net_Q.load_state_dict(torch.load(opt.load_q))
        print("load model ! ", opt.load_generator, opt.load_discriminator, opt.load_q)
    else:
        generator.apply(weights_init)
        print("generator weights are initialized")
        discriminator.apply(weights_init)
        print("discriminator weights are initialized")
        net_Q.apply(weights_init)
        print("net Q  weights are initialized")

    one = torch.FloatTensor([1])
    mone = one * -1

    if cuda:
        one = one.cuda()
        mone = mone.cuda()

    for epoch in range(opt.n_epochs):
        r_ga = []
        r_n = []

        f_ga = []
        f_n = []

        w = []
        for j, (imgs, label) in enumerate(tqdm(dataloader)):
            batch_size = imgs.shape[0]
            real_img = imgs.view(batch_size, 1, 42, 3)
            real_img_noise = noising(real_img)
            ga_label, n_label = label[:, :20, :], label[:, 20:, :]

            n_ga = count_element(ga_label).reshape(batch_size, ) - 1
            n_n = count_element(n_label).reshape(batch_size, ) - 1
            natoms = n_ga + n_n + 2

            real_imgs = real_img.type(FloatTensor)
            real_imgs_noise = real_img_noise.type(FloatTensor)
            real_labels_n, real_labels_ga = n_n.type(LongTensor), n_ga.type(LongTensor)
            ga_label, n_label = ga_label.type(LongTensor), n_label.type(LongTensor)
            cell_label = (natoms.type(FloatTensor) / 40.0).unsqueeze(-1)

            valid = FloatTensor(np.random.uniform(0.8, 1.0, size=(batch_size, 1)))
            fake = FloatTensor(np.random.uniform(0, 0.2, size=(batch_size, 1)))

            for p in discriminator.parameters():
                p.requires_grad = True

            discriminator.zero_grad()
            net_Q.zero_grad()
            optimizer_D.zero_grad()
            optimizer_Q.zero_grad()

            if cuda:
                real_imgs = real_imgs.cuda()
                real_imgs_noise = real_imgs_noise.cuda()
                real_labels_ga = real_labels_ga.cuda()
                real_labels_n = real_labels_n.cuda()
                ga_label = ga_label.cuda()
                n_label = n_label.cuda()
                cell_label = cell_label.cuda()

            real_feature, D_real = discriminator(real_imgs)
            real_ga_label, real_n_label, real_ga_cat, real_n_cat, cell_pred = net_Q(real_imgs_noise)
            D_real = D_real.mean()

            pca = joblib.load('../ipynb/pca_model.pkl')
            new_batch = imgs
            new_batch_reshaped = new_batch.reshape(batch_size, 42 * 3)
            new_batch_reduced = pca.transform(new_batch_reshaped)
            mean_reduced = np.mean(new_batch_reduced, axis=0)
            std_dev_reduced = np.std(new_batch_reduced, axis=0)
            z_pca = np.random.normal(mean_reduced, std_dev_reduced, (batch_size, opt.latent_dim))
            z_normal = np.random.normal(0, 1, (batch_size, opt.latent_dim))
            z_new = 0.2 * z_pca + 0.8 * z_normal


            if cuda:
                z = z.cuda()

            fake_c_ga_int = np.random.randint(0, 20, batch_size)
            fake_c_ga = to_categorical(fake_c_ga_int, num_columns=20)
            fake_c_n_int = np.random.randint(0, 20, batch_size)
            fake_c_n = to_categorical(fake_c_n_int, num_columns=20)
            ga_label_fake, n_label_fake = make_fake_label_ga_n(fake_c_ga_int, fake_c_n_int)

            natoms_fake = fake_c_ga_int + fake_c_n_int + 2
            natoms_fake = (FloatTensor(natoms_fake) / 40.0).unsqueeze(-1)

            if cuda:
                fake_c_ga_int = torch.tensor(fake_c_ga_int).cuda().type(LongTensor)
                fake_c_ga = fake_c_ga.cuda()
                ga_label_fake = torch.tensor(ga_label_fake).type(LongTensor).cuda()
                fake_c_n_int = torch.tensor(fake_c_n_int).cuda().type(LongTensor)
                fake_c_n = fake_c_n.cuda()
                n_label_fake = torch.tensor(n_label_fake).type(LongTensor).cuda()
                natoms_fake = natoms_fake.cuda()

            fake = generator(z, fake_c_ga, fake_c_n, natoms_fake)
            fake_feature, D_fake = discriminator(fake)

            cat_loss_ga_real = categorical_loss(real_ga_label, ga_label)
            cat_loss_n_real = categorical_loss(real_n_label, n_label)

            cat_loss_ga_real2 = categorical_loss(real_ga_cat, real_labels_ga)
            cat_loss_n_real2 = categorical_loss(real_n_cat, real_labels_n)

            cat_loss_real = (cat_loss_ga_real + cat_loss_n_real) + 0.3 * (cat_loss_ga_real2 + cat_loss_n_real2)

            r_ga.append(cat_loss_ga_real2.item())
            r_n.append(cat_loss_n_real2.item())

            D_real_cat = D_real - cat_loss_real
            D_real_cat = D_real_cat.mean().unsqueeze(0)
            D_real_cat.backward(mone)

            D_fake = D_fake.mean().unsqueeze(0)
            D_fake.backward(one)

            gradient_penalty = calc_gradient_penalty(discriminator, real_imgs, fake)
            gradient_penalty.backward()

            D_cost = D_fake - D_real + gradient_penalty
            Wasserstein_D = D_real - D_fake

            w.append(Wasserstein_D.item())

            optimizer_D.step()
            optimizer_Q.step()

            if j % 2 == 0:
                for p in discriminator.parameters():
                    p.requires_grad = False

                generator.zero_grad()
                net_Q.zero_grad()
                optimizer_G.zero_grad()
                optimizer_Q.zero_grad()

                z = FloatTensor(np.random.normal(0, 1, (batch_size, opt.latent_dim)))

                fake = generator(z, fake_c_ga, fake_c_n, natoms_fake)
                fake_feature, G = discriminator(fake)
                fake_ga_label, fake_n_label, fake_ga_cat, fake_n_cat, fake_cell_pred = net_Q(fake)

                cat_loss_ga_fake = categorical_loss(fake_ga_label, ga_label_fake)
                cat_loss_n_fake = categorical_loss(fake_n_label, n_label_fake)

                cat_loss_ga_fake2 = categorical_loss(fake_ga_cat, fake_c_ga_int)
                cat_loss_n_fake2 = categorical_loss(fake_n_cat, fake_c_n_int)

                f_ga.append(cat_loss_ga_fake2.item())
                f_n.append(cat_loss_n_fake2.item())

                G = G.mean()

                cat_loss_fake = 0 * (cat_loss_ga_fake + cat_loss_n_fake) + 0.3 * (
                        cat_loss_ga_fake2 + cat_loss_n_fake2)
                cat_loss = cat_loss_fake

                G_cat = G - cat_loss
                G_cat = G_cat.unsqueeze(0)
                G_cat.backward(mone)
                G_cost = -G
                optimizer_Q.step()
                optimizer_G.step()

            if j == 0:
                gen_images = fake
            else:
                gen_images = torch.cat((gen_images, fake), dim=0)
                batches_done = epoch * len(dataloader) + j

        if epoch % 50 == 0:
            torch.save(generator.state_dict(), os.path.join(date_specific_save_dir, 'generator_' + str(epoch)))
            torch.save(discriminator.state_dict(), os.path.join(date_specific_save_dir, 'discriminator_' + str(epoch)))
            torch.save(net_Q.state_dict(), os.path.join(date_specific_save_dir, 'Q_' + str(epoch)))

        log_string = f"[Epoch {epoch}/{opt.n_epochs}] [W loss: {sum(w) / len(w)}] "
        log_string += f"[real Ga : {sum(r_ga) / len(r_ga)}] [real N : {sum(r_n) / len(r_n)}] [fake Ga : {sum(f_ga) / len(f_ga)}] [fake N : {sum(f_n) / len(f_n)}]"
        print(log_string)

        if epoch == 0:
            with open(os.path.join(log_specific_dir, log_filename), 'a') as f:
                f.write(log_string + '\n')
        else:
            with open(os.path.join(log_specific_dir, log_filename), 'a') as f:
                f.write(log_string + '\n')

        if epoch % 5 == 0:
            gen_name = os.path.join(date_specific_gen_dir, f'gen_images_{epoch}.npy')
            tt = gen_images.cpu().detach().numpy()
            np.save(gen_name, tt)

        adjust_learning_rate(optimizer_D, epoch + 1, opt.d_lr)
        adjust_learning_rate(optimizer_G, epoch + 1, opt.g_lr)
        adjust_learning_rate(optimizer_Q, epoch + 1, opt.q_lr)