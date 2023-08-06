import os
import pydicom
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

plt.rcParams['font.family'] = 'Microsoft YaHei'

DICOM_PATH = os.path.join("D:\\", "Data", "Developing", "PanHuiQiong")


def draw_pixel_value_distribution(dcm, xmin=None, xmax=None, threshold=None, save_image=False, is_print=True,
                                  show=True):
    # dcm = pydicom.dcmread(dcm_file)
    pixel_array = dcm.pixel_array.astype(int)  # 获取CT数据，转换为浮点数类型

    pixels = pixel_array.reshape(-1)
    unique_elements, counts = np.unique(pixels, return_counts=True)
    for i in range(1, len(unique_elements)):
        if unique_elements[i] < unique_elements[i - 1]:
            raise Exception("np.unique得到无序列表")

    if xmin:
        xmin = int(xmin)
        less_than_xmin = np.where(unique_elements < xmin, True, False)
        _, c = np.unique(less_than_xmin, return_counts=True)
        imin = c[1]
    else:
        imin = 0

    if xmax:
        xmax = int(xmax)
        more_than_xmax = np.where(unique_elements > xmax, True, False)
        _, c = np.unique(more_than_xmax, return_counts=True)
        imax = -c[1] if len(c) == 2 else None
    else:
        imax = None

    print(f"最小值:{unique_elements[0]}, 最大值:{unique_elements[-1]}")
    print(f"imin:{imin}, imax:{imax}")
    unique_elements, counts = unique_elements[imin:imax], counts[imin:imax]
    # 绘制曲线
    plt.plot(unique_elements, counts)
    # 绘制高于threshold的异常点
    if threshold:
        threshold = int(threshold)
        stack_arr = np.stack((unique_elements, counts), axis=1)
        stack_arr = stack_arr[stack_arr[:, 1] >= threshold]
        threshold_elements, threshold_counts = stack_arr[:, 0], stack_arr[:, 1]
        plt.scatter(threshold_elements, threshold_counts, color='red', marker='o')
        for x, y in stack_arr:
            plt.text(x, y, f'({x}, {y})', ha='center', va='bottom', color='r')
    plt.title('统计不同Pixel value的像素个数的分布')
    plt.xlabel('Pixel value（Hu值）')
    plt.ylabel('像素个数')
    plt.xlim(unique_elements[0], unique_elements[-1] + 1)
    plt.ylim(0, np.max(counts) + 1)

    if save_image is True:
        (file, ext) = os.path.splitext(dcm_file)
        (path, filename) = os.path.split(file)

        scale = (256 * 256) / np.max(unique_elements)
        image = Image.fromarray((pixel_array * scale).astype(int))
        image.save(f"{filename}.png")

    # 打印出关键位置，查看具体异常像素值是哪几个
    if is_print is True:
        print("# 打印出关键位置，查看具体异常像素值是哪几个")
        for i, v in enumerate(unique_elements):
            c = counts[i]
            if threshold:
                if c >= int(threshold):
                    print(f"| \033[7;34;34m{v}\033[0m\t\033[31m{c}\033[0m\t", end=" ")
                else:
                    print(f"| {v}\t{c}\t", end=" ")
            else:
                c_color = 38 if c <= 10 else 32 if c < 1000 else 33 if c < 2000 else 31
                v_bg = "1;38;38m" if c <= 10 else "7;34;34m"
                print(f"| \033[{v_bg}{v}\033[0m\t\033[{c_color}m{c}\033[0m\t", end=" ")
            if (i + 1) % 10 == 0:
                print("|")

    if show is not True:
        # 获取FigureCanvas对象
        canvas = plt.gcf().canvas
        canvas.draw()
        # 获取绘图的渲染器
        renderer = canvas.get_renderer()
        # 渲染图形为RGB字节流
        image_rgb = renderer.tostring_rgb()
        # 将RGB字节流转换为NumPy数组
        width, height = canvas.get_width_height()
        image_array = np.frombuffer(image_rgb, dtype=np.uint8).reshape(height, width, 3)
        # 在此可以使用image_array，如保存到文件、进行进一步的处理等
        return image_array
    else:
        plt.show()


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    dcm_file = os.path.join(DICOM_PATH, "Pan Hui Qiong0280.dcm")
    # dicoms_to_nii(DICOM_PATH, "test.nii.gz")
    image_array = draw_pixel_value_distribution(dcm_file=dcm_file, show=False)
    print(type(image_array))
    image = Image.fromarray(image_array)
    image.save("testtest.png")
