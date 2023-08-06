## Har2Postman
[![unittest](https://github.com/whitexie/Har2Postman/workflows/unittest/badge.svg)](https://github.com/whitexie/Har2Postman/actions/workflows/unittest.yml)
> 将har文件转换为postman可导入文件

## 安装
```shell script
pip install Har2Postman
```

## 使用
1.将har文件转换为postman可导入文件
```shell script
har2postman postman_echo.har

# INFO:root:read postman_echo.har
# INFO:root:Generate postman collection successfully: postman_echo.json
```
2.在postman中导入postman_echo.json文件
![](https://i.loli.net/2020/02/11/7e1Zm2wrNIF5WEB.png)
