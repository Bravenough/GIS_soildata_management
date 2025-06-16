<script>
import { ref, reactive, onMounted } from 'vue';
import soilDataAPI from '@/utils/api.js';

export default {
  name: 'QueryView',
  setup() {
    // 查询条件
    const queryParams = reactive({
      region: '全国',
      startDate: '2022-01-01',
      endDate: '2023-10-31',
      nutrient: '全部',
      minValue: '',
      maxValue: '',
      soilType: '全部',
      sortBy: 'time',
      sortOrder: 'desc',
      page: 1,
      pageSize: 10
    });
    
    // 查询结果
    const queryResults = ref([]);
    const totalResults = ref(0);
    const totalPages = ref(0);
    const isLoading = ref(false);
    
    // 从数据库查询数据
    const loadQueryResults = async () => {
      isLoading.value = true;
      
      try {
        console.log('开始查询土壤数据，条件:', queryParams);
        
        // 构建查询过滤条件
        const filters = {};
        
        if (queryParams.region !== '全国') {
          // 这里应该根据实际的区域映射逻辑来处理
          filters.province = queryParams.region.replace('地区', '');
        }
        
        if (queryParams.startDate) {
          filters.dateStart = queryParams.startDate;
        }
        
        if (queryParams.endDate) {
          filters.dateEnd = queryParams.endDate;
        }
        
        if (queryParams.minValue) {
          // 根据选择的养分类型设置最小值
          if (queryParams.nutrient === 'nitrogen') {
            filters.nitrogenMin = parseFloat(queryParams.minValue);
          } else if (queryParams.nutrient === 'phosphorus') {
            filters.phosphorusMin = parseFloat(queryParams.minValue);
          } else if (queryParams.nutrient === 'potassium') {
            filters.potassiumMin = parseFloat(queryParams.minValue);
          } else if (queryParams.nutrient === 'ph') {
            filters.phMin = parseFloat(queryParams.minValue);
          }
        }
        
        if (queryParams.maxValue) {
          // 根据选择的养分类型设置最大值
          if (queryParams.nutrient === 'nitrogen') {
            filters.nitrogenMax = parseFloat(queryParams.maxValue);
          } else if (queryParams.nutrient === 'phosphorus') {
            filters.phosphorusMax = parseFloat(queryParams.maxValue);
          } else if (queryParams.nutrient === 'potassium') {
            filters.potassiumMax = parseFloat(queryParams.maxValue);
          } else if (queryParams.nutrient === 'ph') {
            filters.phMax = parseFloat(queryParams.maxValue);
          }
        }
        
        // 调用API获取数据
        const result = await soilDataAPI.getSoilDataTable(queryParams.page, queryParams.pageSize, filters);
        
        // 处理数据并添加状态信息
        queryResults.value = result.data.map(item => ({
          id: item.id,
          time: item.time,
          region: item.location.split('市')[0] + '市',
          location: item.location,
          nitrogen: item.nitrogen,
          phosphorus: item.phosphorus,
          potassium: item.potassium,
          organic: item.organic,
          ph: item.ph,
          soilType: item.texture,
          status: getSoilStatus(item),
          statusColor: getSoilStatusColor(item)
        }));
        
        totalResults.value = result.total;
        totalPages.value = result.totalPages;
        
        console.log('查询完成，共', totalResults.value, '条结果');
        
      } catch (error) {
        console.error('查询土壤数据失败:', error);
        
        // 使用模拟数据作为后备方案
        const mockResults = [
          {
            id: 'SOIL001',
            time: '2024-01-15',
            region: '北京市',
            location: '北京市海淀区',
            nitrogen: 85,
            phosphorus: 45,
            potassium: 120,
            organic: 2.3,
            ph: 6.8,
            soilType: '砂壤土',
            status: '良好',
            statusColor: '#4d7bce'
          },
          {
            id: 'SOIL002',
            time: '2024-01-14',
            region: '上海市',
            location: '上海市浦东新区',
            nitrogen: 120,
            phosphorus: 60,
            potassium: 95,
            organic: 3.1,
            ph: 7.2,
            soilType: '粘土',
            status: '优秀',
            statusColor: '#1dd1a1'
          }
        ];
        
        queryResults.value = mockResults;
        totalResults.value = mockResults.length;
        totalPages.value = 1;
      } finally {
        isLoading.value = false;
      }
    };
    
    // 获取土壤状态
    const getSoilStatus = (soilData) => {
      const ph = parseFloat(soilData.ph);
      const nitrogen = parseFloat(soilData.nitrogen);
      const phosphorus = parseFloat(soilData.phosphorus);
      const potassium = parseFloat(soilData.potassium);
      
      // 简单的评价逻辑
      let score = 0;
      
      // pH评分 (6.5-7.5为最佳)
      if (ph >= 6.5 && ph <= 7.5) score += 25;
      else if (ph >= 5.5 && ph <= 8.0) score += 15;
      else score += 5;
      
      // 氮含量评分
      if (nitrogen >= 80) score += 25;
      else if (nitrogen >= 50) score += 15;
      else score += 5;
      
      // 磷含量评分
      if (phosphorus >= 50) score += 25;
      else if (phosphorus >= 30) score += 15;
      else score += 5;
      
      // 钾含量评分
      if (potassium >= 100) score += 25;
      else if (potassium >= 70) score += 15;
      else score += 5;
      
      // 根据总分返回状态
      if (score >= 85) return '优秀';
      else if (score >= 70) return '良好';
      else if (score >= 55) return '一般';
      else if (score >= 40) return '注意';
      else return '警告';
    };
    
    // 获取土壤状态颜色
    const getSoilStatusColor = (soilData) => {
      const status = getSoilStatus(soilData);
      const colorMap = {
        '优秀': '#1dd1a1',
        '良好': '#4d7bce',
        '一般': '#feca57',
        '注意': '#ff9f43',
        '警告': '#ff6b6b'
      };
      return colorMap[status] || '#666666';
    };
    
    // 执行查询
    const executeQuery = () => {
      queryParams.page = 1;
      loadQueryResults();
    };
    
    // 分页处理
    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        queryParams.page = page;
        loadQueryResults();
      }
    };
    
    // 改变排序
    const changeSort = (sortField) => {
      if (queryParams.sortBy === sortField) {
        queryParams.sortOrder = queryParams.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        queryParams.sortBy = sortField;
        queryParams.sortOrder = 'desc';
      }
      loadQueryResults();
    };
    
    // 导出结果
    const exportResults = (format) => {
      // 实际应用中应调用后端API导出数据
      uni.showToast({
        title: `已导出为${format}格式`,
        icon: 'success'
      });
    };
    
    // 查看详情
    const viewDetails = (id) => {
      // 实际应用中应跳转到详情页
      uni.showToast({
        title: `查看ID:${id}的详情`,
        icon: 'none'
      });
    };
    
    // 随机日期生成
    const randomDate = (start, end) => {
      const startDate = new Date(start).getTime();
      const endDate = new Date(end).getTime();
      const randomTime = startDate + Math.random() * (endDate - startDate);
      const date = new Date(randomTime);
      
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      
      return `${year}-${month}-${day}`;
    };
    
    onMounted(() => {
      // 页面加载后自动执行一次查询
      loadQueryResults();
    });
    
    return {
      queryParams,
      queryResults,
      totalResults,
      totalPages,
      isLoading,
      executeQuery,
      goToPage,
      changeSort,
      exportResults,
      viewDetails
    };
  }
};
</script>

<template>
  <view class="page-container" id="query-page">
    <view class="page-header">
      <text class="header-title">土壤数据信息查询</text>
    </view>
    
    <view class="query-panel">
      <view class="panel-header">
        <text class="panel-title">查询条件</text>
      </view>
      
      <view class="query-form">
        <view class="form-row">
          <view class="form-group">
            <text class="form-label">地区范围</text>
            <picker :range="['全国', '华北地区', '东北地区', '华东地区', '中南地区', '西南地区', '西北地区']" 
                    @change="(e) => queryParams.region = e.target.value">
              <view class="picker-view">{{ queryParams.region }}</view>
            </picker>
          </view>
          
          <view class="form-group">
            <text class="form-label">土壤类型</text>
            <picker :range="['全部', '砂质土', '壤土', '砂壤土', '粘壤土', '黑土']" 
                    @change="(e) => queryParams.soilType = e.target.value">
              <view class="picker-view">{{ queryParams.soilType }}</view>
            </picker>
          </view>
          
          <view class="form-group">
            <text class="form-label">养分指标</text>
            <picker :range="['全部', '氮含量', '磷含量', '钾含量', '有机质', 'pH值']" 
                    @change="(e) => queryParams.nutrient = e.target.value">
              <view class="picker-view">{{ queryParams.nutrient }}</view>
            </picker>
          </view>
        </view>
        
        <view class="form-row">
          <view class="form-group">
            <text class="form-label">起始日期</text>
            <picker mode="date" :value="queryParams.startDate" 
                    @change="(e) => queryParams.startDate = e.target.value">
              <view class="picker-view">{{ queryParams.startDate }}</view>
            </picker>
          </view>
          
          <view class="form-group">
            <text class="form-label">结束日期</text>
            <picker mode="date" :value="queryParams.endDate" 
                    @change="(e) => queryParams.endDate = e.target.value">
              <view class="picker-view">{{ queryParams.endDate }}</view>
            </picker>
          </view>
          
          <view class="form-group range-group">
            <text class="form-label">数值范围</text>
            <view class="range-inputs">
              <input type="text" placeholder="最小值" v-model="queryParams.minValue" />
              <text class="range-separator">-</text>
              <input type="text" placeholder="最大值" v-model="queryParams.maxValue" />
            </view>
          </view>
        </view>
        
        <view class="form-actions">
          <button class="btn" type="default" @click="queryParams = {
            region: '全国',
            startDate: '2022-01-01',
            endDate: '2023-10-31',
            nutrient: '全部',
            minValue: '',
            maxValue: '',
            soilType: '全部',
            sortBy: 'time',
            sortOrder: 'desc',
            page: 1,
            pageSize: 10
          }">重置条件</button>
          <button class="btn" type="primary" @click="executeQuery">查询数据</button>
        </view>
      </view>
    </view>
    
    <view class="results-panel">
      <view class="panel-header">
        <text class="panel-title">查询结果 (共{{ totalResults }}条记录)</text>
        <view class="panel-actions">
          <button class="btn btn-sm" @click="exportResults('Excel')">导出Excel</button>
          <button class="btn btn-sm" @click="exportResults('CSV')">导出CSV</button>
        </view>
      </view>
      
      <view class="results-table-wrapper">
        <view class="loading-indicator" v-if="isLoading">
          <text>数据加载中...</text>
        </view>
        
        <scroll-view class="results-table-container" scroll-x="true" v-else>
          <view class="results-table">
            <view class="table-header">
              <view class="th" @click="changeSort('id')">
                <text>样本ID</text>
                <text class="sort-indicator" v-if="queryParams.sortBy === 'id'">
                  {{ queryParams.sortOrder === 'asc' ? '↑' : '↓' }}
                </text>
              </view>
              <view class="th" @click="changeSort('time')">
                <text>采样时间</text>
                <text class="sort-indicator" v-if="queryParams.sortBy === 'time'">
                  {{ queryParams.sortOrder === 'asc' ? '↑' : '↓' }}
                </text>
              </view>
              <view class="th">
                <text>采样地点</text>
              </view>
              <view class="th" @click="changeSort('nitrogen')">
                <text>氮含量</text>
                <text class="sort-indicator" v-if="queryParams.sortBy === 'nitrogen'">
                  {{ queryParams.sortOrder === 'asc' ? '↑' : '↓' }}
                </text>
              </view>
              <view class="th">
                <text>磷含量</text>
              </view>
              <view class="th">
                <text>钾含量</text>
              </view>
              <view class="th">
                <text>有机质</text>
              </view>
              <view class="th" @click="changeSort('ph')">
                <text>pH值</text>
                <text class="sort-indicator" v-if="queryParams.sortBy === 'ph'">
                  {{ queryParams.sortOrder === 'asc' ? '↑' : '↓' }}
                </text>
              </view>
              <view class="th">
                <text>土壤类型</text>
              </view>
              <view class="th">
                <text>状态</text>
              </view>
              <view class="th">
                <text>操作</text>
              </view>
            </view>
            
            <view class="table-body">
              <view class="tr" v-for="result in queryResults" :key="result.id">
                <view class="td">{{ result.id }}</view>
                <view class="td">{{ result.time }}</view>
                <view class="td">{{ result.location }}</view>
                <view class="td">{{ result.nitrogen }}</view>
                <view class="td">{{ result.phosphorus }}</view>
                <view class="td">{{ result.potassium }}</view>
                <view class="td">{{ result.organic }}</view>
                <view class="td">{{ result.ph }}</view>
                <view class="td">{{ result.soilType }}</view>
                <view class="td">
                  <view class="status-badge" :style="{ backgroundColor: result.statusColor + '20', color: result.statusColor }">
                    {{ result.status }}
                  </view>
                </view>
                <view class="td">
                  <button class="action-btn" @click="viewDetails(result.id)">查看</button>
                </view>
              </view>
              
              <view class="empty-results" v-if="queryResults.length === 0">
                <text>暂无符合条件的数据</text>
              </view>
            </view>
          </view>
        </scroll-view>
        
        <view class="pagination">
          <button class="page-btn" :disabled="queryParams.page === 1" @click="goToPage(1)">首页</button>
          <button class="page-btn" :disabled="queryParams.page === 1" @click="goToPage(queryParams.page - 1)">上一页</button>
          <text class="page-info">第 {{ queryParams.page }} 页，共 {{ totalPages }} 页</text>
          <button class="page-btn" :disabled="queryParams.page === totalPages" @click="goToPage(queryParams.page + 1)">下一页</button>
          <button class="page-btn" :disabled="queryParams.page === totalPages" @click="goToPage(totalPages)">末页</button>
        </view>
      </view>
    </view>
    
    <view class="advanced-features">
      <view class="feature-section">
        <view class="section-header">
          <text class="section-title">数据分析工具</text>
        </view>
        
        <view class="tool-cards">
          <view class="tool-card">
            <view class="tool-icon">图</view>
            <view class="tool-content">
              <text class="tool-title">查询结果可视化</text>
              <text class="tool-desc">将查询结果转换为直观的图表，支持柱状图、折线图、饼图等多种图表类型</text>
              <button class="tool-btn">开始分析</button>
            </view>
          </view>
          
          <view class="tool-card">
            <view class="tool-icon">比</view>
            <view class="tool-content">
              <text class="tool-title">历史数据对比</text>
              <text class="tool-desc">将当前查询结果与历史数据进行对比，发现变化趋势和异常点</text>
              <button class="tool-btn">开始对比</button>
            </view>
          </view>
          
          <view class="tool-card">
            <view class="tool-icon">报</view>
            <view class="tool-content">
              <text class="tool-title">生成分析报告</text>
              <text class="tool-desc">基于查询结果自动生成专业的土壤数据分析报告，包含评估和建议</text>
              <button class="tool-btn">生成报告</button>
            </view>
          </view>
        </view>
      </view>
      
      <view class="feature-section">
        <view class="section-header">
          <text class="section-title">常用查询模板</text>
        </view>
        
        <view class="query-templates">
          <view class="template-item" @click="queryParams.region = '华北地区'; queryParams.nutrient = '氮含量'; executeQuery()">
            <text class="template-name">华北地区氮含量分析</text>
          </view>
          <view class="template-item" @click="queryParams.soilType = '黑土'; executeQuery()">
            <text class="template-name">黑土地区土壤养分全面分析</text>
          </view>
          <view class="template-item" @click="queryParams.minValue = '80'; queryParams.nutrient = '钾含量'; executeQuery()">
            <text class="template-name">高钾含量土壤分布查询</text>
          </view>
          <view class="template-item" @click="queryParams.startDate = '2023-01-01'; queryParams.endDate = '2023-10-31'; executeQuery()">
            <text class="template-name">2023年全国土壤状况概览</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<style>
.page-header {
  padding: 20px;
  background-color: white;
  border-bottom: 1px solid #eee;
}

.header-title {
  font-size: 18px;
  font-weight: bold;
}

.query-panel, .results-panel, .advanced-features {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin: 15px;
  overflow: hidden;
}

.panel-header, .section-header {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-title, .section-title {
  font-size: 16px;
  font-weight: bold;
}

.panel-actions {
  display: flex;
  gap: 10px;
}

.query-form {
  padding: 15px;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 15px;
}

.form-group {
  flex: 1;
  min-width: 180px;
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 14px;
  color: #555;
  margin-bottom: 5px;
}

.picker-view {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f8f8f8;
}

.range-group {
  min-width: 250px;
}

.range-inputs {
  display: flex;
  align-items: center;
}

.range-inputs input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f8f8f8;
}

.range-separator {
  padding: 0 10px;
  color: #999;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

.btn {
  padding: 8px 20px;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 14px;
}

.results-table-wrapper {
  padding: 15px;
}

.loading-indicator {
  padding: 30px;
  text-align: center;
  color: #999;
}

.results-table-container {
  width: 100%;
  overflow-x: auto;
}

.results-table {
  width: 100%;
  border-collapse: collapse;
}

.table-header {
  display: flex;
  background-color: #f5f7fa;
  font-weight: bold;
}

.table-body {
  display: flex;
  flex-direction: column;
}

.tr {
  display: flex;
  border-bottom: 1px solid #eee;
}

.th, .td {
  padding: 12px 15px;
  text-align: left;
  min-width: 120px;
  flex: 1;
}

.th {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.sort-indicator {
  margin-left: 5px;
  color: #4d7bce;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  text-align: center;
}

.action-btn {
  padding: 4px 10px;
  font-size: 12px;
  border-radius: 4px;
  background-color: #4d7bce;
  color: white;
}

.empty-results {
  padding: 30px;
  text-align: center;
  color: #999;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 15px;
  gap: 10px;
}

.page-btn {
  padding: 6px 12px;
  font-size: 14px;
}

.page-info {
  color: #666;
}

.feature-section {
  border-top: 1px solid #f0f0f0;
}

.tool-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding: 15px;
}

.tool-card {
  flex: 1;
  min-width: 250px;
  display: flex;
  align-items: flex-start;
  background-color: #f9f9f9;
  border-radius: 4px;
  padding: 15px;
}

.tool-icon {
  width: 40px;
  height: 40px;
  background-color: #4d7bce;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  margin-right: 15px;
}

.tool-content {
  flex: 1;
}

.tool-title {
  font-weight: bold;
  font-size: 15px;
  margin-bottom: 5px;
  display: block;
}

.tool-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.4;
  margin-bottom: 10px;
  display: block;
}

.tool-btn {
  font-size: 14px;
  padding: 6px 12px;
}

.query-templates {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding: 15px;
}

.template-item {
  flex: 1;
  min-width: 200px;
  padding: 12px 15px;
  background-color: #f0f7ff;
  border-radius: 4px;
  border-left: 3px solid #4d7bce;
  cursor: pointer;
  transition: background-color 0.2s;
}

.template-item:hover {
  background-color: #e6f2ff;
}

.template-name {
  font-size: 14px;
  color: #333;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .form-group {
    flex: 100%;
  }
  
  .tool-card {
    flex: 100%;
  }
  
  .template-item {
    flex: 100%;
  }
}
</style> 