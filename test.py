import os


if __name__ == '__main__':
    targets = ('-01_', '-12_', '-13_', '-22_')
    original_folder = '/home/qiangde/Desktop/double_check'
    for file in os.listdir(original_folder):
        for target in targets:
            if target in file:
                file_path = os.path.join(original_folder, file)
                os.rename(file_path, file_path.replace('double_check', 'others'))


