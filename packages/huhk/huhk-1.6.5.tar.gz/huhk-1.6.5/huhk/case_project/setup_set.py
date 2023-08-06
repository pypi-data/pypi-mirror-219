from setuptools import setup, find_packages

from huhk.unit_fun import FunBase

setup(
    name='huhk',  # 对外模块的名字
    version=FunBase.get_version(),  # 版本号
    description='接口自动化',  # 描述
    author='胡杭凯',  # 作者
    author_email='3173825608@qq.com',
    # package_dir={"": "huhk"},
    packages=find_packages(),
    package_data={'by': ['常用命令.py'],},
    include_package_data=True,
    entry_points={'console_scripts': ['huhk=huhk.case_project.main:main']},
    python_requires=">=3.0",
    install_requires=[
        "faker",
        "openpyxl",
        "apscheduler",
        "rsa",
        "pyDes",
        "pycryptodome",
        "xlsxwriter",
        "pandas",
        "apache-beam",
        "pytest",
        "setuptools",
        "twine",
        "requests==2.29.0",
        "pandas",
        "click",
    ],
)


