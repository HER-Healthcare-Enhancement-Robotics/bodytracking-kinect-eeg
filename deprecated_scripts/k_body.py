# Para el esqueleto de body tracking, a veces falla

import pykinect_azure as pykinect
import cv2

# Initialize the library, if the path is not set, add the library path as argument
pykinect.initialize_libraries(track_body=True)

# Start device
device = pykinect.start_device()

# Idk vi que esto jalaba en un issue
# device_config = pykinect.default_configuration
# device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
# device_config.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED
# device_config.color_format = pykinect.K4A_IMAGE_FORMAT_COLOR_MJPG
# device_config.camera_fps = pykinect.K4A_FRAMES_PER_SECOND_30
# device_config.synchronized_images_only = True

# Start body tracker
body_tracker = pykinect.start_body_tracker()

while True:
    try:
        # Get capture
        capture = device.update()

        if capture is None:
            print("Failed to capture image")
            continue

        # Get body tracker frame
        body_frame = body_tracker.update()

        if body_frame is None:
            print("Failed to get body frame")
            continue

        # Get the color image
        ret, depth_color_image = capture.get_colored_depth_image()

        if not ret:
            print("Failed to get colored depth image")
            continue

        # Draw the skeletons
        depth_color_image = body_frame.draw_bodies(depth_color_image)

        # Display the image
        cv2.imshow("Color Image with Skeleton", depth_color_image)

        # Press q key to stop
        if cv2.waitKey(1) == ord('q'):
            break
    except Exception as e:
        print(f"Error: {e}")

cv2.destroyAllWindows()
