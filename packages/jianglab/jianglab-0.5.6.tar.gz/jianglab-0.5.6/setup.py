from setuptools import setup, find_packages

setup(
    name='jianglab',
    version='0.5.6',
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "treelib",
        "McsPyDataTools",
        "tqdm",
        "scipy",
        "gspread",
        "oauth2client",
        "xmltodict",
        "opencv-python",
        "ipython"

    ],
    author = "Jiang Zheng",
    author_email = "zjiang314@gmail.com",
    description = "A package for Jiang lab",
    url = "https://github.com/jiang-lab-retina/jianglab.git",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

