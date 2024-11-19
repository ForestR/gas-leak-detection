# Micro Leak Detection of Natural Gas for Residential Users Based on Gas Flowmeters

This repository contains the code and data for our paper accepted at The 12th International Conference on Information Technology: IoT and Smart City (ICIT 2024), to be held at University of Malaya, Kuala Lumpur, Malaysia.

## Abstract
This paper presents a novel approach to detecting small residential gas leaks by developing and testing a leakage detection algorithm, termed the Weeg algorithm. Using real-world data from household gas meters and simulating both normal and leak conditions, we benchmarked the Weeg algorithm against traditional detection methods. The evaluation was performed on a dataset containing 86 leakage samples and 1103 non-leakage samples. The Weeg algorithm demonstrated significant improvements, achieving an accuracy of 90.2\% and an F1 score of 0.458, while reducing false positive rates compared to conventional algorithms.

## Repository Structure
- `data/`: Contains all data files
  - `raw/`: Raw data from flowmeters
  - `processed/`: Cleaned and processed data
  - `results/`: Analysis results and outputs
- `src/`: Source code
  - `data_processing/`: Scripts for data preprocessing
  - `models/`: Detection algorithms and models
  - `visualization/`: Plotting and visualization code
- `notebooks/`: Jupyter notebooks for analysis
- `docs/`: Documentation and paper materials
  - `figures/`: Publication-ready figures

## Installation
```bash
pip install -r requirements.txt
```

## Usage
[Instructions on how to run your code]

## Publication
This paper will be published in the ACM Conference Proceedings (ISBN: 979-8-4007-1737-6) and will be indexed by EI Compendex and Scopus.

## Citation
```bibtex
@inproceedings{yin2024micro,
  title={Micro Leak Detection of Natural Gas for Residential Users Based on Gas Flowmeters},
  author={Yin, Da and Ni, Weiping and Shu, Fangcun},
  booktitle={Proceedings of the 12th International Conference on Information Technology: IoT and Smart City},
  pages={},
  year={2024},
  isbn={979-8-4007-1737-6},
  publisher={Association for Computing Machinery},
  address={Kuala Lumpur, Malaysia}
}
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any inquiries about the code or paper, please contact:
- Da Yin (dyin1900@gmail.com)

## Conference Information
- **Conference**: ICIT 2024 - The 12th International Conference on Information Technology: IoT and Smart City
- **Date**: December 13-15, 2024
- **Venue**: University of Malaya, Kuala Lumpur, Malaysia
- **Website**: http://www.icit.org/