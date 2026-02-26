# 📘 Realsee3D Dataset

![Dataset Overview](assets/dataset_overview.png)

[![Website](https://img.shields.io/badge/Website-visit-blue)](https://dataset.realsee.ai/)
[![Download](https://img.shields.io/badge/Download-now-green)](https://https://dataset.realsee.ai/#download)

Realsee3D is a large-scale, multi-view RGB-D dataset containing 10,000 indoor scenes, comprising real-world residential scenes captured by 3D LiDAR Camera and procedurally generated scenes.

## ✨ Features

*   **Large Scale:** 10,000 unique indoor scenes, comprising 95,962 rooms and 299,073 viewpoints/RGB-D pairs.
*   **Rich Data:** Panoramic RGB-D captures with complete room-level coverage.
*   **Comprehensive Annotations:** Includes CAD drawings, floor plans, semantic segmentation, 3D detection labels and more (forthcoming).
*   **Diverse Scenes:** Comprising 1,000 real-world scenes with varied layouts and decoration styles, and 9,000 procedurally generated scenes utilizing over 100 designer-curated style templates, ensuring diverse furniture models and styles for robust training and testing.

## 🗃️ Data Organization & Access

The Realsee3D dataset is organized into individual scenes, each containing detailed multi-view RGB-D data.

*   **Data Structure & Usage:** [DATASET_STRUCTURE.md](DATASET_STRUCTURE.md) provides a comprehensive explanation of the file organization, data formats, and detailed usage instructions.
*   **Methodology:** Visit our [official website](https://dataset.realsee.ai/) for more detailed information on how real-world data is collected and how synthetic data is generated.

### 📥 How to Download

To access the dataset, you must sign a Data Usage Agreement (PDF format). You can download the agreement directly [here](docs/Realsee3D_Dataset_agreement.pdf).
Please send your request, specifying your intended use, to **developer@realsee.com** with the subject **[Realsee3D Dataset Application]**. Once your application is approved and you have signed the agreement, we will reply with download instructions and links.


## 📊 Statistics

For a detailed breakdown of dataset statistics, please refer to [metadata/README.md](metadata/README.md).

## 📋 Changelog

*   **2025-12-05:** Phase I data(RGB-D pano and extrinsics) released.
*   **2025-11-28:** Dataset introduction and official website release.

## 📄 Citation

If you use the Realsee3D dataset in your research, please cite our paper:

```
@misc{Li2025realsee3d_data,
  doi = {10.5281/zenodo.17826243},
  url = {https://doi.org/10.5281/zenodo.17826243},
  author = {Li, Linyuan and Wu, Yan and Li, Xi and Wang, Lingli and Rao, Tong and Zhou, Jie and Pan, Cihui and Hui, Xinchen},
  title = {Realsee3D: A Large-Scale Multi-View RGB-D Dataset of Indoor Scenes (Version 1.0)},
  publisher = {Zenodo},
  year = {2025}
}
```

## 📝 License

### Code License

The accompanying code for data parsing, visualization, and evaluation is released under the [MIT License](https://opensource.org/licenses/MIT), allowing for free use, modification, and distribution.

