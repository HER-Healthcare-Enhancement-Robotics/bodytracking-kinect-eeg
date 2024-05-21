import cv2
import json
import pykinect_azure as pykinect

def save_skeleton_data(body_frame, filename="skeleton_data.json"):
    skeleton_data = []

    num_bodies = body_frame.get_num_bodies()
    for i in range(num_bodies):
        body_id = body_frame.get_body_id(i)
        skeleton = body_frame.get_body_skeleton(i)
        joints = []
        for joint in skeleton.joints:
            joints.append({
                "position": {
                    "x": joint.position.xyz.x,
                    "y": joint.position.xyz.y,
                    "z": joint.position.xyz.z,
                },
                "orientation": {
                    "x": joint.orientation.wxyz.x,
                    "y": joint.orientation.wxyz.y,
                    "z": joint.orientation.wxyz.z,
                    "w": joint.orientation.wxyz.w,
                },
                "confidence_level": joint.confidence_level,
            })
        skeleton_data.append({
            "body_id": body_id,
            "joints": joints,
        })

    with open(filename, 'w') as f:
        json.dump(skeleton_data, f, indent=4)

if __name__ == "__main__":
    # Initialize the library, if the library is not found, add the library path as argument
    pykinect.initialize_libraries(track_body=True)

    # Modify camera configuration
    device_config = pykinect.default_configuration
    device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
    device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
    #print(device_config)

    # Start device
    device = pykinect.start_device(config=device_config)

    # Start body tracker
    bodyTracker = pykinect.start_body_tracker()

    cv2.namedWindow('Depth image with skeleton', cv2.WINDOW_NORMAL)
    while True:
        # Get capture
        capture = device.update()

        # Get body tracker frame
        body_frame = bodyTracker.update()

        # Get the color depth image from the capture
        ret_depth, depth_color_image = capture.get_colored_depth_image()

        # Get the colored body segmentation
        ret_color, body_image_color = body_frame.get_segmentation_image()

        if not ret_depth or not ret_color:
            continue

        # Combine both images
        combined_image = cv2.addWeighted(depth_color_image, 0.6, body_image_color, 0.4, 0)

        # Draw the skeletons
        combined_image = body_frame.draw_bodies(combined_image)

        # Display the image
        cv2.imshow('Depth image with skeleton', combined_image)

        # Save skeleton data to a file
        save_skeleton_data(body_frame, filename="skeleton_data.json")

        # Press q key to stop
        if cv2.waitKey(1) == ord('q'):
            break

    # Clean up
    cv2.destroyAllWindows()
    device.stop()
