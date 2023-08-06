# 使用
```
from geovis_upload_sdk import Uploader

uploader = Uploader(hostURL, appKey, secretKey)
result = uploader.upload(categoryId, file)
```



## 1 安装

```shell
pip uninstall geovis_upload_sdk

pip install geovis_upload_sdk==0.0.1

```



## 2 测试、编译和上传

### 2.1 本地测试

```shell
python setup.py develop
```



编译tar.gz：

```shell
python setup.py sdist
```





编译whl：

```
pip install wheel
python setup.py bdist_wheel
```



检查

```shell
python setup.py check 
```



上传到pypi：

```shell
pip install twine
twine upload dist/*
```



## 更新日志

`0.0.1` 基础版测试
`0.0.2` 支持分片上传
`0.0.3` 优化

