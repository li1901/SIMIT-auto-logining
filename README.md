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
        git clone <项目仓库地址>  # 如有仓库可补充，无则忽略
cd SIMIT-auto-logining

2. 安装Python依赖  
        pip install -r requirements.txt  # 建议创建requirements.txt文件，包含selenium等依赖

3. 配置ChromeDriver  
        - 下载对应版本的ChromeDriver后，Windows用户可将其放入项目根目录；Linux/Mac用户可将其路径添加到系统`PATH`
      

4. 配置账号信息（推荐）  
        创建`.env`文件，存储账号密码（避免硬编码）：  
        SIMIT_USERNAME=你的账号
SIMIT_PASSWORD=你的密码

## 使用方法

### 基础运行

直接执行脚本：

python simit_auto_login.py  # 假设脚本名为simit_auto_login.py

### 定时运行

- - Windows：通过「任务计划程序」创建定时任务，触发执行Python脚本

- - Linux/Mac：通过`cron`设置定时任务（示例：每天8点执行）  
        0 8 * * * /usr/bin/python3 /path/to/simit_auto_login.py >> /path/to/logs/login.log 2>&1

## 日志说明

脚本通过`logging`模块记录日志，默认输出到控制台及日志文件（如`login_YYYYMMDD.log`），包含：

- - 登录尝试时间

- - 登录成功/失败状态

- - 异常详情（如网络错误、元素定位失败等）

## 注意事项

1. ChromeDriver版本需与本地Chrome浏览器版本严格匹配，否则会出现启动失败

2. 请勿将账号密码硬编码到脚本中，建议使用环境变量或`.env`文件管理

3. 定时任务频率不宜过高，避免被系统判定为异常请求

4. 若登录页面结构变更，需对应调整脚本中的元素定位逻辑

## 问题反馈

如遇到登录失败、脚本报错等问题，可提交Issue并附上日志信息，便于排查解决。
