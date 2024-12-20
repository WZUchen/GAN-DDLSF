# GAN-DDLSF

![GitHub](https://img.shields.io/github/license/yourusername/GAN-DDLSF)
![GitHub stars](https://img.shields.io/github/stars/yourusername/GAN-DDLSF?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/GAN-DDLSF?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/GAN-DDLSF)
![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/GAN-DDLSF)

## Database Components

### Basic Materials Project Database
- Contains binary compound structures from MP Dataset (`binary_compound_Database`)
- Serves as the foundational dataset for subsequent analysis and model training

### Filtered Compound Database
- Refined subset with specific constraints:
  - Unit cells containing fewer than 10 atoms
  - Total atomic count under 20
- Database identifier: `filtered_compound_Database_cell_under10_atoms_under20`

### Generated Structure Database
- Collection of computationally predicted structures
- Includes both stable and metastable configurations
- Located in: `generate_screening_cif_crystal_structure`

## Methodology

The project follows a systematic approach to structure prediction:
1. Initial data collection from Materials Project
2. Application of physical constraints and filtering criteria
3. Structure generation and stability analysis
4. Validation and verification of predicted structures

## Development Plan

### Current Progress

- ✅ Data Upload Completed

  - Basic MP binary compound structures

  - Filtered compound database

  - Generated stable and metastable structures

### Future Plans

- 🔄 In Progress

  - Data processing scripts organization and documentation

  - Processing workflow documentation refinement

- 📅 Planned Releases

  - Structure screening scripts

  - Data preprocessing utilities

  - Structure generation and validation scripts

  - Complete operation examples and usage instructions

