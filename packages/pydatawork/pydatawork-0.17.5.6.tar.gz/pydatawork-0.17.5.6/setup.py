

###### Thu Jun 15 13:20:21 CST 2023
# 制作完成，后续更新时，需要维护此处的信息。版本更新。入口不变。

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pydatawork',
    version='0.17.5.6',
    py_modules=['pydatawork'],
    author='jk.zhou',
    author_email='zhouqiling.bjfu@foxmail.com',
    description="jk.zhou's datawork",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords='datawork',
    url='https://github.com/jkjoker/datawork',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)

