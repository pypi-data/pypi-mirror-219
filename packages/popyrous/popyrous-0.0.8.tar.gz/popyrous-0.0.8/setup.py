from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

VERSION = '0.0.8' 
DESCRIPTION = "Pouya's Python routines. A collection of useful Python routines for everyday and professional life."

# Setting up
setup(
       # the name must match the folder name
        name="popyrous", 
        version=VERSION,
        author="Pouya P. Niaz",
        author_email="<pniaz20@ku.edu.tr>",
        url='https://github.com/pniaz20/popyrous',
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        # packages=find_packages('popyrous'),
        # package_dir={'': 'popyrous'},
        python_requires=">=3.7, <4",
        license='MIT',
        install_requires=[
            'numpy','scipy','pandas','matplotlib','seaborn','scikit-learn','gdown','pywavelets'
        ],
        keywords=['python', 'routines', 'matlab', 'zipfile', 'packages', 'time series', 'filtering', 'download', 'web'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "Topic :: Utilities"
        ]
)