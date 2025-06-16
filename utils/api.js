// API接口适配层，用于uni-app前端调用
// 注意：在实际的uni-app项目中，这些API需要通过后端服务提供
// 这里模拟数据库连接，实际使用时应该通过HTTP请求调用后端API

// 模拟数据库服务（实际项目中应该通过HTTP调用后端）
const baseUrl = 'http://localhost:3000/api'; // 后端API地址

class SoilDataAPI {
  // 通用请求方法
  async request(url, method = 'GET', data = {}) {
    return new Promise((resolve, reject) => {
      uni.request({
        url: `${baseUrl}${url}`,
        method,
        data,
        header: {
          'Content-Type': 'application/json'
        },
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(`请求失败: ${res.statusCode}`));
          }
        },
        fail: (error) => {
          reject(error);
        }
      });
    });
  }

  // 获取土壤样本数据（用于地图显示）
  async getSoilSamples(filters = {}) {
    try {
      const result = await this.request('/soil-samples', 'GET', filters);
      console.log('✅ 成功获取土壤样本数据:', result.length, '条记录');
      return result;
    } catch (error) {
      console.error('❌ 获取土壤样本数据失败:', error);
      // 如果后端服务不可用，返回空数组而不是模拟数据
      uni.showToast({
        title: '数据加载失败，请检查网络连接',
        icon: 'none'
      });
      return [];
    }
  }

  // 获取土壤数据表格
  async getSoilDataTable(page = 1, pageSize = 10, filters = {}) {
    try {
      const result = await this.request('/soil-data-table', 'GET', { page, pageSize, ...filters });
      console.log('✅ 成功获取土壤数据表格:', result.data.length, '条记录');
      return result;
    } catch (error) {
      console.error('❌ 获取土壤数据表格失败:', error);
      uni.showToast({
        title: '数据加载失败，请检查网络连接',
        icon: 'none'
      });
      return { data: [], total: 0, page, pageSize, totalPages: 0 };
    }
  }

  // 获取区域养分统计数据
  async getRegionNutrientStats() {
    try {
      const result = await this.request('/region-nutrient-stats', 'GET');
      console.log('✅ 成功获取区域养分统计数据:', result.length, '个省份');
      return result;
    } catch (error) {
      console.error('❌ 获取区域养分统计失败:', error);
      return [];
    }
  }

  // 获取pH值分布统计
  async getPhDistributionStats() {
    try {
      const result = await this.request('/ph-distribution-stats', 'GET');
      console.log('✅ 成功获取pH分布统计数据:', result.length, '个分类');
      return result;
    } catch (error) {
      console.error('❌ 获取pH分布统计失败:', error);
      return [];
    }
  }

  // 获取土壤质地分布统计
  async getSoilTextureStats() {
    try {
      const result = await this.request('/soil-texture-stats', 'GET');
      console.log('✅ 成功获取土壤质地统计数据:', result.length, '种质地');
      return result;
    } catch (error) {
      console.error('❌ 获取土壤质地统计失败:', error);
      return [];
    }
  }

  // 获取养分趋势数据
  async getNutrientTrendData(months = 12) {
    try {
      const result = await this.request('/nutrient-trend-data', 'GET', { months });
      console.log('✅ 成功获取养分趋势数据:', result.length, '个月份');
      return result;
    } catch (error) {
      console.error('❌ 获取养分趋势数据失败:', error);
      return [];
    }
  }

  // 获取统计概况数据
  async getStatisticsOverview() {
    try {
      const result = await this.request('/statistics-overview', 'GET');
      console.log('✅ 成功获取统计概况数据:', result);
      return result;
    } catch (error) {
      console.error('❌ 获取统计概况失败:', error);
      return {
        totalSamples: 0,
        provincesCovered: 0,
        averagePh: 0,
        qualityDistribution: []
      };
    }
  }

  // 添加新的API方法

  // 获取土壤质量评估数据
  async getSoilQualityAssessment(sampleId) {
    try {
      const result = await this.request(`/soil-quality-assessment/${sampleId}`, 'GET');
      console.log('✅ 成功获取土壤质量评估数据:', result);
      return result;
    } catch (error) {
      console.error('❌ 获取土壤质量评估失败:', error);
      return null;
    }
  }

  // 获取历史监测数据
  async getHistoricalData(stationId, dateRange = 30) {
    try {
      const result = await this.request(`/historical-data/${stationId}`, 'GET', { dateRange });
      console.log('✅ 成功获取历史监测数据:', result.length, '条记录');
      return result;
    } catch (error) {
      console.error('❌ 获取历史监测数据失败:', error);
      return [];
    }
  }
}

// 创建API实例
const soilDataAPI = new SoilDataAPI();

export default soilDataAPI; 