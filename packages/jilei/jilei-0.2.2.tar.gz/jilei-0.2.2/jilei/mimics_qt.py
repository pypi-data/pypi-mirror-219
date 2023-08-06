import os
import re
import sys
import json
import numpy as np
import pydicom
import matplotlib.pyplot as plt
from collections import OrderedDict

from PIL import Image
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QFileDialog, QMessageBox
import dicom2nifti

from jilei.mimics import draw_pixel_value_distribution
from jilei.dicom import change_pixel_value, change_pixel_value_from_dcmfile, get_dicoms, dicoms_to_nii
from jilei.qt import pixel_array_2_qimage


def start():
    app = QApplication(sys.argv)
    window = MimicsToolWindow()
    window.show()
    sys.exit(app.exec_())


def message(title, text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Information)
    msg.addButton(QMessageBox.Ok)
    msg.exec()


def show(dcm, dcm_widget, plot_widget, xmin=None, xmax=None, threshold=None):
    if dcm is None:
        return
    image_array = draw_pixel_value_distribution(dcm=dcm, xmin=xmin, xmax=xmax, threshold=threshold,
                                                show=False)
    plot_widget.set_images(image_array=image_array)

    pixel_array = dcm.pixel_array
    scale = 255 / np.max(pixel_array)
    pixel_array = pixel_array * scale
    pixel_array = np.uint8(pixel_array)
    dcm_widget.set_images(image_array=pixel_array)


def show_label(labeled_widget, dcm_file, pixel_value):
    if dcm_file is None:
        return
    dcm = change_pixel_value_from_dcmfile(dcm_file=dcm_file, conditions={int(pixel_value): 255}, default=0)
    pixel_array = np.uint8(dcm.pixel_array)
    labeled_widget.set_images(image_array=pixel_array)


def convert_label(dcm_path=None, labels={}):
    """
    :param dcm_path:
    :param labels: 格式：[3252:airway;2491:vein;]
    :return:
    """
    if dcm_path is None or not os.path.exists(dcm_path):
        message("提示", "请指定正确的dicom文件夹路径")
        return

    if labels and labels[-1] != ';':
        labels = labels + ';'
    match = re.match(r"^(?:\d+,\d+,\w+;)+$", labels)
    if match is None:
        message("标签格式错误", "应符合 x,y,z; 的格式。例：3252,1,airway;2491,2,vein;")
        return

    # Key, Value, Class
    conditions = {kvc.split(",")[0]: kvc.split(",")[1] for kvc in labels[:-1].split(';')}
    labelnames = {kvc.split(",")[1]: kvc.split(",")[2] for kvc in labels[:-1].split(';')}

    arr = []
    dcms = get_dicoms(dicom_path=dcm_path)
    for dcm in dcms:
        dcm = change_pixel_value(dcm, conditions=conditions, default=0)
        arr.append(dcm)

    os.makedirs(os.path.join(dcm_path, 'dist'), exist_ok=True)
    dicoms_to_nii(arr, os.path.join(dcm_path, 'dist', "MSD.nii.gz"))

    # 保存标签名称
    with open(os.path.join(dcm_path, 'dist', "dataset.json"), 'w') as fp:
        labelnames["0"] = "background"
        labelnames = OrderedDict(sorted(labelnames.items()))
        datasetjson = {"labels": labelnames}
        modality = dcms[0].Modality
        if modality == "CT":
            datasetjson["modality"] = {"CT"}
        elif modality == "MR":
            datasetjson["modality"] = {"MRI"}
        else:
            datasetjson["modality"] = {modality}
        json_str = json.dumps(datasetjson, indent=4)
        fp.write(json_str)

    message("提示", "转换完成")


def convert_original(dcm_path):
    if dcm_path is None or not os.path.exists(dcm_path):
        message("提示", "请指定正确的dicom文件夹路径")
        return

    dcms = get_dicoms(dicom_path=dcm_path)
    os.makedirs(os.path.join(dcm_path, 'dist'), exist_ok=True)
    dicoms_to_nii(dcms, os.path.join(dcm_path, 'dist', "ORI.nii.gz"))


class ImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.image_label = QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)  # 图片居中显示
        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)

    def set_images(self, image_path=None, image_array=None):
        if image_path is not None:
            pixmap = QtGui.QPixmap(image_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)  # 按比例缩放图片
        elif image_array is not None:
            qimage = pixel_array_2_qimage(image_array)
            pixmap = QtGui.QPixmap.fromImage(qimage)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)  # 按比例缩放图片


class MimicsToolWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.dcm = None
        self.dcm_file = None
        self.dcm_path = None
        self.dcm_path_labeled = None
        self.labels = None

        # 创建主窗口
        self.setWindowTitle("积垒AI工具 - Mimics Mask转换为MSD(Medical Segmentation Decthlon) nii dataset")
        self.setGeometry(100, 100, 800, 600)

        """ 布局图
        |----------+----------|
        |          |          |
        |    LT    |    RT    |
        |          |          |
        |----------+----------|
        |          |          |
        |    LB    |    RB    |
        |          |          |
        |----------+----------|
        """

        """ ############################################################################################################
                                                        [M] 创建主布局
        ################################################################################################################
        """
        main_layout = QHBoxLayout()

        # --------------------------------------------------------------------------------------------------------------
        # - [L] 创建左侧布局] --------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        left_layout = QVBoxLayout()
        # -- [L] 创建左上角、左下角 ---------------------------------------------------------------------------------------
        lt_widget = ImageWidget()
        lb_widget = ImageWidget()
        # 设置大小
        lt_widget.setFixedSize(512, 512)
        lb_widget.setFixedSize(512, 512)
        # 将左上角、左下角和右下角区域添加到左侧布局中
        left_layout.addWidget(lt_widget)
        left_layout.addWidget(lb_widget)

        # --------------------------------------------------------------------------------------------------------------
        # - [R] 创建右侧布局 --------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        right_layout = QVBoxLayout()

        # -- [R] 创建右上角、右下角 ---------------------------------------------------------------------------------------
        rt_widget = QWidget()
        rb_widget = ImageWidget()
        rt_widget.setFixedSize(512, 512)
        rb_widget.setFixedSize(512, 512)

        # 测试
        test = True
        if test == True:
            lt_widget.setStyleSheet("background-color: #E12E4B;")
            lb_widget.setStyleSheet("background-color: #F9E54E;")
            # rt_widget.setStyleSheet("background-color: blue;")
            rb_widget.setStyleSheet("background-color: #5BBDC8;")

        """ ############################################################################################################
                                                     [RT] 右上角布局
        ################################################################################################################
        """
        rt_layout = QVBoxLayout(rt_widget)
        rt_layout.setSpacing(10)

        # --------------------------------------------------------------------------------------------------------------
        # [RT-1] DICOM测试
        # --------------------------------------------------------------------------------------------------------------
        rt_1_widget = QWidget()
        rt_1_layout = QVBoxLayout(rt_1_widget)
        # 第一部分：选择单张dicom进行测试，观察Hu值
        r1_title_label = QLabel("步骤一：先选取一张包含所有标签的DICOM, 观察CT异常值都有哪些")
        r1_title_label.setStyleSheet("color:rgb(5,58,58)")
        r1_title_label.setFont(QtGui.QFont("Roman times", 10, QtGui.QFont.Bold))
        self.rt_1_dicom_file_label = QLabel("选择Dicom文件: ")
        rt_1_button = QPushButton("打开DICOM文件")
        rt_1_button.clicked.connect(lambda: self.select_file(lb_widget))
        # 第二行：范围值输入框
        rt_1_range_layout = QHBoxLayout()
        rt_1_range_layout_label = QLabel("Hu范围值:")
        self.rt_1_min_input = QLineEdit()
        self.rt_1_max_input = QLineEdit()
        rt_1_range_layout_threshold_label1 = QLabel(" Count阈值:")
        self.rt_1_threshold_input = QLineEdit()
        rt_1_range_layout_threshold_label2 = QLabel("个")
        rt_1_range_layout.addWidget(rt_1_range_layout_label)
        rt_1_range_layout.addWidget(self.rt_1_min_input)
        rt_1_range_layout.addWidget(self.rt_1_max_input)
        rt_1_range_layout.addWidget(rt_1_range_layout_threshold_label1)
        rt_1_range_layout.addWidget(self.rt_1_threshold_input)
        rt_1_range_layout.addWidget(rt_1_range_layout_threshold_label2)
        show_figure_button = QPushButton("绘制")
        show_figure_button.clicked.connect(
            lambda: show(dcm=self.dcm, dcm_widget=lb_widget, plot_widget=lt_widget, xmin=self.rt_1_min_input.text(),
                         xmax=self.rt_1_max_input.text(), threshold=self.rt_1_threshold_input.text()))

        rt_1_layout.addWidget(r1_title_label)
        rt_1_layout.addWidget(self.rt_1_dicom_file_label)
        rt_1_layout.addWidget(rt_1_button)
        rt_1_layout.addLayout(rt_1_range_layout)
        rt_1_layout.addWidget(show_figure_button)

        # --------------------------------------------------------------------------------------------------------------
        # [RT-2] 标签高亮：单独显示标签
        # --------------------------------------------------------------------------------------------------------------
        rt_2_widget = QWidget()
        rt_2_layout = QVBoxLayout(rt_2_widget)
        rt_2_title_label = QLabel("步骤二：查看Hu异常值是哪个部位的标签")
        rt_2_title_label.setStyleSheet("color:rgb(5,58,58)")
        rt_2_title_label.setFont(QtGui.QFont("Roman times", 10, QtGui.QFont.Bold))

        rt_2_number_layout = QHBoxLayout()
        rt_2_number_input = QLineEdit()
        rt_2_number_button = QPushButton("单独显示标签")
        rt_2_number_button.clicked.connect(
            lambda: show_label(labeled_widget=rb_widget, dcm_file=self.dcm_file, pixel_value=rt_2_number_input.text()))
        rt_2_number_layout.addWidget(rt_2_number_input)
        rt_2_number_layout.addWidget(rt_2_number_button)

        rt_2_layout.addWidget(rt_2_title_label)
        rt_2_layout.addLayout(rt_2_number_layout)

        # --------------------------------------------------------------------------------------------------------------
        # [RT-3] 数据制作：将标签导出为MSD nii数据集
        # --------------------------------------------------------------------------------------------------------------
        rt_3_widget = QWidget()
        rt_3_layout = QVBoxLayout(rt_3_widget)

        rt_3_title_label1 = QLabel("步骤三：将Mimics导出标签(多个dicom)转换为nii")
        rt_3_title_label2 = QLabel("格式: 3252,1,airway;2491,2,vein; ")
        rt_3_title_label1.setStyleSheet("color:rgb(5,58,58)")
        rt_3_title_label2.setStyleSheet("color:rgb(5,58,58)")
        rt_3_title_label1.setFont(QtGui.QFont("Roman times", 10, QtGui.QFont.Bold))

        rt_3_path_layout = QHBoxLayout()
        self.rt_3_path_label = QLabel("选择Dicom文件目录: ")
        rt_3_path_button = QPushButton("打开目录")
        rt_3_path_button.clicked.connect(self.select_label_path)
        rt_3_path_layout.addWidget(self.rt_3_path_label)
        rt_3_path_layout.addWidget(rt_3_path_button)

        rt_3_convert_layout = QHBoxLayout()
        self.rt_3_text_input = QLineEdit()
        self.rt_3_convert_button = QPushButton("开始转换")
        self.rt_3_convert_button.clicked.connect(
            lambda: convert_label(self.dcm_path_labeled, self.rt_3_text_input.text()))
        rt_3_convert_layout.addWidget(self.rt_3_text_input)
        rt_3_convert_layout.addWidget(self.rt_3_convert_button)

        rt_3_layout.addWidget(rt_3_title_label1)
        rt_3_layout.addWidget(rt_3_title_label2)
        rt_3_layout.addLayout(rt_3_path_layout)
        rt_3_layout.addLayout(rt_3_convert_layout)

        # --------------------------------------------------------------------------------------------------------------
        # [RT-4] 将原始数据也制作为单个nii文件
        # --------------------------------------------------------------------------------------------------------------
        rt_4_widget = QWidget()
        rt_4_layout = QVBoxLayout(rt_4_widget)

        rt_4_title_label = QLabel("步骤四：选择目录，将多个原始DICOM文件转换为单个.nii")
        rt_4_title_label.setStyleSheet("color:rgb(5,58,58)")
        rt_4_title_label.setFont(QtGui.QFont("Roman times", 10, QtGui.QFont.Bold))

        rt_4_path_layout = QHBoxLayout()
        self.rt_4_path_label = QLabel("选择Dicom文件目录: ")
        rt_4_path_button = QPushButton("打开目录")
        rt_4_path_button.clicked.connect(self.select_path)
        rt_4_path_layout.addWidget(self.rt_4_path_label)
        rt_4_path_layout.addWidget(rt_4_path_button)

        rt_4_convert_layout = QHBoxLayout()
        self.rt_4_convert_button = QPushButton("开始转换")
        self.rt_4_convert_button.clicked.connect(lambda: convert_original(self.dcm_path))
        rt_4_convert_layout.addWidget(self.rt_4_convert_button)

        rt_4_layout.addWidget(rt_4_title_label)
        rt_4_layout.addLayout(rt_4_path_layout)
        rt_4_layout.addLayout(rt_4_convert_layout)

        # --------------------------------------------------------------------------------------------------------------
        # 将各个部件添加到右上角操作界面的布局中
        rt_layout.setAlignment(QtCore.Qt.AlignTop)
        rt_layout.addWidget(rt_1_widget)
        rt_layout.addWidget(rt_2_widget)
        rt_layout.addWidget(rt_3_widget)
        rt_layout.addWidget(rt_4_widget)

        # --------------------------------------------------------------------------------------------------------------
        # 组合各组件到父组件中
        # --------------------------------------------------------------------------------------------------------------
        # 将右上角操作界面添加到右侧布局中
        right_layout.addWidget(rt_widget)
        right_layout.addWidget(rb_widget)
        # 将左侧和右侧布局添加到主布局中
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        # 创建主部件，并将主布局设置为主部件的布局
        main_widget = QWidget()
        # main_widget.setStyleSheet("background-color:rgb(5,58,58);")
        main_widget.setLayout(main_layout)
        # 设置主部件为主窗口的中心部件
        self.setCentralWidget(main_widget)

    def select_file(self, widget):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择DICOM文件")
        if file_path:
            self.rt_1_dicom_file_label.setText(f"选择Dicom文件: {file_path}")
            self.dcm_file = file_path
            widget.set_images(file_path)
            self.dcm = pydicom.dcmread(self.dcm_file)

    def select_label_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择DICOM目录")
        self.rt_3_path_label.setText(folder_path)
        self.dcm_path_labeled = folder_path

    def select_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择DICOM目录")
        self.rt_4_path_label.setText(folder_path)
        self.dcm_path = folder_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MimicsToolWindow()
    window.show()
    sys.exit(app.exec_())
