# Kinect SDK connection, no body tracking, only displays the camera
# Uses pyk4a
from pyk4a import PyK4A, Config, ColorResolution, DepthMode, ImageFormat
import cv2
import numpy as np

# Set up configuration
config = Config(
    color_resolution=ColorResolution.RES_720P,
    depth_mode=DepthMode.NFOV_UNBINNED,
    camera_fps=2,
    color_format=ImageFormat.COLOR_BGRA32,
    synchronized_images_only=True,
)

# Initialize and start the device
k4a = PyK4A(config)
k4a.start()

try:
    while True:
        capture = k4a.get_capture()

        if capture.color is not None:
            color_image = capture.color
            cv2.imshow("Color Image", color_image)

        if capture.depth is not None:
            depth_image = capture.depth

            # Normalize the depth image to fall between 0 and 255
            depth_normalized = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX)

            # Convert depth image to 8-bit
            depth_normalized = np.uint8(depth_normalized)

            # Apply a colormap (e.g., COLORMAP_JET)
            depth_colored = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_JET)

            cv2.imshow("Colored Depth Image", depth_colored)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    k4a.stop()
    cv2.destroyAllWindows()
