import os


def read_training_logs(dataset_id, configuration, fold):
    """

    :param results_pa"D:\nnUNet\nnUNet_results\"
    :param dataset_id: 数字 Dataset006_Lung的dataset_id就为6
    :param configuration: 训练模式，可选的有[2d | 3d_lower | 3d_fullres | 3d_cascade_fullres]
    :param fold: 交叉验证数量
    :return:
    """
    results_path = os.environ.get("nnUNet_results")
    raw_path = os.environ.get("nnUNet_raw")
    datasets = os.listdir(results_path)

    dataset = ''
    for d in datasets:
        if str(dataset_id).zfill(3) in d:
            dataset = d

    if dataset == '':
        exit(f"没有找到数据集：dataset_id={str(dataset_id).zfill(3)}")

    logs_path = os.path.join(results_path, dataset, f"nnUNetTrainer__nnUNetPlans__{configuration}", f"fold_{fold}")
    print(os.listdir(logs_path))


def _find_last_epoch_from_logfile(file):
    pass


if __name__ == "__main__":
    read_training_logs(6, "3d_fullres", 5)
