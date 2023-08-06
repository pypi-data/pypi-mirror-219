from pathlib import Path
from setuptools import find_namespace_packages, setup

# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

# Define our package
setup(
    name="TinetApiRequest",
    version="0.1.9",
    description="天润接口测试库",
    author="天润-测试",
    author_email="zhupeng@ti-net.com.cn",
    url="https://www.ti-net.com.cn/",
    python_requires=">=3.7",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    license='MIT',
)