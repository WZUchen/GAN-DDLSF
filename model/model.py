import torch.nn as nn
import torch

class Generator(nn.Module):
    def __init__(self, opt):
        super(Generator, self).__init__()
        input_dim = opt.latent_dim + 20 + 20 + 1  # 20 for Ga, 20 for N
        self.input_dim = opt.input_dim  # Update this as needed

        self.l1 = nn.Sequential(nn.Linear(input_dim, 128 * 40), nn.ReLU(True))  # 40 = 20(Ga) + 20(N)
        self.map1 = nn.Sequential(nn.ConvTranspose2d(128, 256, (1, 3), stride=1, padding=0), nn.BatchNorm2d(256, 0.8),
                                  nn.ReLU(True))
        self.map2 = nn.Sequential(nn.ConvTranspose2d(256, 512, (1, 1), stride=1, padding=0), nn.BatchNorm2d(512, 0.8),
                                  nn.ReLU(True))
        self.map3 = nn.Sequential(nn.ConvTranspose2d(512, 256, (1, 1), stride=1, padding=0), nn.BatchNorm2d(256, 0.8),
                                  nn.ReLU(True))
        self.map4 = nn.Sequential(nn.ConvTranspose2d(256, 1, (1, 1), stride=1, padding=0))

        self.cellmap = nn.Sequential(nn.Linear(120, 42), nn.BatchNorm1d(42), nn.ReLU(True), nn.Linear(42, 6),
                                     nn.Sigmoid())  # 105 = 35 * 3

        self.sigmoid = nn.Sigmoid()

    def forward(self, noise, c1, c2, c4):
        gen_input = torch.cat((noise, c4, c1, c2), -1)  # Concatenating Ga and N labels
        # print(gen_input.shape)
        h = self.l1(gen_input)
        h = h.view(h.shape[0], 128, 40, 1)  # 40 = 20(Ga) + 20(N)
        h = self.map1(h)
        h = self.map2(h)
        h = self.map3(h)
        h = self.map4(h)

        h_flatten = h.view(h.shape[0], -1)
        pos = self.sigmoid(h)
        # print(h_flatten.shape)
        cell = self.cellmap(h_flatten)
        cell = cell.view(cell.shape[0], 1, 2, 3)
        return torch.cat((cell, pos), dim=2)


class Discriminator(nn.Module):  # 定义一个判别器类，继承自 nn.Module
    def __init__(self):
        super(Discriminator, self).__init__()  # 调用父类的构造函数

        self.model = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=512, kernel_size=(1, 3), stride=1, padding=0),
            nn.LeakyReLU(0.2, inplace=True),  # 第一个卷积层，后接LeakyReLU激活函数
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(1, 1), stride=1, padding=0),
            nn.LeakyReLU(0.2, inplace=True),  # 第二个卷积层，后接LeakyReLU激活函数
            nn.Conv2d(in_channels=512, out_channels=256, kernel_size=(1, 1), stride=1, padding=0),
            nn.LeakyReLU(0.2, inplace=True)  # 第三个卷积层，后接LeakyReLU激活函数
        )

        # 调整平均池化层以匹配 Ga 和 N 元素的数量
        self.avgpool_ga = nn.AvgPool2d(kernel_size=(20, 1))  # Ga元素的平均池化层
        self.avgpool_n = nn.AvgPool2d(kernel_size=(20, 1))  # N元素的平均池化层

        # 根据新维度调整第一个线性层的输入大小
        self.feature_layer = nn.Sequential(
            nn.Linear(1024, 1000),  # 调整输入大小
            nn.LeakyReLU(0.2, inplace=True),  # 线性层后接LeakyReLU激活函数
            nn.Linear(1000, 200),  # 另一个线性层
            nn.LeakyReLU(0.2, inplace=True)  # 再次使用LeakyReLU激活函数
        )
        self.output = nn.Sequential(nn.Linear(200, 10))  # 输出层

    def forward(self, x):
        B = x.shape[0]  # 获取批次大小
        output = self.model(x)

        # 调整切片以匹配新结构：2用于 'cell'，20用于Ga，20用于N
        output_c = output[:, :, :2, :]  # 切割 cell 部分
        output_ga = output[:, :, 2:22, :]  # 切割 Ga 部分
        output_n = output[:, :, 22:, :]  # 切割 N 部分

        # 使用更新后的平均池化层
        output_ga = self.avgpool_ga(output_ga)  # 对 Ga 部分应用平均池化
        output_n = self.avgpool_n(output_n)  # 对 N 部分应用平均池化

        output_all = torch.cat((output_c, output_ga, output_n), dim=-2)  # 将所有部分拼接
        output_all = output_all.view(B, -1)  # 调整形状
        feature = self.feature_layer(output_all)  # 通过特征层
        return feature, self.output(feature)  # 返回特征和输出


class QHead_BiSe(nn.Module):
    def __init__(self):
        super(QHead_BiSe, self).__init__()

        self.model_Bi = nn.Sequential(
            nn.Conv2d(1, 512, (1, 3), 1, 0),
            nn.BatchNorm2d(512, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(512, 256, (1, 1), 1, 0),
            nn.BatchNorm2d(256, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(256, 256, (1, 1), 1, 0),
            nn.BatchNorm2d(256, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(256, 2, (1, 1), 1, 0)
        )

        self.model_Se = nn.Sequential(
            nn.Conv2d(1, 512, (1, 3), 1, 0),
            nn.BatchNorm2d(512, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(512, 256, (1, 1), 1, 0),
            nn.BatchNorm2d(256, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(256, 256, (1, 1), 1, 0),
            nn.BatchNorm2d(256, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(256, 2, (1, 1), 1, 0)
        )

        self.model_cell = nn.Sequential(
            nn.Conv2d(1, 64, (1, 3), 1, 0),
            nn.BatchNorm2d(64, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, 64, (1, 1), 1, 0),
            nn.BatchNorm2d(64, 0.8),
            nn.LeakyReLU(0.2, inplace=True)
        )

        self.softmax = nn.Softmax2d()

        self.label_Bi_layer = nn.Sequential(
            nn.Linear(40, 300),
            nn.BatchNorm1d(300, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(300, 100),
            nn.BatchNorm1d(100, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(100, 20),
            nn.Softmax(dim=1)
        )

        self.label_Se_layer = nn.Sequential(
            nn.Linear(40, 300),
            nn.BatchNorm1d(300, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(300, 100),
            nn.BatchNorm1d(100, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(100, 20),
            nn.Softmax(dim=1)
        )

        self.label_c_layer = nn.Sequential(
            nn.Linear(128, 100),
            nn.BatchNorm1d(100, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(100, 50),
            nn.BatchNorm1d(50, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(50, 1),
            nn.Sigmoid()
        )

    def forward(self, image):
        cell = image[:, :, :2, :]
        Bi = image[:, :, 2:22, :]
        Se = image[:, :, 22:, :]

        cell_output = self.model_cell(cell)
        Bi_output = self.model_Bi(Bi)
        Se_output = self.model_Se(Se)

        cell_output_f = torch.flatten(cell_output, start_dim=1)
        Bi_output_f = torch.flatten(Bi_output, start_dim=1)
        Se_output_f = torch.flatten(Se_output, start_dim=1)

        Bi_output_sm = self.softmax(Bi_output)
        Se_output_sm = self.softmax(Se_output)

        cell_label = self.label_c_layer(cell_output_f)
        Bi_cat = self.label_Bi_layer(Bi_output_f)
        Se_cat = self.label_Se_layer(Se_output_f)

        return Bi_output_sm, Se_output_sm, Bi_cat, Se_cat, cell_label
