# <center>超星学习通刷课平台</center>
## 项目背景
进入大学之后需要完成大量的网课,而**刷课平台**实际上成本非常低,大部分同学都在被割韭菜。本项目旨在开源刷课代码, 为大家提供便利。
## 项目截图
![screenshot20231211.png](pictures%2Fscreenshot20231211.png)
![screenshot202312111.png](pictures%2Fscreenshot202312111.png)
![screenshot20231211 (1).png](pictures%2Fscreenshot20231211%20%281%29.png)
![screenshot20231211 (2).png](pictures%2Fscreenshot20231211%20%282%29.png)
![screenshot20231211 (3).png](pictures%2Fscreenshot20231211%20%283%29.png)
![screenshot20231211 (4).png](pictures%2Fscreenshot20231211%20%284%29.png)
![screenshot20231211 (5).png](pictures%2Fscreenshot20231211%20%285%29.png)
![screenshot20231211 (6).png](pictures%2Fscreenshot20231211%20%286%29.png)
## 功能特点
1. 功能较为完善的前后端, 能实现在前端刷课,后端监控进度
2. 支持账号密码、二维码两种登陆方式 
3. 支持绑定多个超星账号 
4. 自动完成视频、音频、阅读、图书、章节测试的任务点
5. 内置多个题库和GPT接口,能够完成课程作业(单选、多选、判断、填空、简答)
6. 完善的日志和错误反馈, 
## TODO
1. 签到
2. 绑定EMAIL和QQ, 通过gocq-http进行错误通知
3. 自动考试
4. 支持其他网课平台(雨课堂)
5. 刷课实时更新百分比进度
## 配置文件
### Redis
```python
# backend/app/core/config/__init__.py
REDIS_HOST: str = "localhost"
REDIS_TIMEOUT: int = 5
REDIS_KEY_EXPIRE_TIMEDELTA: timedelta = timedelta(minutes=5)
```
### MySql
```python
# backend/app/core/config/__init__.py
MYSQL_HOST: str = "127.0.0.1"
MYSQL_PORT: str = "3306"
MYSQL_USER: str = "root"
MYSQL_PASSWORD: str = "123456"
MYSQL_DB: str = "chaoxing"
```
### 题库Token
```python
# backend/app/common/constants
ENNCY_TOKEN: str = ""
EVERY_TOKEN: str = ""
HEIBOOK_TOKEN: str = ""
AIDIAN_TOKEN: str = ""
WANNENG_TOKEN: str = ""
```
## 项目部署
### 前端
前端采用Vite4 + Vue3开发, 使用了Pinia+TailwindCSS+ElementPlus的技术栈
1. `npm install`安装项目依赖
2. `npm run dev`启动前端服务
### 后端
后端采用Fastapi开发, 使用了Sqlalchemy+Redis的技术栈
1. `pip install requirement.txt`安装项目依赖
2. 运行redis和mysql服务, 填写配置文件
3. 运行`create_db.py`初始化数据库
4. 运行`main.py`启动后端服务