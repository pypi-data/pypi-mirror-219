import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name='Algo-Vi',
    version='1.0.3',
    description="It visual the Search Algorithm",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/punithanae/Python_library",
    author="Punithan",
    author_email="punithanae@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    py_modules=['AlgoVi'],
    package_dir={'':'Search-Vi'},
    include_package_data=True,
    keyword=['Search', 'Sort']

)
