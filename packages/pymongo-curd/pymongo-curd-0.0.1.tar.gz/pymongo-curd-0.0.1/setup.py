import setuptools
from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pymongo-curd',
    version='0.0.1',
    author='Guomq',
    author_email='Guo_mq@outlook.com',
    description='pymongo 的一级文档及二级文档的CURD简单封装',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/watele0528/mypackage.git',
    packages=setuptools.find_packages(),
    install_requires=['pymongo>=4.4.1'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8'
)
