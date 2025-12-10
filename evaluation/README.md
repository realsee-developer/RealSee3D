# RealSee3D Evaluation Toolkit

This directory contains evaluation tools for the RealSee3D dataset. We provide standard evaluation protocols for tasks such as **Monocular Depth Estimation** and **Multi-view Stereo (MVS)**.

## 1. Preparation

Before running the evaluation, please ensure your prediction files are organized correctly.
Your prediction files should be organized as belows, similar to our realsee3d data structure.

```
predictions/
├── scene_id/
    └── viewpoints/
        └── viewpoint_id/
            ├── depth.png        # predicted depth
            ├── depth_conf.png   # predicted conf
```



## 2. Monocular Depth Estimation

### Example

```bash

# Evaluate on validation set with specific metrics
python evaluate_mono.py \
    --data_path /your/realsee3d/data/path \
    --pred_path /your/prediction/data/path
```

### Metrics

**AbsRel (Absolute Relative Error)**
```
AbsRel = (1/N) * Σ|d_pred - d_gt| / d_gt
```
Measures the relative error between predicted and ground truth depth values. Lower values indicate better accuracy.

**SqRel (Squared Relative Error)**
```
SqRel = (1/N) * Σ(d_pred - d_gt)² / d_gt
```
Measures squared relative error with heavier penalty for large errors. Lower values indicate smaller overall error.

**RMSE (Root Mean Square Error)**
```
RMSE = √((1/N) * Σ(d_pred - d_gt)²)
```
Measures absolute error with sensitivity to large deviations. Lower values indicate lower overall error.

**RMSE_log (Root Mean Square Logarithmic Error)**
```
RMSE_log = √((1/N) * Σ(log(d_pred) - log(d_gt))²)
```
Logarithmic variant that focuses on relative error and reduces impact of outliers.

**δ1, δ2, δ3 (Threshold Accuracy)**
```
δ1: % of pixels where max(d_pred/d_gt, d_gt/d_pred) < 1.25
δ2: % of pixels where max(d_pred/d_gt, d_gt/d_pred) < 1.25²
δ3: % of pixels where max(d_pred/d_gt, d_gt/d_pred) < 1.25³
```
Measure the percentage of predictions within specific error thresholds. Higher values indicate better accuracy.
