import cv2

import numpy as np
import csv
from typing import Tuple
import pydicom
import torch
from torch.utils.data import Dataset


class ProcessedData(Dataset):

    def __init__(self, csv_file, verbose = False, transform=None):

        self.images = []
        self.labels = []
        self.transform = transform
        self.malign_count = 0
        self.benign_count = 0
        self.verbose = verbose

        self.load_images(csv_file)

    def load_images(self, csv_file):
        with open(csv_file) as file:
            csvreader = csv.reader(file)

            header = next(csvreader)
            counter = 0
            for row in csvreader:
                class_label = int(row[0])
                self.labels.append(class_label)
                if self.verbose:
                    self.get_category(class_label)

                img_path = row[1]
                img = self.load_dicom_to_array(img_path)
                transformed_img = self.img_transform(img)
                self.images.append(transformed_img)
                counter += 1

            if self.verbose:
                print(f'Loaded {counter} images, {self.benign_count} benign and {self.malign_count} malign')

    def get_category(self, label):
        if label == 0 or label == 2:
            self.malign_count += 1
        elif label == 1 or label == 3:
            self.benign_count += 1

    def img_transform(self, img_array):
        rgb_image = self.convert_to_RGB(img_array)
        resized_image = self.resize_with_pad(rgb_image, (224, 224))
        if self.transform:
            transformed_img = self.transform(resized_image)
        else:
            transformed_img = resized_image
        return transformed_img


    def convert_to_RGB(self, img_array):
        return cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)

    @staticmethod
    def resize_with_pad(image: np.array,
                        new_shape: Tuple[int, int],
                        padding_color: Tuple[int] = (255, 255, 255)) -> np.array:

        original_shape = (image.shape[1], image.shape[0])
        ratio = float(max(new_shape)) / max(original_shape)
        new_size = tuple([int(x * ratio) for x in original_shape])
        image = cv2.resize(image, new_size)
        delta_w = new_shape[0] - new_size[0]
        delta_h = new_shape[1] - new_size[1]
        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)
        image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=padding_color)
        return image

    @staticmethod
    def load_dicom_to_array(path):
        dicom_img = pydicom.dcmread(path)
        return np.array(dicom_img.pixel_array)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        image = self.images[index]
        label = self.labels[index]
        return image, label





