import pykinect_azure as pykinect
import cv2
import open3d as o3d
import numpy as np

# Initialize the library, if the path is not set, add the library path as argument
pykinect.initialize_libraries(track_body=True)

# Start device
device = pykinect.start_device()

# Get the calibration data
calibration = device.get_calibration(pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED, pykinect.K4A_COLOR_RESOLUTION_720P)

# Start body tracker
body_tracker = pykinect.start_body_tracker()

# Initialize visualizer
vis = o3d.visualization.Visualizer()
vis.create_window()
point_cloud = o3d.geometry.PointCloud()
vis.add_geometry(point_cloud)

while True:
    # Get capture
    capture = device.update()

    # Get body tracker frame
    body_frame = body_tracker.update()

    # Get the color image
    ret_color, color_image = capture.get_color_image()
    ret_depth, depth_image = capture.get_depth_image()

    if not ret_color or not ret_depth:
        continue

    # Draw the skeletons
    color_image_with_bodies = body_frame.draw_bodies(color_image)

    # Display the image with skeletons
    cv2.imshow("Color Image with Skeleton", color_image_with_bodies)

    # Press q key to stop
    if cv2.waitKey(1) == ord('q'):
        break

    # Transform the depth image to the point cloud
    xyz_image = pykinect.helpers.transform_depth_image_to_point_cloud(depth_image, calibration, pykinect.K4A_CALIBRATION_TYPE_DEPTH)

    # Convert the point cloud to Open3D format
    point_cloud.points = o3d.utility.Vector3dVector(xyz_image.reshape(-1, 3))
    
    # Optionally, colorize the point cloud
    if ret_color:
        color_image_reshaped = color_image.reshape(-1, 3) / 255.0
        point_cloud.colors = o3d.utility.Vector3dVector(color_image_reshaped)

    # Update the visualizer
    vis.update_geometry(point_cloud)
    vis.poll_events()
    vis.update_renderer()

# Cleanup
device.close()
cv2.destroyAllWindows()
vis.destroy_window()
