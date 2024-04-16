# GAN-DDLSF

## Abstract
In this project, we introduce a novel generative adversarial network (GAN) model, named GAN-DDLSF, which integrates a data-driven latent space fusion (DDLSF) method. This method optimizes the latent space by blending the statistical properties of real data with a standard Gaussian distribution. Our approach addresses the challenges of high-dimensional data complexity and mode collapse in GANs, enhancing prediction accuracy in materials science. Specifically, GAN-DDLSF is applied to predict binary crystal structures of Gallium Nitride (GaN), a key material for advanced electronics and optoelectronics. The model successfully generates 9,321 GaN binary crystal structures, achieving significant stability and metastability rates, thereby advancing the potential for new materials discovery and design.

## Key Features
- **Data-Driven Latent Space Optimization**: Combines real data attributes with Gaussian distributions to mitigate GAN mode collapse.
- **Material Science Application**: Targets the prediction of binary crystal structures for Gallium Nitride (GaN).
- **High Prediction Accuracy**: Generates numerous stable and metastable crystal structures, enhancing the accuracy of crystal predictions.

## Installation
```bash
git clone https://github.com/yourusername/GAN-DDLSF.git
cd GAN-DDLSF
pip install -r requirements.txt
