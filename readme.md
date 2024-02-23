# Vocab Builder

Vocab Builder是一个帮助用户通过听写方式学习新单词的Web应用。该应用支持单词的添加、编辑、删除功能，并且能够跟踪每个单词的听写次数，优先让用户练习那些听写次数较少的单词。

## 功能

- 单词的添加、编辑和删除
- 单词听写练习
- 根据听写次数优先选择单词进行练习
- 支持通过CSV文件批量导入单词

## 技术栈

- Frontend: HTML, CSS, JavaScript
- Backend: Flask (Python)
- Database: MongoDB

## 安装

### 环境要求

- Python 3.6+
- MongoDB

### 步骤

1. 克隆仓库到本地：

[git clone https://your-repository-url.git](https://github.com/zhangrongyu0101/vocab-builder.git)
```
cd vocab-builder
```

2. 安装依赖：

```
pip install -r requirements.txt
```

3. 启动MongoDB服务（根据你的安装方式和操作系统可能有所不同）。


4. 启动应用：

```
python run.py
```

应用现在应该在`http://127.0.0.1:5000/`上运行。

## 使用

TODO
（在这一部分，提供一些基本的使用说明，比如如何添加单词，如何开始听写练习等。）

## 贡献

欢迎任何形式的贡献，无论是新功能、bug修复还是文档改进。请先fork仓库并提交pull请求。

## 许可证

MIT


## 下一步的工作
数据库上云

新增单词本功能

美化前端页面

使用TS重构部分代码
