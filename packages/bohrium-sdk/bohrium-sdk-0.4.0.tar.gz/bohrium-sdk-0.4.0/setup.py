from setuptools import setup
import setuptools
setup(
    name="bohrium-sdk",
    version="0.4.0",
    author="dingzhaohan",
    author_email="dingzh@dp.tech",
    url="https://github.com/dingzhaohan/bohrium-openapi-python-sdk",
    description="bohrium openapi python sdk",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyhumps",
        "rich"
    ],
    python_requires='>=3.7',
    entry_points={}
)

