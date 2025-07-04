# AI模特试衣系统

基于阿里云百炼API的智能试衣系统，支持上传人像和服装图片，生成AI试衣效果图。

## 功能特性

- 🎨 **智能试衣**: 上传人像和服装图片，AI自动生成试衣效果
- 📱 **美观界面**: 现代化响应式设计，支持移动端
- 📋 **历史记录**: 查看所有试衣任务的历史记录和结果
- 🔄 **实时状态**: 实时查看任务处理状态，支持手动刷新
- 🛡️ **安全配置**: 通过环境变量管理敏感配置

## 技术栈

### 后端
- **FastAPI**: 现代化Python Web框架
- **SQLAlchemy**: ORM数据库操作
- **SQLite**: 轻量级数据库
- **Pillow**: 图像处理
- **Requests**: HTTP客户端

### 前端
- **HTML5**: 语义化标记
- **CSS3**: 现代化样式设计
- **JavaScript**: 交互逻辑
- **响应式设计**: 支持各种设备

## 快速开始

### 1. 环境准备

确保您的系统已安装Python 3.8或更高版本。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制环境变量示例文件并配置：

```bash
cp env.example .env
```

编辑`.env`文件，配置您的阿里云百炼API Key：

```env
# 阿里云百炼API Key
DASHSCOPE_API_KEY=your_api_key_here

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 数据库配置
DATABASE_URL=sqlite:///./ai_model.db

# 文件上传配置
UPLOAD_DIR=uploads
MAX_FILE_SIZE=5242880  # 5MB
```

### 4. 启动应用

```bash
python run.py
```

### 5. 访问系统

打开浏览器访问：http://localhost:8000

## 使用说明

### 上传图片

1. **人像图片** (必选)
   - 格式：JPG、PNG、JPEG、BMP、HEIC
   - 大小：5KB - 5MB
   - 要求：包含完整人像，背景清晰

2. **服装图片** (至少选择一个)
   - **上装图片**：平铺图，背景干净
   - **下装图片**：平铺图，背景干净
   - 格式和大小要求同人像图片

### 查看结果

- 任务提交后会自动跳转到历史记录页面
- 可以实时查看任务处理状态
- 支持手动刷新任务状态
- 结果图片有效期为24小时

## API接口

### 上传图片并提交任务
```
POST /api/upload
Content-Type: multipart/form-data

参数:
- person_image: 人像图片文件 (必选)
- top_garment: 上装图片文件 (可选)
- bottom_garment: 下装图片文件 (可选)
```

### 获取任务列表
```
GET /api/tasks
```

### 获取单个任务详情
```
GET /api/tasks/{task_id}
```

### 刷新任务状态
```
POST /api/tasks/{task_id}/refresh
```

## 项目结构

```
AI模特/
├── backend/                 # 后端代码
│   ├── config.py           # 配置管理
│   ├── database.py         # 数据库连接
│   ├── models.py           # 数据模型
│   ├── upload_service.py   # 文件上传服务
│   ├── ai_service.py       # AI服务
│   └── main.py             # FastAPI应用
├── frontend/               # 前端代码
│   └── index.html          # 主页面
├── uploads/                # 上传文件目录
├── requirements.txt        # Python依赖
├── env.example            # 环境变量示例
├── run.py                 # 启动脚本
└── README.md              # 项目说明
```

## 注意事项

1. **API Key安全**: 请妥善保管您的阿里云百炼API Key，不要提交到版本控制系统
2. **文件限制**: 图片文件大小限制为5MB，支持常见图片格式
3. **处理时间**: AI试衣处理时间通常为1-3分钟，请耐心等待
4. **结果有效期**: 生成的试衣结果图片有效期为24小时
5. **网络要求**: 需要稳定的网络连接以访问阿里云API

## 故障排除

### 常见问题

1. **API Key错误**
   - 检查`.env`文件中的`DASHSCOPE_API_KEY`配置
   - 确认API Key有效且有足够配额

2. **图片上传失败**
   - 检查图片格式是否支持
   - 确认图片大小不超过5MB
   - 验证图片是否包含完整人像

3. **任务处理失败**
   - 检查网络连接
   - 查看错误信息详情
   - 尝试重新提交任务

### 日志查看

启动应用时会显示详细的日志信息，包括：
- 服务器启动状态
- API调用结果
- 错误信息

## 开发说明

### 添加新功能

1. 在`backend/`目录下添加新的服务模块
2. 在`main.py`中添加相应的API路由
3. 在前端页面中添加对应的交互功能

### 数据库迁移

当前使用SQLite数据库，如需迁移到其他数据库：
1. 修改`config.py`中的`DATABASE_URL`
2. 更新`requirements.txt`添加相应数据库驱动
3. 运行数据库迁移脚本

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规和API使用条款。

## 支持

如有问题或建议，请提交Issue或联系开发者。 