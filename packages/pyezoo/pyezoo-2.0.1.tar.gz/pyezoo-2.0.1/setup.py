from setuptools import setup

import setup_config

# 将readme文件中内容加载进来
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=setup_config.ezoo_group_name,
    version=setup_config.ezoo_version,
    description='python3 sdk for ezoodb.',
    python_requires=">=3.7",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='eZoo',
    author_email='ezoo@ezoodb.com',
    url= "https://www.ezoodb.com",
    requires=['thrift'],
    packages=setup_config.ezoo_packages,
    install_requires=["thrift"],
    project_urls={
        "Documentation": "https://www.ezoodb.com/ezoo-doc?u=/doc/3.eZoo%25E6%258A%2580%25E6%259C%25AF%25E6%2589%258B%25E5%2586%258C/5.eZoo-API/",
    }
)
