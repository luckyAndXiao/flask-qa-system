# Flask 问答网站

基于 Flask 构建的轻量级问答平台，支持用户发布问题、回答和评论的完整交互功能。

## ✨ 功能特性

### 用户互动
- 📝 提问与编辑功能
- 💬 撰写/删除回答
- 💭 多级评论功能
- 🔍 关键词搜索问题

### 数据管理
- 🗃️ MySQL 关系型数据库存储
- 🔒 基于 Session 的登录系统
- 📊 数据关系建模（用户-问题-回答-评论）
- ⚡ 数据库迁移与版本控制

## 🛠️ 技术栈
| 类别         | 技术实现                  |
|--------------|--------------------------|
| 后端框架     | Flask + Blueprint        |
| ORM          | SQLAlchemy               |
| 前端模板     | Jinja2 + Bootstrap     |
| 表单验证     | WTForms                  |
| 数据库       | MySQL 8.0   Redis             |

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 8.0+
- pip 包管理器

### 部署流程

1. 克隆仓库
```bash
git clone https://github.com/yourusername/flask-qa-platform.git
cd flask-qa-platform
```
