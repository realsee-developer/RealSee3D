import os
import cv2
import numpy as np
import argparse
import math

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_ply(filename, points, colors, observer_indices):
    """
    Writes a PLY file with x, y, z, r, g, b, observer_index.
    """
    with open(filename, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(points)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("property ushort observer_index\n")
        f.write("end_header\n")
        
        for i in range(len(points)):
            p = points[i]
            c = colors[i]
            oi = observer_indices[i]
            f.write(f"{p[0]:.6f} {p[1]:.6f} {p[2]:.6f} {c[0]} {c[1]} {c[2]} {oi}\n")

def process_scene(data_root, output_dir, save_individual=False):
    viewpoints_dir = os.path.join(data_root, "viewpoints")
    if not os.path.exists(viewpoints_dir):
        print(f"Error: {viewpoints_dir} not found.")
        return

    viewpoints = sorted([d for d in os.listdir(viewpoints_dir) if os.path.isdir(os.path.join(viewpoints_dir, d))])
    
    all_points = []
    all_colors = []
    all_observer_indices = []

    print(f"Found {len(viewpoints)} viewpoints.")
    
    if save_individual:
        ensure_dir(output_dir)

    for iobe, vp_id in enumerate(viewpoints):
        print(f"Processing viewpoint {iobe+1}/{len(viewpoints)}: {vp_id}")
        vp_dir = os.path.join(viewpoints_dir, vp_id)
        
        depth_path = os.path.join(vp_dir, "depth_image.png")
        scale_path = os.path.join(vp_dir, "depth_scale.txt")
        color_path = os.path.join(vp_dir, "panoImage_1600.jpg")
        mask_path = os.path.join(vp_dir, "pano_mask.png")
        ext_path = os.path.join(vp_dir, "extrinsics.txt")
        
        if not (os.path.exists(depth_path) and os.path.exists(scale_path) and 
                os.path.exists(color_path) and os.path.exists(ext_path)):
            print(f"Skipping {vp_id}: Missing files (depth, scale, color, or extrinsics).")
            continue

        # 1. Read Extrinsics
        try:
            with open(ext_path, 'r') as f:
                ext_lines = f.read().strip().split()
                ext_vals = [float(x) for x in ext_lines]
                ext = np.array(ext_vals).reshape(4, 4)
        except Exception as e:
            print(f"Error reading extrinsics for {vp_id}: {e}")
            continue

        # 2. Read Scale
        try:
            with open(scale_path, 'r') as f:
                depth_scale = float(f.read().strip())
        except Exception as e:
            print(f"Error reading depth scale for {vp_id}: {e}")
            continue

        # 3. Read Images
        # cv2.IMREAD_UNCHANGED is crucial for 16-bit depth
        depth_img = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED)
        color_img = cv2.imread(color_path, cv2.IMREAD_COLOR) # BGR

        if depth_img is None or color_img is None:
            print(f"Error reading images for {vp_id}")
            continue

        h, w = depth_img.shape
        
        # Resize Color to match Depth if needed
        if color_img.shape[:2] != (h, w):
            color_img = cv2.resize(color_img, (w, h), interpolation=cv2.INTER_LINEAR)

        # Read Mask if exists
        mask_img = None
        if os.path.exists(mask_path):
            mask_img = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
            if mask_img is not None:
                # Handle 3-channel mask
                if len(mask_img.shape) == 3:
                    mask_img = mask_img[:, :, 0]
                
                if mask_img.shape[:2] != (h, w):
                    mask_img = cv2.resize(mask_img, (w, h), interpolation=cv2.INTER_NEAREST)
        
        # 4. Generate Point Cloud
        
        # Create grid of indices
        iy, ix = np.indices((h, w))
        
        # Calculate spherical coordinates
        # yaw: [-0.5*pi, 0.5*pi]
        yaw = (iy.astype(np.float32) / h - 0.5) * np.pi
        
        # pitch: [-pi, pi]
        pitch = (ix.astype(np.float32) / w - 0.5) * 2.0 * np.pi
        
        # Filter by yaw (30 degrees cut from top/bottom poles)
        limit = 30 * np.pi / 180.0
        low_yaw = -np.pi/2 + limit
        high_yaw = np.pi/2 - limit
        
        valid_mask = (yaw >= low_yaw) & (yaw <= high_yaw)
        
        # Filter by depth
        # 0 is invalid in uint16 depth
        dist = depth_img.astype(np.float32) / depth_scale
        valid_mask = valid_mask & (depth_img > 0) & (dist >= 0.4)
        
        # Filter by Pano Mask if it exists (255 = valid)
        if mask_img is not None:
            valid_mask = valid_mask & (mask_img == 255)
        
        # Apply mask
        yaw = yaw[valid_mask]
        pitch = pitch[valid_mask]
        dist = dist[valid_mask]
        
        # Get Colors (BGR -> RGB)
        b_channel = color_img[..., 0][valid_mask]
        g_channel = color_img[..., 1][valid_mask]
        r_channel = color_img[..., 2][valid_mask]
        cols = np.stack([r_channel, g_channel, b_channel], axis=1)
        
        # Calculate Cartesian coordinates (Local)
        cos_yaw = np.cos(yaw)
        sin_yaw = np.sin(yaw)
        cos_pitch = np.cos(pitch)
        sin_pitch = np.sin(pitch)
        
        x_local = dist * cos_yaw * sin_pitch
        y_local = dist * sin_yaw
        z_local = dist * cos_yaw * cos_pitch
        
        # Transform to World coordinates
        points_local = np.stack([x_local, y_local, z_local, np.ones_like(x_local)], axis=1)
        points_world = points_local @ ext.T
        points_world = points_world[:, :3]
        
        obs_indices = np.full(len(points_world), iobe, dtype=np.uint16)
        
        if save_individual:
            ind_outfile = os.path.join(output_dir, f"{vp_id}.ply")
            write_ply(ind_outfile, points_world, cols, obs_indices)

        all_points.append(points_world)
        all_colors.append(cols)
        all_observer_indices.append(obs_indices)

    # 5. Write Output
    ensure_dir(output_dir)
    outfile = os.path.join(output_dir, "merged.ply")
    print(f"Writing output to {outfile}...")
    
    if all_points:
        final_points = np.concatenate(all_points, axis=0)
        final_colors = np.concatenate(all_colors, axis=0)
        final_observers = np.concatenate(all_observer_indices, axis=0)
        
        write_ply(outfile, final_points, final_colors, final_observers)
        print(f"Done. Saved {len(final_points)} points.")
    else:
        print("Done. No valid points found to save.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate colored point cloud from organized data.")
    parser.add_argument("--source", type=str, required=True, help="Path to the organized data directory (containing 'viewpoints' folder)")
    parser.add_argument("--output", type=str, default="pcd_results", help="Directory to save PLY files")
    parser.add_argument("--save_individual", action='store_true', help="Save individual PLY files for each viewpoint")
    
    args = parser.parse_args()
    
    process_scene(args.source, args.output, args.save_individual)