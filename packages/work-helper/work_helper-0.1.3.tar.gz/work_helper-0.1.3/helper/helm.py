import argparse
from helper import __version__
import os
from helper.base.logger import log
import re

YAMLS_DIR = "yamls"


def parse_yaml(charts_dir: str, namespace: str):
    for dir in os.listdir(charts_dir):
        path = os.path.join(charts_dir, dir)
        if os.path.isdir(path):
            if dir == "infrastructure":
                parse_infrastructure(path)
            elif os.path.exists(os.path.join(path, "values.yaml")):
                parse_charts(path, dir, namespace)


def parse_charts(path: str, app: str, namespace: str):
    log.info(f"处理Helm Charts：{path}")
    os.system(
        f"helm template {path} -n {namespace} > {os.path.join(YAMLS_DIR,app+'.yaml')}"
    )


def parse_infrastructure(path: str):
    log.info(f"处理基础定义：{path}")
    fi = open(os.path.join(YAMLS_DIR, "infrastructure.yaml"), "w", encoding="utf-8")
    for entry in os.listdir(path):
        file_path = os.path.join(path, entry)
        if os.path.isfile(file_path) and entry.endswith(".yaml"):
            with open(file_path, encoding="utf-8") as f:
                content = f.read().strip()
                if len(content) > 0:
                    fi.write(content + "\n---\n")
    fi.close()


def capture_images():
    log.info("生成镜像列表")
    fi = open("images.txt", "w", encoding="utf-8")
    pattern = re.compile(r"\simage:\s(.+)\s")
    for entry in os.listdir(YAMLS_DIR):
        file_path = os.path.join(YAMLS_DIR, entry)
        if os.path.isfile(file_path) and entry.endswith(".yaml"):
            with open(file_path, "r", encoding="utf-8") as f:
                matches: list[str] = pattern.findall(f.read())
                for img in matches:
                    fi.write(img.strip('"') + "\n")

    fi.close()


def main():
    parser = argparse.ArgumentParser(description="镜像打包程序")
    parser.add_argument(
        "--version", action="version", version=__version__, help="显示程序版本号"
    )
    parser.add_argument("--charts", type=str, default=".", help="charts目录")
    parser.add_argument("--namespace", type=str, default="sigma7", help="命名空间")
    args = parser.parse_args()
    charts_dir = args.charts
    ns = args.namespace

    os.makedirs(YAMLS_DIR, exist_ok=True)
    parse_yaml(charts_dir, ns)
    capture_images()


if __name__ == "__main__":
    main()
