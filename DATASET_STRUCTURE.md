# 📂 Dataset Structure

The dataset is organized by scenes. Each scene directory contains a list of viewpoints and a subdirectory containing the data for each viewpoint.

```text
scene_id/
├── viewpoints.txt       # List of viewpoint IDs (timestamps) available in the scene
└── viewpoints/
    └── viewpoint_id/    # Directory for a specific viewpoint
        ├── panoImage_1600.jpg  # RGB Panoramic image (1600x800 usually)
        ├── depth_image.png     # Depth map (16-bit PNG)
        ├── pano_mask.png       # Validity mask for the panorama
        ├── extrinsics.txt      # 4x4 Camera extrinsic matrix (World to Camera)
        ├── depth_scale.txt     # Scale factor to convert depth pixel values to meters
        └── floor.txt           # Floor plane information
```

## Data Details

*   **RGB Panorama (`panoImage_1600.jpg`)**: High-resolution 360° panoramic image.
*   **Depth Map (`depth_image.png`)**: 16-bit depth map aligned with the RGB panorama.
*   **Extrinsics (`extrinsics.txt`)**: The pose of the camera for the viewpoint.
*   **Depth Scale (`depth_scale.txt`)**: The divisor used to obtain the metric depth (e.g., `depth_in_meters = pixel_value / scale`).
*   **Floor Info (`floor.txt`)**: Parameters defining the floor plane.
