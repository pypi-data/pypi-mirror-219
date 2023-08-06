import os
from helper.base.logger import log
from helper import __version__
import argparse
from datetime import datetime


def remove_registry(image: str):
    if image.find("/") == -1:
        return "/" + image
    return image[image.index("/") :]


def tag_image(image: str, addr: str = "127.0.0.1:5000"):
    os.system(f"docker pull {image}")

    full_name = addr + remove_registry(image)
    os.system(f"docker tag {image} {full_name}")
    return full_name


def archive(files: list[str]):
    now = datetime.now()
    os.system(
        f"docker save {' '.join(files)} | gzip > images{now.strftime('%d%H%M')}.tar.gz"
    )


def get_images(images_file: str):
    with open(images_file, "r") as file:
        return list(map(lambda x: x.strip(), file.readlines()))


def image_pack(images_file: str, addr: str):
    images = get_images(images_file)
    taged_images = list(map(lambda x: tag_image(x, addr), images))

    if len(taged_images) > 0:
        archive(taged_images)
        log.info("打包成功!")


def main():
    parser = argparse.ArgumentParser(description="镜像打包程序")
    parser.add_argument(
        "--version", action="version", version=__version__, help="显示程序版本号"
    )
    parser.add_argument("--images_file", type=str, default="images.txt", help="镜像列表文件")
    parser.add_argument(
        "--host", type=str, default="127.0.0.1:5000", help="需要导入的registry地址"
    )
    args = parser.parse_args()
    addr = args.host
    images_file = args.images_file

    try:
        image_pack(images_file, addr)
    except FileNotFoundError:
        log.error(f"指定的镜像清单文件不存在:{images_file}")


if __name__ == "__main__":
    main()
