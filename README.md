# 📘 Realsee3D Dataset

![Dataset Overview](assets/dataset_overview.png)

[![Website](https://img.shields.io/badge/Website-visit-blue)](https://realsee-developer.github.io/RealSee3D/)
[![Download](https://img.shields.io/badge/Download-now-green)](https://realsee-developer.github.io/RealSee3D/#download)

Realsee3D is a large-scale, multi-view RGB-D dataset containing 10,000 indoor scenes, comprising real-world residential scenes captured by 3D LiDAR Camera and procedurally generated scenes.

## ✨ Features

*   **Large Scale:** 10,000 unique indoor scenes, comprising 95,962 rooms and 299,073 viewpoints/RGB-D pairs.
*   **Rich Data:** Panoramic RGB-D captures with complete room-level coverage.
*   **Comprehensive Annotations:** Includes CAD drawings, floor plans, semantic segmentation, 3D detection labels and more (forthcoming).
*   **Diverse Scenes:** Comprising 1,000 real-world scenes with varied layouts and decoration styles, and 9,000 procedurally generated scenes utilizing over 100 designer-curated style templates, ensuring diverse furniture models and styles for robust training and testing.

## 🗃️ Data Organization & Access

The Realsee3D dataset is organized into individual scenes, each containing detailed multi-view RGB-D data.

*   **Data Structure & Usage:** [DATASET_STRUCTURE.md](DATASET_STRUCTURE.md) provides a comprehensive explanation of the file organization, data formats, and detailed usage instructions.
*   **Methodology:** Visit our [official website](https://realsee-developer.github.io/RealSee3D) for more detailed information on how real-world data is collected and how synthetic data is generated.

### 📥 How to Download

To access the dataset, you must sign a Data Usage Agreement (PDF format). You can download the agreement directly [here](docs/Realsee3D_Dataset_agreement.pdf).
Please send your request, specifying your intended use, to **developer@realsee.com**. Once your application is approved and you have signed the agreement, we will reply with download instructions and links.


## 📊 Statistics

For a detailed breakdown of dataset statistics, please refer to [metadata/README.md](metadata/README.md).

## 📋 Changelog

*   **2025-11-28:** Dataset introduction and official website release.

## 📄 Citation

If you use the Realsee3D dataset in your research, please cite our paper:

```
@inproceedings{realsee3d,
  title={Realsee3D: A Large-Scale Multi-View RGB-D Dataset of Indoor Scenes},
  author={Linyuan Li, Cihui Pan, Tong Rao, Jie Zhou, Yan Wu, Xi Li, Lingli Wang et al.},
  booktitle={},
  year={2026}
}
```

## 📝 License

### Dataset License

The Realsee3D dataset is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

### Code License

The accompanying code for data parsing, visualization, and evaluation is released under the [MIT License](https://opensource.org/licenses/MIT), allowing for free use, modification, and distribution.

