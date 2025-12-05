import cv2
import numpy as np

def load_viewpoint_gt(viewpoint_dir: str):

    depth_url = os.path.join(viewpoint_dir, 'depth_image.png')
    depth = cv2.imread(depth_url, cv2.IMREAD_UNCHANGED)
    depth_mask = (depth > 0)

    depth_scale_url = os.path.join(viewpoint_dir, 'depth_scale.txt')
    depth_scale = np.loadtxt(depth_scale_url)
    depth = depth / depth_scale

    pano_mask_url = os.path.join(viewpoint_dir, 'pano_mask.png')
    pano_mask = cv2.imread(pano_mask_url, cv2.IMREAD_UNCHANGED)
    depth_mask = depth_mask & pano_mask

    # If a glass/mirror mask is avalable, remove the (unreliable) depth in those regions.
    # glass_mask = 
    # depth_mask = depth_mask & (~glass_mask)

    return depth, depth_mask

def load_viewpoint_depth_pred(viewpoint_dir: str):
    """
    Load prediction results from a user-defined storage location and format.

    This function is intentionally left empty to allow users to implement their own logic
    for loading predictions based on how and where they choose to store their data.
    The implementation should be customized according to the specific data storage path 
    and serialization method used by the user.
    """
    return
