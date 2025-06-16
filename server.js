const express = require('express');
const cors = require('cors');
const DatabaseService = require('./utils/database.js');

const app = express();
const PORT = 3000;

// 中间件
app.use(cors());
app.use(express.json());

// API路由

// 获取土壤样本数据（用于地图显示）
app.get('/api/soil-samples', async (req, res) => {
  try {
    const filters = req.query;
    const data = await DatabaseService.getSoilSamples(filters);
    res.json(data);
  } catch (error) {
    console.error('获取土壤样本数据失败:', error);
    res.status(500).json({ error: '获取土壤样本数据失败' });
  }
});

// 获取土壤数据表格
app.get('/api/soil-data-table', async (req, res) => {
  try {
    const { page = 1, pageSize = 10, ...filters } = req.query;
    const data = await DatabaseService.getSoilDataTable(
      parseInt(page), 
      parseInt(pageSize), 
      filters
    );
    res.json(data);
  } catch (error) {
    console.error('获取土壤数据表格失败:', error);
    res.status(500).json({ error: '获取土壤数据表格失败' });
  }
});

// 获取区域养分统计数据
app.get('/api/region-nutrient-stats', async (req, res) => {
  try {
    const data = await DatabaseService.getRegionNutrientStats();
    res.json(data);
  } catch (error) {
    console.error('获取区域养分统计失败:', error);
    res.status(500).json({ error: '获取区域养分统计失败' });
  }
});

// 获取pH值分布统计
app.get('/api/ph-distribution-stats', async (req, res) => {
  try {
    const data = await DatabaseService.getPhDistributionStats();
    res.json(data);
  } catch (error) {
    console.error('获取pH分布统计失败:', error);
    res.status(500).json({ error: '获取pH分布统计失败' });
  }
});

// 获取土壤质地分布统计
app.get('/api/soil-texture-stats', async (req, res) => {
  try {
    const data = await DatabaseService.getSoilTextureStats();
    res.json(data);
  } catch (error) {
    console.error('获取土壤质地统计失败:', error);
    res.status(500).json({ error: '获取土壤质地统计失败' });
  }
});

// 获取养分趋势数据
app.get('/api/nutrient-trend-data', async (req, res) => {
  try {
    const { months = 12 } = req.query;
    const data = await DatabaseService.getNutrientTrendData(parseInt(months));
    res.json(data);
  } catch (error) {
    console.error('获取养分趋势数据失败:', error);
    res.status(500).json({ error: '获取养分趋势数据失败' });
  }
});

// 获取土壤质量评估数据
app.get('/api/soil-quality-assessment/:sampleId', async (req, res) => {
  try {
    const { sampleId } = req.params;
    const data = await DatabaseService.getSoilQualityAssessment(sampleId);
    res.json(data);
  } catch (error) {
    console.error('获取土壤质量评估失败:', error);
    res.status(500).json({ error: '获取土壤质量评估失败' });
  }
});

// 获取历史监测数据
app.get('/api/historical-data/:stationId', async (req, res) => {
  try {
    const { stationId } = req.params;
    const { dateRange = 30 } = req.query;
    const data = await DatabaseService.getHistoricalData(stationId, parseInt(dateRange));
    res.json(data);
  } catch (error) {
    console.error('获取历史监测数据失败:', error);
    res.status(500).json({ error: '获取历史监测数据失败' });
  }
});

// 获取统计概况数据
app.get('/api/statistics-overview', async (req, res) => {
  try {
    const data = await DatabaseService.getStatisticsOverview();
    res.json(data);
  } catch (error) {
    console.error('获取统计概况失败:', error);
    res.status(500).json({ error: '获取统计概况失败' });
  }
});

// 健康检查接口
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: '土壤数据API服务正常运行' });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`🚀 土壤数据API服务器已启动`);
  console.log(`📍 服务地址: http://localhost:${PORT}`);
  console.log(`🔍 健康检查: http://localhost:${PORT}/api/health`);
  console.log(`📊 API文档: http://localhost:${PORT}/api/soil-samples`);
});

// 优雅关闭
process.on('SIGINT', async () => {
  console.log('\n🛑 正在关闭服务器...');
  await DatabaseService.close();
  process.exit(0);
});

module.exports = app; 