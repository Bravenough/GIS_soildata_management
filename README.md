# 基于GIS的土壤数据评估及分析信息查询系统 - 启动说明

## 🌟 系统概述
本系统是一个基于GIS的土壤数据评估及分析信息查询系统，采用uni-app前端 + Express后端 + MySQL数据库的架构。
- **数据规模**: 10,000个土壤样本，覆盖31个省份
- **功能**: 土壤数据查询、分析、可视化和评估

## 📋 环境要求
- Node.js >= 14.0.0
- MySQL >= 5.7
- npm >= 6.0.0
- HBuilderX (可选，用于uni-app开发)

## 🗄️ 数据库配置
系统使用MySQL数据库，配置信息在 `utils/database.js` 文件中：
- **主机**: localhost
- **端口**: 3306
- **用户名**: root
- **密码**: 050316
- **数据库**: soil_data

## 🚀 快速启动

### 方法1：完整启动 (推荐)

#### 1. 安装依赖
```bash
npm install
```

#### 2. 启动后端服务
```bash
npm start
# 或者开发模式（自动重启）
npm run dev
```

#### 3. 启动前端服务

**如果遇到 "uni-serve" 命令不存在错误，请使用以下解决方案：**

**方案A: 使用HBuilderX (推荐)**
1. 打开HBuilderX
2. 文件 → 打开目录 → 选择项目文件夹
3. 右键项目根目录 → 运行 → 运行到浏览器 → Chrome

**方案B: 安装uni-app CLI**
```bash
npm install -g @dcloudio/cli
npm run dev:h5
```

**方案C: 使用启动脚本**
```bash
start-frontend.bat
```

**方案D: 直接使用测试页面**
访问: http://localhost:8081/test.html

#### 4. 访问系统
- **API测试页面**: http://localhost:8081/test.html ⭐ **推荐先访问**
- **完整前端**: http://localhost:8081/index.html
- **后端API**: http://localhost:3000

### 方法2：HBuilderX启动

1. **打开HBuilderX**
2. **文件 → 打开目录** → 选择项目文件夹
3. **右键项目根目录** → **运行 → 运行到浏览器 → Chrome**

### 方法3：仅后端测试

```bash
# 启动后端
npm start

# 测试数据库连接
npm run test-db

# 访问API测试页面
# http://localhost:8080/test.html
```

## 🔧 测试验证

### 1. 数据库连接测试
```bash
npm run test-db
```
**预期输出**:
```
✅ 统计概况数据: { totalSamples: 10000, provincesCovered: 31, averagePh: 6.76 }
✅ 土壤样本数据: 共1000条记录
🎉 所有数据库测试通过！
```

### 2. API接口测试
访问: http://localhost:8080/test.html
- 自动测试统计概况接口
- 手动测试各个API功能
- 实时显示数据库数据

## 🌐 服务地址
| 服务 | 地址 | 说明 |
|------|------|------|
| **API测试页面** | http://localhost:8081/test.html | 推荐首先访问 |
| **完整前端** | http://localhost:8081/index.html | uni-app完整界面 |
| **后端API** | http://localhost:3000 | RESTful API服务 |
| **健康检查** | http://localhost:3000/api/health | 服务状态检查 |

## 📡 API接口列表
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/statistics-overview` | GET | 获取统计概况 |
| `/api/soil-samples` | GET | 获取土壤样本数据 |
| `/api/soil-data-table` | GET | 获取土壤数据表格 |
| `/api/region-nutrient-stats` | GET | 获取区域养分统计 |
| `/api/ph-distribution-stats` | GET | 获取pH分布统计 |
| `/api/soil-texture-stats` | GET | 获取土壤质地统计 |
| `/api/nutrient-trend-data` | GET | 获取养分趋势数据 |
| `/api/soil-quality-assessment/:id` | GET | 获取土壤质量评估 |
| `/api/historical-data/:stationId` | GET | 获取历史监测数据 |
| `/api/health` | GET | 健康检查 |

## 🛠️ 故障排除

### 常见问题

#### 1. 端口被占用
```bash
# 查看占用进程
netstat -ano | findstr :3000
# 终止进程
taskkill /PID <进程ID> /F
```

#### 2. 数据库连接失败
- 检查MySQL服务是否启动
- 验证数据库配置 (`utils/database.js`)
- 确认数据库 `soil_data` 存在

#### 3. HBuilderX运行错误
- 确保安装了uni-app插件
- 重启HBuilderX
- 使用 **文件 → 打开目录** 而不是导入

#### 4. 依赖安装失败
```bash
# 清除缓存
npm cache clean --force
# 重新安装
npm install
```

#### 5. 前端页面空白
- 访问 http://localhost:8081/test.html 验证后端
- 检查浏览器控制台错误信息
- 确认两个服务都已启动

#### 6. "uni-serve" 命令不存在
这是uni-app项目的常见问题，解决方案：
- **推荐**: 使用HBuilderX图形界面运行项目
- **备选**: 安装 `npm install -g @dcloudio/cli`
- **临时**: 直接使用 http://localhost:8081/test.html 测试功能
- **脚本**: 运行 `start-frontend.bat` 选择启动方式

## 📁 项目结构
```
├── server.js              # 后端服务入口
├── utils/database.js       # 数据库操作
├── test-db.js             # 数据库测试脚本
├── test.html              # API测试页面
├── index.html             # 前端入口
├── pages/                 # uni-app页面
├── static/                # 静态资源
└── data/                  # 数据文件
```

## 🔍 开发调试
- **后端日志**: 控制台输出API请求和数据库操作
- **前端调试**: 浏览器开发者工具
- **API测试**: 使用test.html页面或Postman
- **数据库**: 使用Navicat或MySQL Workbench

## 📊 系统状态检查
1. **后端服务**: 访问 http://localhost:3000/api/health
2. **数据库连接**: 运行 `npm run test-db`
3. **前端服务**: 访问 http://localhost:8081/test.html
4. **完整功能**: 访问 http://localhost:8081/index.html

## 🎯 推荐启动流程
1. **启动后端**: `npm start`
2. **启动前端**: `npm run dev:h5`
3. **验证系统**: 访问 http://localhost:8081/test.html
4. **使用系统**: 访问 http://localhost:8081/index.html

---
**注意**: 建议首先访问 http://localhost:8081/test.html 验证系统功能正常，再使用完整的uni-app界面。 