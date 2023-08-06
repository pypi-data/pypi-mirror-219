import os
import numpy as np
from PIL import Image
import nibabel as nib
import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from skimage import color
from skimage.segmentation import find_boundaries
import SimpleITK as sitk
import cv2

np.set_printoptions(threshold=np.inf)


def get_totalsegmentation_labels():
    df = pd.read_csv('../data/TotalSegmentationLabels.txt', delimiter='\t')
    return {row[0]: row[1] for row in df.to_numpy()}


def save_image_from_2darray(images, folder, normalization=False, labeled_layer_only=False):
    os.makedirs(folder, exist_ok=True)
    for i, img in enumerate(images):
        min, max = np.min(img), np.max(img)
        if labeled_layer_only and min == max:
            continue

        if normalization:
            scaled_array = (img - min) / (max - min) * 255
            scaled_array = scaled_array.astype(np.uint8)
        else:
            scaled_array = img
        # 创建PIL图像对象
        image = Image.fromarray(scaled_array)
        # 保存图像为JPEG格式
        image.save(f'{folder}/{i + 1}.jpg')


def seperate_masks(nii_file):
    nii_data = nib.load(nii_file)
    nii_array = nii_data.get_fdata()
    images = []
    labels = get_totalsegmentation_labels()

    segmentations = set()
    for i in range(nii_array.shape[2]):
        image = nii_array[:, :, i]
        image_ravel = image.ravel()
        for pixel in image_ravel:
            if pixel not in segmentations:
                segmentations.add(pixel)

    segmentations.remove(0.0)

    for label_no in segmentations:
        images = []
        for i in range(nii_array.shape[2]):
            image = nii_array[:, :, i]
            mask = np.isclose(image, label_no, atol=1e-8)
            image[~mask] = 0
            images.append(image)

        # print(f'../outputs/{label_no}-{labels[round(label_no)]}')
        save_image_from_2darray(images, f'../outputs/{label_no}-{labels[round(label_no)]}')


def test_nii():
    # seperate_masks('../data/zqf_huge.nii.gz')

    # 读取NIfTI文件
    nii_file = '../data/hepaticvessel_022_label.nii.gz'

    nii_data = nib.load(nii_file)
    nii_array = nii_data.get_fdata()
    # print(nii_array[:, :, 237])
    print(nii_array.shape)
    print(nii_array.T.shape)
    images = []
    # for i in range(nii_array.shape[2]):
    #     image = nii_array[:, :, i]
    #     images.append(image)
    for img in nii_array.T:
        images.append(img)

    filename, extension = os.path.splitext(os.path.basename(nii_file))
    save_image_from_2darray(images, f'../outputs/{filename}', labeled_layer_only=True)


def normalize_nii(nii_file):
    # nii_file = '../data/hepaticvessel_022_label.nii.gz'
    nii_data = nib.load(nii_file)
    nii_array = nii_data.get_fdata().T


def boundary_mask_to_contour(mask):
    print(mask)


def test_boundary():
    layer = 26 - 1

    nii_file = '../data/hepaticvessel_050.nii.gz'
    # nii_array = np.fliplr(np.flipud(sitk.GetArrayFromImage(sitk.ReadImage(nii_file))[layer, :, :]))
    nii_array = np.rot90(sitk.GetArrayFromImage(sitk.ReadImage(nii_file))[layer, :, :], 2)

    pixel_min, pixel_max = np.min(nii_array), np.max(nii_array)
    print(pixel_min, pixel_max)
    scaled_array = (nii_array - pixel_min) / (pixel_max - pixel_min) * 255
    # gamma校正
    # gamma = 0.5
    # scaled_array = np.power(scaled_array, gamma)
    # pixel_min, pixel_max = np.min(scaled_array), np.max(scaled_array)
    # print(pixel_min, pixel_max)
    # scaled_array = (scaled_array - pixel_min) / (pixel_max - pixel_min) * 255

    scaled_array = scaled_array.astype(np.uint8)
    image = Image.fromarray(scaled_array)
    image.save('test.png')

    label_file = '../data/hepaticvessel_050_label.nii.gz'
    label_array = np.rot90(sitk.GetArrayFromImage(sitk.ReadImage(label_file))[layer, :, :], 2)

    label_1_mask = np.where(label_array == 1, 255 * 256, 0)
    label_2_mask = np.where(label_array == 2, 255 * 256, 0)
    label_1_mask_bound = find_boundaries(label_1_mask, connectivity=2)
    label_2_mask_bound = find_boundaries(label_2_mask, connectivity=2)

    label_rgb = color.gray2rgb(scaled_array)

    label_rgb[label_1_mask_bound] = [255, 0, 0]
    label_rgb[label_2_mask_bound] = [0, 255, 0]
    image = Image.fromarray(label_rgb)
    image.save('rgb.png')

    filename, extension = os.path.splitext(os.path.basename(nii_file))
    os.makedirs(f'../outputs/{filename}/patch', exist_ok=True)
    # 遍历边缘像素点
    for i, j in zip(*np.where(label_1_mask_bound)):
        # 以边缘像素点为中心选取 9x9 像素的方块
        x_size, y_size = nii_array.shape[0], nii_array.shape[1]

        margin = 32
        x_min = i - margin
        x_max = i + margin
        y_min = j - margin
        y_max = j + margin

        if x_min <= 0 or x_max >= x_size or y_min <= 0 or y_max >= y_size:
            continue

        # 提取方块区域
        patch = nii_array[x_min:x_max, y_min:y_max]
        patch_mask = np.where(label_1_mask[x_min:x_max, y_min:y_max] == 255 * 256, True, False)
        # patch_mask = label_1_mask_bound[x_min:x_max, y_min:y_max]

        scaled_array = (patch - pixel_min) / (pixel_max - pixel_min) * 255

        scaled_array = scaled_array.astype(np.uint8)

        # # 创建PIL图像对象

        scaled_array = color.gray2rgb(scaled_array)

        scaled_array_masked = scaled_array.copy()
        scaled_array_masked[patch_mask] = [255, 0, 0]

        # split = np.zeros((patch_mask.shape[1], 1, 3))
        # split.astype(np.uint8)
        merged = np.hstack((scaled_array, scaled_array_masked))

        image = Image.fromarray(scaled_array)
        scaled_array[patch_mask] = [255, 0, 0]
        image_masked = Image.fromarray(scaled_array)
        # # 保存图像为JPEG格式
        img = Image.fromarray(merged)

        img.save(f'../outputs/{filename}/patch/patch_{i}_{j}.png')
        # image.save(f'../outputs/{filename}/patch/patch_{i}_{j}.png')
        # image_masked.save(f'../outputs/{filename}/patch/patch_{i}_{j}_masked.png')


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def nii2jpg_with_qt(labeled_layer_only=True):
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):
            self.setWindowTitle("选择.nii文件")
            self.setGeometry(300, 300, 300, 200)

            button = QPushButton("打开", self)
            button.clicked.connect(self.openFileDialog)
            button.setGeometry(50, 50, 200, 50)

        def openFileDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt)",
                                                      options=options)
            if fileName:
                print("Selected file:", fileName)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test_boundary()
