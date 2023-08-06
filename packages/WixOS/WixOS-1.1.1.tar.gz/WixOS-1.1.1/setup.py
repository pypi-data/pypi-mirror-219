from setuptools import setup

setup(
    name="WixOS",
    version="1.1.1",
    author="Aras Tokdemir",
    author_email="aras.tokdemir@outlook.com",
    description="WixOS Package",
    packages=["WixOS"],
    install_requires=[
        "Pillow",
        "psutil",
        "PyQt5",
        "psutil",

    ],
    entry_points={
        "console_scripts": [
        "wix-main = WixOS.main:main",
        ],
    },
)
