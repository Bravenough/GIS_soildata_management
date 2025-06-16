# 土壤数据管理系统 - MySQL数据库指南

## 🎯 系统说明

本系统已完全采用MySQL数据库，所有前端页面和数据服务都已配置为MySQL专用。

## 📋 环境要求

- MySQL 8.0+ (推荐)
- Node.js 14+
- Python 3.8+ (仅用于数据装载)

## 🔧 MySQL数据库配置

### 1. 修改数据库连接配置

编辑以下两个文件中的数据库配置：

**`utils/database.js`** 和 **`api/database.js`**：
```javascript
const dbConfig = {
  host: 'localhost',
  port: 3306,
  password: 'your_password', // 修改为您的MySQL密码
  database: 'soil_data',
  charset: 'utf8mb4',
  connectionLimit: 10,
  acquireTimeout: 60000,
  timeout: 60000
};
```

### 2. 创建数据库和装载数据

```bash
# 1. 确保MySQL服务运行
# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 运行MySQL专用装载脚本
python load_mysql_demo.py
```

### 3. 安装前端依赖

```bash
npm install
```

## 🚀 启动系统

1. **确保MySQL服务正在运行**
2. **确保数据库已创建并装载数据**
3. **启动前端项目**（在HBuilderX中运行）

## 📊 数据库结构

系统包含17个核心数据表：
- `regions` - 地区信息
- `soil_samples` - 土壤样本
- `soil_test_data` - 检测数据
- `soil_quality_assessments` - 质量评估
- `historical_monitoring` - 历史监测
- 等等...

总计约26万条真实土壤数据。

## 🔍 可视化工具推荐

- **Navicat for MySQL**
- **MySQL Workbench**
- **phpMyAdmin**
- **DataGrip**

连接信息：
- 主机：localhost
- 端口：3306
- 数据库：soil_data
- 用户：root (或您的MySQL用户)

## 📈 功能特性

✅ **已实现的功能**：
- 地图可视化采样点数据
- 土壤数据管理和分页查询
- 高级筛选和排序
- 统计图表展示
- 评估分析系统
- 历史数据趋势
- 数据导出功能

✅ **数据库特性**：
- 连接池优化
- 错误处理和重连
- 响应式数据加载
- 并行查询优化

## 🛠️ 故障排除

### 常见问题：

1. **连接失败**
   - 检查MySQL服务状态
   - 确认连接密码正确
   - 检查端口是否开放

2. **数据加载失败**
   - 确认数据库存在
   - 检查表结构是否完整
   - 查看控制台错误信息

3. **前端编译错误**
   - 运行 `npm install` 确保依赖完整
   - 检查import语句位置

## 📝 系统架构

```
前端页面 → utils/api.js → utils/database.js → MySQL数据库
         ↓
    降级机制 → 模拟数据（仅在MySQL不可用时）
```

所有页面已配置为MySQL优先，确保最佳性能和数据一致性。

---

**注意**：系统已完全移除SQLite支持，专注于MySQL高性能数据服务。 