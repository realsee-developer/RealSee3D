import argparse
import numpy as np
import os
import cv2
from tqdm import tqdm
from .utils.io import load_viewpoint_depth_gt, load_viewpoint_depth_pred
from .utils.alignment import align_by_ssi_lsq
from .depth_metrics import compute_depth_metrics


def evaluate(pred_dir: str, gt_dir: str, alignment: bool = False):
    """
    Main evaluation loop.
    
    Args:
        pred_dir: Directory containing user predictions.
        gt_dir: Directory containing ground truth data.
        alignment: if alignment predictions with gt.
    """

    metrics = []

    for scene_id in os.listdir(gt_dir):
        scene_dir = os.path.join(gt_dir, scene_id)

        for viewpoint_id in os.listdir(scene_dir+'/viewpoints'):
            viewpoint_dir = os.path.join(scene_dir, 'viewpoints', viewpoint_id)

            # load gt depth
            gt, gt_mask = load_viewpoint_depth_gt(viewpoint_dir)

            # load prediction
            # pred_path = 
            pr = load_viewpoint_epth_pred()

            # Resize prediction if dimensions do not match GT
            if gt.shape != pred.shape:
                pr = cv2.resize(pr, (gt.shape[1], gt.shape[0]), interpolation=cv2.INTER_NEAREST)

            # if prediction is relative depth, align it with metric depth
            if args.alignment:
                pr, _ = align_by_ssi_lsq(pr, gt, gt_mask)

            # Compute metrics for the current frame
            m = compute_depth_metrics(pr, gt, gt_mask)
            metrics.append(m)

    # Aggregate and average metrics over the entire dataset
    final_metrics = {}
    if metrics:
        for key in metrics[0].keys():
            final_metrics[key] = np.nanmean([_[key] for _ in metrics_total])

    print(f"\nEvaluation Results:")
    print("-" * 30)
    for k, v in final_metrics.items():
        print(f"{k:<10}: {v:.4f}")
    print("-" * 30)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="RealSee3D Monocular Depth Evaluation")
    parser.add_argument('--gt_dir', type=str, required=True, help="Path to ground truth directory")
    parser.add_argument('--pred_dir', type=str, required=True, help="Path to prediction directory")
    parser.add_argument('--alignment', action='store_true', help="Apply depth alignment")
    
    args = parser.parse_args()
    
    evaluate(args.pred_dir, args.gt_dir, args.alignment)
