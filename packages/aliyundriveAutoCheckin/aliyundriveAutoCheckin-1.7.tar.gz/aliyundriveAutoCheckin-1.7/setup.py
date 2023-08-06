from setuptools import setup, find_packages

with open("aliyundriveAutoCheckin.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='aliyundriveAutoCheckin',
    version='1.7',
    author='xiaohan17',
    author_email='2799153122@qq.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        # List your package's dependencies here
        'requests'
    ],
)
