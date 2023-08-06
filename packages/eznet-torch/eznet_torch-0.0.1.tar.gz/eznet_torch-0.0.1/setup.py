from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

VERSION = '0.0.1' 
DESCRIPTION = "Easily build PyTorch models: utils for training/testing, built-in ANN, CNN, RNN models, modular Dense and Convolutional blocks, etc."

# Setting up
setup(
       # the name must match the folder name
        name="eznet_torch", 
        version=VERSION,
        author="Pouya P. Niaz",
        author_email="<pniaz20@ku.edu.tr>",
        url='https://github.com/pniaz20/eznet_torch',
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        # packages=find_packages('eznet_torch'),
        # package_dir={'': 'eznet_torch'},
        python_requires=">=3.7, <4",
        license='MIT',
        install_requires=[
            'numpy','tqdm','scikit-learn','torch'
        ],
        keywords=['torch','pytorch','deep learning','neural network'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "Topic :: Utilities",
            "Topic :: Education",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Artificial Intelligence"
        ]
)