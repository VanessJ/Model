import csv
import enum
import os
from os import listdir
from os.path import isfile, join
import re


class Labels(enum.Enum):
    MASS_MALIGN = 0
    MASS_BELIGN = 1
    CALC_MALIGN = 2
    CALC_BELIGN = 3


class CSVLoader:

    def __init__(self, absolute_path):
        self.REBUILD_CSV = False
        self.absolute_path = absolute_path

    def loadCSV(self, path):
        if self.REBUILD_CSV:
            with open(path) as file:
                csvreader = csv.reader(file)

                # create modified csv file
                name = self.create_modified_file_name(path)
                f = open(name, 'w', newline='')
                writer = csv.writer(f)
                header = ['CATEGORY', 'IMG_PATH']
                writer.writerow(header)

                header = next(csvreader)
                line_count = 1
                for row in csvreader:
                    # print(f'{", ".join(row)}')
                    cropped_image = row[12]
                    roi_mask = row[13]
                    line_count += 1
                    img_path = self.get_img_path(cropped_image, roi_mask)
                    category = row[9]
                    category = self.get_category(category, path)

                    new_row = [category, img_path]
                    writer.writerow(new_row)

                print(f'Processed {line_count} lines.')
        else:
            print("Creation of new CSV file skipped")

    @staticmethod
    def create_modified_file_name(original_file):
        list = original_file.split('.')
        name = list[0] + "_for_training"
        new_name = name + ".csv"
        return new_name

    @staticmethod
    def get_category(category, path):
        MASS = -1
        CALC = -2

        if bool(re.search('mass', path)):
            pre_category = MASS
        else:
            pre_category = CALC

        if pre_category == MASS:
            if category.startswith('M'):
                category = Labels.MASS_MALIGN.value
            else:
                category = Labels.MASS_BELIGN.value
        else:
            if category.startswith('M'):
                category = Labels.CALC_MALIGN.value
            else:
                category = Labels.CALC_BELIGN.value

        return category

    def get_img_path(self, cropped_img_path, roi_mask_path):
        img_path = self.fix_path(cropped_img_path)
        mask_path = self.fix_path(roi_mask_path)

        if img_path != mask_path:

            # file 1
            files = [f for f in listdir(img_path) if isfile(join(img_path, f))]
            if len(files) != 1:
                print("PANIKA!!!!")
                os._exit(-1)
            files = self.dcom_absolute_paths(img_path, files)
            file_1 = files[0]

            # file 2
            files = [f for f in listdir(mask_path) if isfile(join(mask_path, f))]
            if len(files) != 1:
                print("PANIKA!!!!")
                os._exit(-1)
            files = self.dcom_absolute_paths(mask_path, files)
            file_2 = files[0]

            mask_path = self.get_bigger_file((file_1, file_2))
            img_path = self.get_smaller_file((file_1, file_2))

        else:
            files = [f for f in listdir(img_path) if isfile(join(img_path, f))]
            if len(files) != 2:
                print("PANIKA!!!!")
                os._exit(-1)
            files = self.dcom_absolute_paths(img_path, files)
            mask_path = self.get_bigger_file(files)
            img_path = self.get_smaller_file(files)
        return img_path

    @staticmethod
    def dcom_absolute_paths(directory, files):
        file_paths = []
        for file in files:
            file = directory + "\\" + file
            file_paths.append(file)
        return file_paths

    @staticmethod
    def get_bigger_file(files):
        file_1_size = os.path.getsize(files[0])
        file_2_size = os.path.getsize(files[1])
        if file_1_size > file_2_size:
            return files[0]
        else:
            return files[1]

    @staticmethod
    def get_smaller_file(files):
        file_1_size = os.path.getsize(files[0])
        file_2_size = os.path.getsize(files[1])
        if file_1_size > file_2_size:
            return files[1]
        else:
            return files[0]

    def fix_path(self, path):
        path_list = path.split('/')
        path_list.pop()
        fixed_path = self.absolute_path + '\\'.join(path_list)
        return fixed_path



