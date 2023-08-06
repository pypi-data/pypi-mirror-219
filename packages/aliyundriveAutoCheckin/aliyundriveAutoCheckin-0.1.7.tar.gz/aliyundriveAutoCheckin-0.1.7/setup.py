from setuptools import setup, find_packages

setup(
    name="aliyundriveAutoCheckin",
    version="0.1.7",
    author="xiaohan17",
    author_email="2799153122@qq.com",
    description="阿里云盘自动签到",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zzh0107/aliyundriveAutoCheckin",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
