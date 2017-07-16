# 落书 API Server

```
Python 3.6
Anaconda 3
Django 1.11
```
## 开发环境部署

1.开发机
```shell
pip freeze > requirements.txt
```
2.服务器
```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
cd serverapi(部署目录)
pip install -r requirements.txt
```

## 守护进程
```
使用Nodejs开发的PM2模块(fork)
```

```nodejs
pm2 start auto.sh
```

### 开发进度

- [x]〈服务器〉用户登录
- [x]〈服务器〉借阅信息
- [x]〈服务器〉图书续借
- [x]〈服务器〉图书检索
- [x]〈服务器〉借阅排行榜
- [x]〈服务器〉检索排行榜
- [x]〈服务器〉馆藏信息
- [x]〈服务器〉搭建服务器API接口
- [x]〈服务器〉功能模块化与异常处理
- [x]〈服务器〉安全（加密解密）
- [x]〈服务器〉服务器全部功能测试
- [x]〈服务器〉搭建临时测试API供小程序调试使用
- [x]〈服务器改进〉搜索功能分页，减少搜索等待时间
- [x]〈小程序〉首页-框架与逻辑
- [ ]〈小程序〉借阅-框架与逻辑
- [ ]〈小程序〉书架-框架与逻辑
- [ ]〈小程序〉我的-框架与逻辑
- [ ]〈小程序〉整体测试与改进
- [ ]〈系统〉域名备案或者解决方案
- [ ]〈系统〉小程序-服务器连接测试
- [ ]〈系统〉系统正常工作流程测试
- [ ]〈系统〉系统异常处理测试
- [ ]〈系统〉总结与改进意见
