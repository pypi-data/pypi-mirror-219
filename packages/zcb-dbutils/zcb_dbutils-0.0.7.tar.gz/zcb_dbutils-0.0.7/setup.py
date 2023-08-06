from setuptools import setup, find_packages

VERSION = '0.0.7'
DESCRIPTION = 'db utils with pymysql by chzcb'

setup(
    name="zcb_dbutils",
    version=VERSION,
    author="chzcb",
    author_email="chzcb.04@163.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md',encoding="UTF8").read(),
    install_requires=['pymysql'],
    keywords=['python', 'pymysql', 'zcb_dbutils'],
    license="MIT",
    packages=find_packages(),
    url="https://github.com/chzcb/dbutils",
    py_modules=['zcb_dbutils'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ]
)