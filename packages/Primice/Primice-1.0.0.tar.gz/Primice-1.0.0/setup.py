import setuptools

with open("./README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="Primice",
    version="1.0.0",
    author="Primice",
    author_email="1121796946@qq.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)