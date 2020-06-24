import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'pandas',
    'xlrd',
    'tqdm',
    'matplotlib'
]

setuptools.setup(
    name="SAPMA",
    version="0.0.1",
    author="Abel van Beek",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Imable/simple-air-pollution-modeling-approach",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)