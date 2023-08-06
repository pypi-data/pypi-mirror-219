from setuptools import setup, find_packages

setup(
    name="geovis_upload_sdk",
    version="0.0.3",
    author="kevinxuelei",
    author_email="kevinxuelei@163.com",
    description="geovis file upload sdk",
    long_description="geovis file upload sdk",
    url='https://github.com/kevinxuelei',
    packages=find_packages(),
    install_requires=[],
    # 搜索关键词
    keywords=['python', 'menu', 'dumb_menu', 'windows', 'mac', 'linux'],
    # 环境：python版本、支持系统...
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
