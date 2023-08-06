import io
import os
import re

import setuptools


def get_long_description():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(base_dir, "README.md"), encoding="utf-8") as f:
        return f.read()


def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


def get_version():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(current_dir, "yolov8", "__init__.py")
    with io.open(version_file, encoding="utf-8") as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)


setuptools.setup(
    name="yolov8",
    version=get_version(),
    author="",
    license="",
    description=(':warning: The `yolov8` package is a placeholder, not the official Ultralytics version. Please install the official `ultralytics` package via `pip install ultralytics` instead.'),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires=">=3.7",
    install_requires=get_requirements(),
    extras_require={"tests": ["pytest"]},
    include_package_data=True,
    options={'bdist_wheel':{'python_tag':'py37.py38.py39'}},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    keywords="machine-learning, deep-learning, ml, pytorch, YOLO, object-detection, vision, YOLOv3, YOLOv4, YOLOv5, YOLOv6, YOLOv7, YOLOv8",
    entry_points={}
)
