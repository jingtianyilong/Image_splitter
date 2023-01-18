import argparse
import os
from PIL import Image
from pathlib import Path


class Site:
    max_ratio = 0
    min_ratio = 0
    img = []
    split_num = 0
    best_split_num = 0
    magic_resolution = [1280, 1706]
    ori_file_name = ""
    ori_path = ""
    img_width = 0
    img_height = 0
    max_num = 9

    def __init__(self, site_name="red", ori_img_path="0.jpg"):
        print("init", site_name, ori_img_path)
        self.ori_file_name = Path(ori_img_path).stem
        self.ori_path = Path(ori_img_path).parent
        self.img = Image.open(ori_img_path)
        self.img_width, self.img_height = self.img.size
        self.get_best_split_num()

    def get_best_split_num(self):
        if self.img_width > self.img_height:
            self.best_split_num = int(
                self.img_width
                / (
                    self.img_height
                    * self.magic_resolution[0]
                    / self.magic_resolution[1]
                )
            )
        else:
            self.best_split_num = int(
                self.img_height
                / (self.img_width * self.magic_resolution[1] / self.magic_resolution[0])
            )
        if self.best_split_num >= self.max_num:
            self.best_split_num = self.max_num
        print("best num: ", self.best_split_num)

    def split(self, split_num):
        if self.img_width > self.img_height:
            print(self.magic_resolution[0])
            target_width = split_num * self.magic_resolution[0]
            self.img = self.img.resize(
                (target_width, int(target_width * self.img_height / self.img_width)),
                Image.ANTIALIAS,
            )
            new_image = Image.new(
                self.img.mode, (target_width, self.magic_resolution[1]), color="white"
            )
            new_image.paste(
                self.img,
                (
                    0,
                    int(
                        (
                            self.magic_resolution[1]
                            - target_width * self.img_height / self.img_width
                        )
                        / 2
                    ),
                ),
            )
            export_img_list = [
                new_image.crop(
                    [
                        i * self.magic_resolution[0],
                        0,
                        (i + 1) * self.magic_resolution[0],
                        self.magic_resolution[1],
                    ]
                )
                for i in range(split_num)
            ]
            self.save_imgs(export_img_list)
        else:
            new_image = self.img

    def save_imgs(self, img_list):
        i = 0
        for img in img_list:
            img.save(
                "{}/{}_split_{:d}.png".format(self.ori_path, self.ori_file_name, i + 1)
            )
            print(
                "save file to: {}/{}_split_{:d}.png".format(
                    self.ori_path, self.ori_file_name, i + 1
                )
            )
            i += 1

    def auto_split(self):
        print("do auto split")
        self.get_best_split_num()
        self.split(self.best_split_num)


def getArgs():
    parser = argparse.ArgumentParser(
        description="Describe which platform you want to use",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input_path", type=str, default="0.jpg", help="Path to the image to split"
    )
    parser.add_argument(
        "--platform",
        type=str,
        default="red",
        help="Describe which platform you want to use. Available: red",
    )
    parser.add_argument(
        "--format", type=str, default="png", help="Export format for the image"
    )
    parser.add_argument(
        "--export_path",
        type=str,
        default="",
        help="Path for export. Default to ~/Downloads",
    )
    args = parser.parse_args()
    return args


def getDuplicate(check_path, target_name: str):
    file_name_list_in_path = [f for f in os.listdir(check_path) if os.path.isfile(f)]
    for name in file_name_list_in_path:
        if target_name in name:
            print("some warning for duplicate name")
            return name
    return False


if __name__ == "__main__":
    args = getArgs()
    split_machine = Site(args.platform, args.input_path)
    split_machine.auto_split()
