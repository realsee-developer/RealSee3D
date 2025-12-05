import numpy as np
from typing import Dict, Optional

def compute_depth_metrics(pred: np.ndarray, gt: np.ndarray, mask: Optional[np.ndarray] = None) -> Dict[str, float]:
    """
    Compute standard metrics for depth estimation.
    
    Args:
        pred: Predicted depth map, shape (N, H, W) or (H, W).
        gt: Ground Truth depth map, same shape as pred.
        mask: Boolean mask indicating valid pixels (e.g., gt > 0).
              If None, a mask is generated based on gt > 0.
    
    Returns:
        A dictionary containing the following metrics:
        - abs_rel: Absolute Relative Error
        - sq_rel: Squared Relative Error
        - rmse: Root Mean Squared Error
        - rmse_log: Root Mean Squared Log Error
        - a1, a2, a3: Accuracy under threshold (delta < 1.25^i)
    """
    if mask is None:
        mask = gt > 0

    # Select only valid regions
    pred_valid = pred[mask]
    gt_valid = gt[mask]

    # Avoid division by zero or log(0) issues
    pred_valid = np.clip(pred_valid, 1e-3, None)
    gt_valid = np.clip(gt_valid, 1e-3, None)

    # Compute accuracy thresholds
    thresh = np.maximum((gt_valid / pred_valid), (pred_valid / gt_valid))
    a1 = (thresh < 1.25).mean()
    a2 = (thresh < 1.25 ** 2).mean()
    a3 = (thresh < 1.25 ** 3).mean()

    # Compute RMSE
    rmse = (gt_valid - pred_valid) ** 2
    rmse = np.sqrt(rmse.mean())

    # Compute RMSE Log
    rmse_log = (np.log(gt_valid) - np.log(pred_valid)) ** 2
    rmse_log = np.sqrt(rmse_log.mean())

    # Compute Relative Errors
    abs_rel = np.mean(np.abs(gt_valid - pred_valid) / gt_valid)
    sq_rel = np.mean(((gt_valid - pred_valid) ** 2) / gt_valid)

    return {
        "abs_rel": abs_rel,
        "sq_rel": sq_rel,
        "rmse": rmse,
        "rmse_log": rmse_log,
        "a1": a1,
        "a2": a2,
        "a3": a3,
    }
