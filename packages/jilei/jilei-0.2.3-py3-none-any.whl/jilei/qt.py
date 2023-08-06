from PyQt5.QtGui import QImage


def pixel_array_2_qimage(pixel_array):
    if len(pixel_array.shape) == 3:
        height, width, channel = pixel_array.shape
        bytes_per_line = channel * width
        qimage = QImage(pixel_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
    elif len(pixel_array.shape) == 2:
        height, width = pixel_array.shape
        bytes_per_line = width
        qimage = QImage(pixel_array.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
    else:
        raise Exception(f"不支持的像素数组: pixel_array.shape={pixel_array.shape}")
    return qimage
