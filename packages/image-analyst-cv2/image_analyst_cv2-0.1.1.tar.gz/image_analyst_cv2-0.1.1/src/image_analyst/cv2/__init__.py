try:
    import cv2  # noqa: F401
    import cv2.dnn  # noqa: F401
except ImportError as e:
    raise ImportError(
        "OpenCV library is not found. Please install OpenCV first."
    ) from e
