# SIMIT-auto-logining  
自动定时完成SIMIT网络认证窗口的登录操作，解决需手动重复登录的问题，提升使用便利性。
## 功能特性

- - 自动检测并定位SIMIT网络登录窗口

- - 支持定时触发登录任务

- - 完善的日志记录（登录状态、时间、异常信息等）

- - 随机延迟机制降低风控风险

## 环境要求

### Python 依赖库

pip install selenium python-dotenv  # 推荐用dotenv管理敏感信息

- - `time`（Python内置）

- - `random`（Python内置）

- - `logging`（Python内置）

- - `datetime`（Python内置）

- - `selenium`（核心自动化库）

### 工具依赖

- - Chrome浏览器（需与chromedriver版本匹配）

- - ChromeDriver（浏览器驱动）  
        下载地址：[Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)  
        注意：需根据本地Chrome版本选择对应Driver版本，并配置到系统环境变量或脚本同级目录

## 安装步骤

1. 克隆/下载本项目代码  
        git clone <项目仓库地址> 

2. 安装Python依赖  
       包含selenium等依赖

3. 配置ChromeDriver  
        - 下载对应版本的ChromeDriver后，Windows用户可将其放入项目根目录；Linux/Mac用户可将其路径添加到系统`PATH`
      
4. 配置账号信息

## 使用方法

### 基础运行

直接执行脚本：

python login.py  


## 日志说明

脚本通过`log`记录日志，包含：

- - 登录尝试时间

- - 登录成功/失败状态

- - 异常详情（如网络错误、元素定位失败等）

## 注意事项

1. ChromeDriver版本需与本地Chrome浏览器版本严格匹配，否则会出现启动失败

2. 定时任务频率不宜过高，避免被系统判定为异常请求

## 问题反馈

如遇到登录失败、脚本报错等问题，可提交Issue并附上日志信息，便于排查解决。
