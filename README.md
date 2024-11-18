# Micro Leak Detection of Natural Gas for Residential Users Based on Gas Flowmeters

This repository contains the code and data for the paper "Micro Leak Detection of Natural Gas for Residential Users Based on Gas Flowmeters" accepted at IEEE ICIT 2024.

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

## Installation
```bash
pip install -r requirements.txt
```

## Usage
[Instructions on how to run your code]

## Citation
```bibtex
@inproceedings{yin2024micro,
  title={Micro Leak Detection of Natural Gas for Residential Users based on Gas Flowmeters},
  author={Yin, Da and Ni, Weiping and Shu, Fangcun},
  booktitle={2024 The 12th International Conference on Information Technology: IoT and Smart City (ICIT)},
  year={2024},
  organization={ACM}
}
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
- Da Yin
- Weiping Ni
- Fangcun Shu