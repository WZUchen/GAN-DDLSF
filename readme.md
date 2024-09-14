# GAN-DDLSF: Advancing Materials Discovery with AI 🚀

![GitHub](https://img.shields.io/github/license/WZUchen/GAN-DDLSF)
![GitHub last commit](https://img.shields.io/github/last-commit/WZUchen/GAN-DDLSF)
![GitHub issues](https://img.shields.io/github/issues/WZUchen/GAN-DDLSF)
![GitHub stars](https://img.shields.io/github/stars/WZUchen/GAN-DDLSF?style=social)

## Abstract

GAN-DDLSF introduces a groundbreaking approach in the realm of generative adversarial networks (GANs), specifically tailored for materials science applications. By integrating a novel data-driven latent space fusion (DDLSF) method, our model optimizes the latent space through a unique blend of real data statistical properties and standard Gaussian distributions. This innovative technique effectively addresses the persistent challenges of high-dimensional data complexity and mode collapse in GANs, significantly enhancing prediction accuracy in materials science.

Our primary focus is on predicting binary crystal structures of Gallium Nitride (GaN), a critical material in advanced electronics and optoelectronics. GAN-DDLSF has successfully generated 9,321 GaN binary crystal structures, achieving remarkable stability and metastability rates. This breakthrough not only demonstrates the model's efficacy but also opens new avenues for materials discovery and design.

## Key Features 🔑

- **Data-Driven Latent Space Optimization**: Our unique DDLSF method combines real data attributes with Gaussian distributions, effectively mitigating GAN mode collapse. 🔍
- **Cutting-edge Materials Science Application**: Specifically targets the prediction of binary crystal structures for Gallium Nitride (GaN), pushing the boundaries of material informatics. 🧬
- **Unprecedented Prediction Accuracy**: Generates a vast array of stable and metastable crystal structures, significantly enhancing the accuracy and reliability of crystal predictions. 🎯
- **Scalable Architecture**: Designed to be adaptable for various materials and crystal structures beyond GaN. 🔧
- **Interpretable Results**: Provides insights into the generated structures, facilitating better understanding of material properties. 📊

## Repository Contents 📁

We are excited to announce that our GAN-DDLSF code and data are now available! Our repository includes:

- **Source Code**: Fully documented and ready for community use and contributions.
- **Training Datasets**: Carefully curated datasets to help you train the model efficiently.
- **Generated Datasets**: Explore the diverse crystal structures produced by our model.
- **Documentation**: Step-by-step guides for setup, training, and result interpretation.
- **Jupyter Notebooks**: Interactive examples demonstrating key functionalities and use cases.

## Installation

To get started, follow these steps to install the necessary dependencies and set up the environment:

```bash
git clone https://github.com/WZUchen/GAN-DDLSF.git
cd GAN-DDLSF
pip install -r requirements.txt
```

## Data Preprocessing 🧹

Before training the model, it is essential to preprocess the data. We have provided scripts that handle data normalization, cleaning, and preparation. Execute the scripts in the `data_processing` folder in order:

```bash
cd data_processing
```

This ensures that the dataset is in the proper format and ready for training.

## Training the Model 🚀

Once the data is processed, you can start training the GAN-DDLSF model using the `Trainer/train.py` script. This script is designed to train the GAN model on the preprocessed data and optimize the latent space fusion process.

```bash
cd ../Trainer
python train.py
```

The training process includes:

- **Model Initialization**: Initializing the GAN-DDLSF architecture with predefined hyperparameters.
- **Latent Space Fusion**: Applying the DDLSF method to balance real data distribution and Gaussian noise.
- **Checkpointing**: Saving intermediate results for future use.

## Post-processing 📈

After training is complete, you can generate and analyze the predicted crystal structures using the post-processing scripts in the `postprocess_data` directory. This step helps you evaluate the quality and properties of the generated structures.

```bash
cd ../postprocess_data
```

Post-processing includes:

- **Structure Analysis**: Evaluating the stability and metastability of the predicted crystal structures.
- **Visualization**: Visualizing the generated structures for better interpretation of results.
  
## Quick Start Guide

### Example Workflow:

1. **Clone the Repository**: `git clone https://github.com/WZUchen/GAN-DDLSF.git`
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Preprocess Data**: Run the scripts in `data_processing` folder.
4. **Train the Model**: `python Trainer/train.py`
5. **Post-process Results**: Analyze and visualize with scripts in `postprocess_data`.

For detailed instructions, please refer to our [documentation](docs/README.md).

## Contributing

We welcome contributions to enhance GAN-DDLSF! Here's how you can get involved:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss what you would like to change.


## Acknowledgments

This project was fully developed independently by Chen Zi'an. Special thanks to all contributors who have helped shape this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact

Chen Zi'an - wzucza@gmail.com

Project Link: [https://github.com/WZUchen/GAN-DDLSF](https://github.com/WZUchen/GAN-DDLSF)
