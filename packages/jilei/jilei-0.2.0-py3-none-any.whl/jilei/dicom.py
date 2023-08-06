import os
import pydicom
import numpy as np
import dicom2nifti
from PIL import Image

DICOM_PATH = os.path.join("D:\\", "Data", "Developing", "PanHuiQiong")


def get_dicoms(dicom_path):
    # Step1. 读取目录下的所有dicom文件
    dicoms = []
    for dcm in os.listdir(dicom_path):
        if dcm.endswith('.dcm'):
            dicoms.append(dcm)

    dicoms.sort()
    dcms = []
    for i in range(len(dicoms)):
        dcm = pydicom.dcmread(os.path.join(dicom_path, dicoms[i]))
        dcms.append(dcm)

    return dcms


def change_pixel_value2(dcm, value=None, when_positive=None, when_negative=None):
    """
    将CT数据中的某个像素值替换为另一个像素值
    如果像素值等于value，则替换为when_positive。如果像素值不等于value，则替换为when_negative。
    如果when_positive或when_negative为None，则不替换。
    dcm = pydicom.dcmread(dcm_file)
    """
    if value is not None:
        arr = dcm.pixel_array
        pixel_array = np.where(arr == value, when_positive if when_positive is not None else arr,
                               when_negative if when_negative is not None else arr)
        dcm.PixelData = pixel_array.astype(np.uint16).tobytes()

    return dcm


def change_pixel_value(dcm, conditions=None, default=0):
    """

    :param dcm:
    :param conditions: 键值对，键为像素值，值为替换后的像素值
    :param default: 默认值
    :return:
    """
    arr = dcm.pixel_array
    hu_map = [arr == int(hu) for hu in conditions]
    overwrites = [int(v) for v in conditions.values()]
    pixel_array = np.select(hu_map, overwrites, default=default)
    dcm.PixelData = pixel_array.astype(np.uint16).tobytes()
    return dcm


def change_pixel_value_from_dcmfile(dcm_file, conditions=None, default=0):
    dcm = pydicom.dcmread(dcm_file)
    return change_pixel_value(dcm, conditions, default=default)


def crop_pixel_value(dcm_file, value=None, output_dir='.'):
    pixel_array = change_pixel_value_from_dcmfile(dcm_file=dcm_file, conditions={value:3000}, default=0)
    scale = (256 * 256) / np.max(pixel_array)
    pixel_array = pixel_array * scale

    # 将CT数据转换为图像
    (file, ext) = os.path.splitext(dcm_file)
    (path, filename) = os.path.split(file)
    image = Image.fromarray(pixel_array.astype(int))
    image.save(os.path.join(output_dir, f"{filename}.cropped.{value}.png"))


def dicoms_to_nii_from_path(dicoms_path, nii_file):
    dicom2nifti.dicom_series_to_nifti(dicoms_path, nii_file)


def dicoms_to_nii(dcms, nii_file):
    dicom2nifti.convert_dicom.dicom_array_to_nifti(dcms, nii_file)


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # dicoms_to_nii(DICOM_PATH, "test.nii.gz")
    dcms = get_dicoms(DICOM_PATH)

    value, when_positive, when_negative = 3252, 2000, 0
    for dcm in dcms:
        pixel_array = dcm.pixel_array
        pixel_array = np.where(pixel_array == value, 2500, 0)
        dcm.PixelData = pixel_array.astype(np.uint16).tobytes()

    dicoms_to_nii(dcms, "test4.nii.gz")
