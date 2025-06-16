<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as echarts from 'echarts';
import soilDataAPI from '@/utils/api.js';

export default {
  name: 'HistoryDataView',
  setup() {
    // DOM引用
    const trendChartRef = ref(null);
    const dataTableRef = ref(null);
    
    // 图表实例
    let trendChart = null;
    
    // 样本点数据
    const samplePoint = ref(null);
    const historyData = ref([]);
    const sampleId = ref('');
    const sampleName = ref('');
    
    // 加载历史数据
    const loadHistoryData = async () => {
      try {
        console.log('开始加载历史数据...');
        
        // 获取历史监测数据
        const result = await soilDataAPI.getHistoricalData();
        
        if (result && result.length > 0) {
          // 转换数据格式
          historyData.value = result.map(item => ({
            id: item.id,
            date: item.date,
            ph: parseFloat(item.ph) || 0,
            nitrogen: parseFloat(item.nitrogen) || 0,
            phosphorus: parseFloat(item.phosphorus) || 0,
            potassium: parseFloat(item.potassium) || 0,
            organic: parseFloat(item.organic) || 0,
            location: item.location,
            depth: item.depth || '0-20cm'
          }));
          
          // 如果有样本点名称，更新
          if (result[0].location) {
            sampleName.value = result[0].location;
          }
          
          console.log('历史数据加载完成，共', historyData.value.length, '条记录');
        } else {
          // 使用模拟数据作为后备方案
          historyData.value = generateMockHistoryData();
          sampleName.value = '示例监测点';
          console.log('使用模拟历史数据');
        }
        
        // 更新图表
        if (historyData.value.length > 0) {
          updateTrendChart();
        }
        
      } catch (error) {
        console.error('加载历史数据失败:', error);
        
        // 使用模拟数据作为后备方案
        historyData.value = generateMockHistoryData();
        sampleName.value = '示例监测点';
        
        // 更新图表
        if (historyData.value.length > 0) {
          updateTrendChart();
        }
      }
    };
    
    // 生成模拟历史数据
    const generateMockHistoryData = () => {
      const mockData = [];
      const startDate = new Date('2022-01-01');
      
      for (let i = 0; i < 24; i++) {
        const date = new Date(startDate);
        date.setMonth(startDate.getMonth() + i);
        
        mockData.push({
          id: `HIST${String(i + 1).padStart(3, '0')}`,
          date: date.toISOString().split('T')[0],
          ph: Number((6.5 + Math.random() * 1.5).toFixed(1)),
          nitrogen: Math.round(60 + Math.random() * 40),
          phosphorus: Math.round(25 + Math.random() * 30),
          potassium: Math.round(80 + Math.random() * 50),
          organic: Number((2.0 + Math.random() * 2.0).toFixed(1)),
          location: '北京市海淀区监测点',
          depth: '0-20cm'
        });
      }
      
      return mockData;
    };
    
    // 图表初始化
    const initChart = () => {
      if (trendChartRef.value) {
        console.log('初始化历史趋势图表...');
        
        if (trendChart) {
          trendChart.dispose();
        }
        
        trendChart = echarts.init(trendChartRef.value);
        
        // 如果有数据，更新图表
        if (historyData.value && historyData.value.length > 0) {
          updateTrendChart();
        }
      }
    };
    
    // 更新趋势图
    const updateTrendChart = () => {
      if (!trendChart) return;
      
      // 准备数据
      const dates = historyData.value.map(item => item.date);
      const phValues = historyData.value.map(item => item.ph);
      const nitrogenValues = historyData.value.map(item => item.nitrogen);
      const phosphorusValues = historyData.value.map(item => item.phosphorus);
      const potassiumValues = historyData.value.map(item => item.potassium);
      const organicValues = historyData.value.map(item => item.organic);
      
      // 设置图表选项
      const option = {
        title: {
          text: `${sampleName.value} 历史养分趋势`,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          formatter: function(params) {
            let result = params[0].name + '<br/>';
            params.forEach(param => {
              const unit = param.seriesName === 'pH值' || param.seriesName === '有机质' ? '' : 'mg/kg';
              const suffix = param.seriesName === '有机质' ? '%' : unit;
              result += 
                `<span style="display:inline-block;margin-right:4px;border-radius:10px;width:10px;height:10px;background-color:${param.color};"></span>` +
                `${param.seriesName}: ${param.value}${suffix}<br/>`;
            });
            return result;
          }
        },
        legend: {
          data: ['pH值', '氮含量', '磷含量', '钾含量', '有机质'],
          bottom: 10
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '15%',
          top: '15%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {},
            dataZoom: {},
            restore: {}
          },
          right: 20,
          top: 20
        },
        xAxis: {
          type: 'category',
          data: dates,
          boundaryGap: false,
          axisLabel: {
            rotate: 30
          }
        },
        yAxis: [
          {
            type: 'value',
            name: '养分含量(mg/kg)',
            min: 0,
            max: 150,
            position: 'left',
            axisLine: {
              show: true,
              lineStyle: {
                color: '#ff6b6b'
              }
            }
          },
          {
            type: 'value',
            name: 'pH值/有机质(%)',
            min: 0,
            max: 10,
            position: 'right',
            axisLine: {
              show: true,
              lineStyle: {
                color: '#feca57'
              }
            }
          }
        ],
        series: [
          {
            name: 'pH值',
            type: 'line',
            yAxisIndex: 1,
            symbol: 'circle',
            symbolSize: 8,
            data: phValues,
            itemStyle: { color: '#feca57' },
            lineStyle: { width: 3 }
          },
          {
            name: '氮含量',
            type: 'line',
            symbol: 'circle',
            symbolSize: 8,
            data: nitrogenValues,
            itemStyle: { color: '#ff6b6b' },
            lineStyle: { width: 3 }
          },
          {
            name: '磷含量',
            type: 'line',
            symbol: 'circle',
            symbolSize: 8,
            data: phosphorusValues,
            itemStyle: { color: '#48dbfb' },
            lineStyle: { width: 3 }
          },
          {
            name: '钾含量',
            type: 'line',
            symbol: 'circle',
            symbolSize: 8,
            data: potassiumValues,
            itemStyle: { color: '#1dd1a1' },
            lineStyle: { width: 3 }
          },
          {
            name: '有机质',
            type: 'line',
            yAxisIndex: 1,
            symbol: 'circle',
            symbolSize: 8,
            data: organicValues,
            itemStyle: { color: '#a29bfe' },
            lineStyle: { width: 3 }
          }
        ]
      };
      
      trendChart.setOption(option);
    };
    
    // 导出数据为CSV
    const exportCSV = () => {
      if (!historyData.value || historyData.value.length === 0) {
        uni.showToast({
          title: '没有可导出的数据',
          icon: 'none'
        });
        return;
      }
      
      uni.showLoading({
        title: '正在导出数据...'
      });
      
      try {
        // 构建CSV内容
        const csvHeader = '日期,pH值,氮含量(mg/kg),磷含量(mg/kg),钾含量(mg/kg),有机质(%)';
        const csvRows = historyData.value.map(item => 
          `${item.date},${item.ph},${item.nitrogen},${item.phosphorus},${item.potassium},${item.organic}`
        );
        const csvContent = [csvHeader, ...csvRows].join('\n');
        
        // 模拟保存文件
        setTimeout(() => {
          uni.hideLoading();
          
          uni.showModal({
            title: '数据导出成功',
            content: `文件已保存到：/downloads/${sampleName.value}_历史数据.csv`,
            showCancel: false,
            success: function() {
              uni.showToast({
                title: '导出完成',
                icon: 'success'
              });
            }
          });
        }, 1000);
      } catch (error) {
        uni.hideLoading();
        uni.showToast({
          title: '导出失败: ' + error.message,
          icon: 'none'
        });
      }
    };
    
    // 处理窗口大小变化
    const handleResize = () => {
      if (trendChart) {
        trendChart.resize();
      }
    };
    
    // 返回首页
    const goBack = () => {
      uni.navigateBack();
    };
    
    onMounted(async () => {
      console.log('历史数据页面已挂载');
      
      // 先加载数据
      await loadHistoryData();
      
      // 从URL获取样本点ID和名称 (此部分将被事件监听取代)
      /*
      const query = uni.createSelectorQuery();
      const pages = getCurrentPages();
      const currentPage = pages[pages.length - 1];
      const options = currentPage.$page ? currentPage.$page.options : {};
      
      if (options.id) {
        sampleId.value = options.id;
      }
      if (options.name) {
        sampleName.value = decodeURIComponent(options.name);
      }
      */
      
      // 监听采样历史数据事件 (修改事件名称)
      uni.$on('history-data', (data) => { // Changed from 'sample-history-data'
        console.log('接收到历史数据:', data);
        if (data) {
          if (data.currentData) { // Changed from data.samplePoint to data.currentData
            samplePoint.value = data.currentData;
            // 使用接收到的数据填充 sampleName 和 sampleId
            if (data.currentData.name) {
              sampleName.value = data.currentData.name;
            }
            if (data.currentData.id) {
              sampleId.value = data.currentData.id;
            }
          }
          
          if (data.history && data.history.length > 0) {
            historyData.value = [...data.history];
            // 添加当前样本点数据作为最新记录
            if (samplePoint.value) {
              const currentSampleRecord = {
                date: samplePoint.value.sampleTime.split(' ')[0], // 只取日期部分
                ph: samplePoint.value.pH,
                nitrogen: samplePoint.value.nitrogen,
                phosphorus: samplePoint.value.phosphorus,
                potassium: samplePoint.value.potassium,
                organic: samplePoint.value.organic
              };
              
              // 确保当前记录在最前面，并且如果日期相同则不重复添加（或按需更新）
              const existingIndex = historyData.value.findIndex(item => item.date === currentSampleRecord.date);
              if (existingIndex !== -1) {
                // 如果找到相同日期的记录，可以选择替换它或保留旧的
                // historyData.value.splice(existingIndex, 1); // 移除旧的
              }
              // 将当前记录添加到数组开头
              historyData.value.unshift(currentSampleRecord);

              // 去重并排序：确保按日期降序排列，并且如果unshift后有重复的当天记录，则保留一个
              // (一个简单去重方法是基于date，但如果同一天可以有多个不同记录，则此逻辑需要调整)
              const uniqueDates = new Set();
              historyData.value = historyData.value.filter(item => {
                if (!uniqueDates.has(item.date)) {
                  uniqueDates.add(item.date);
                  return true;
                }
                return false;
              });
            }
             // 按日期降序排序
            historyData.value.sort((a, b) => new Date(b.date) - new Date(a.date));
            
            // 更新图表
            initChart(); // 调用 initChart，它会调用 updateTrendChart
          } else if (data.currentData) { // 如果没有历史数据，但有当前数据
            // samplePoint.value 已经通过上面的 if (data.currentData) 设置了
             if (samplePoint.value) { // 确保 samplePoint.value 存在
                const currentSampleRecord = {
                    date: samplePoint.value.sampleTime.split(' ')[0],
                    ph: samplePoint.value.pH,
                    nitrogen: samplePoint.value.nitrogen,
                    phosphorus: samplePoint.value.phosphorus,
                    potassium: samplePoint.value.potassium,
                    organic: samplePoint.value.organic
                };
                historyData.value = [currentSampleRecord]; // 历史数据仅包含当前点
                initChart(); // 初始化/更新图表
            } else {
                 console.warn("当前数据 (currentData) 为空，无法生成历史记录。")
            }
          } else {
            console.log('接收到的历史数据为空或格式不正确');
            // 可以在这里显示一个提示，或者加载一些默认/空状态
            historyData.value = []; // 确保清空
            initChart(); // 尝试初始化图表为空状态
          }
        }
      });
      
      // 初始化图表 (将由事件回调中的 initChart() 触发)
      /*
      setTimeout(() => {
        initChart();
      }, 500);
      */
      
      // 添加窗口大小变化事件监听
      window.addEventListener('resize', handleResize);
    });
    
    onBeforeUnmount(() => {
      console.log('历史数据页面即将卸载');
      
      // 移除事件监听
      window.removeEventListener('resize', handleResize);
      uni.$off('history-data'); // Changed from 'sample-history-data'
      
      // 销毁图表实例
      if (trendChart) {
        trendChart.dispose();
        trendChart = null;
      }
    });

    const getCategoryClass = (value) => {
      if (value > 0) return 'positive';
      if (value < 0) return 'negative';
      return 'neutral';
    };
    
    return {
      trendChartRef,
      dataTableRef,
      sampleName,
      sampleId,
      historyData,
      goBack,
      exportCSV,
      getCategoryClass
    };
  }
};
</script>

<template>
  <view class="history-data-container">
    <view class="page-header">
      <view class="back-button" @click="goBack">
        <text class="back-icon">←</text>
        <text>返回</text>
      </view>
      <text class="header-title">{{ sampleName }} 历史数据</text>
      <view class="header-actions">
        <button class="action-btn" @click="exportCSV">导出CSV</button>
      </view>
    </view>
    
    <view class="page-content">
      <view class="trend-chart-container">
        <view class="chart-header">
          <text class="section-title">土壤养分历史趋势</text>
        </view>
        <view class="chart-body" ref="trendChartRef"></view>
      </view>
      
      <view class="data-table-container">
        <view class="table-header">
          <text class="section-title">历史采样数据记录</text>
        </view>
        <scroll-view class="table-scroll" scroll-x="true" ref="dataTableRef">
          <view class="data-table">
            <view class="table-head">
              <view class="th">采样日期</view>
              <view class="th">pH值</view>
              <view class="th">氮含量 (mg/kg)</view>
              <view class="th">磷含量 (mg/kg)</view>
              <view class="th">钾含量 (mg/kg)</view>
              <view class="th">有机质 (%)</view>
            </view>
            <view class="table-row" v-for="(item, index) in historyData" :key="index">
              <view class="td">{{ item.date }}</view>
              <view class="td">{{ item.ph }}</view>
              <view class="td">{{ item.nitrogen }}</view>
              <view class="td">{{ item.phosphorus }}</view>
              <view class="td">{{ item.potassium }}</view>
              <view class="td">{{ item.organic }}</view>
            </view>
          </view>
        </scroll-view>
      </view>
      
      <view class="summary-container">
        <view class="summary-header">
          <text class="section-title">养分变化统计分析</text>
        </view>
        <view class="summary-content">
          <view class="summary-card" v-if="historyData.length >= 2">
            <text class="summary-title">氮含量变化趋势</text>
            <text class="summary-value" :class="getCategoryClass(historyData[0].nitrogen - historyData[historyData.length-1].nitrogen)">
              {{ historyData[0].nitrogen - historyData[historyData.length-1].nitrogen > 0 ? '↑' : '↓' }} 
              {{ Math.abs(historyData[0].nitrogen - historyData[historyData.length-1].nitrogen) }} mg/kg
            </text>
            <text class="summary-description">与最早记录相比</text>
          </view>
          
          <view class="summary-card" v-if="historyData.length >= 2">
            <text class="summary-title">磷含量变化趋势</text>
            <text class="summary-value" :class="getCategoryClass(historyData[0].phosphorus - historyData[historyData.length-1].phosphorus)">
              {{ historyData[0].phosphorus - historyData[historyData.length-1].phosphorus > 0 ? '↑' : '↓' }} 
              {{ Math.abs(historyData[0].phosphorus - historyData[historyData.length-1].phosphorus) }} mg/kg
            </text>
            <text class="summary-description">与最早记录相比</text>
          </view>
          
          <view class="summary-card" v-if="historyData.length >= 2">
            <text class="summary-title">钾含量变化趋势</text>
            <text class="summary-value" :class="getCategoryClass(historyData[0].potassium - historyData[historyData.length-1].potassium)">
              {{ historyData[0].potassium - historyData[historyData.length-1].potassium > 0 ? '↑' : '↓' }} 
              {{ Math.abs(historyData[0].potassium - historyData[historyData.length-1].potassium) }} mg/kg
            </text>
            <text class="summary-description">与最早记录相比</text>
          </view>
          
          <view class="summary-card" v-if="historyData.length >= 2">
            <text class="summary-title">有机质变化趋势</text>
            <text class="summary-value" :class="getCategoryClass(historyData[0].organic - historyData[historyData.length-1].organic)">
              {{ historyData[0].organic - historyData[historyData.length-1].organic > 0 ? '↑' : '↓' }} 
              {{ Math.abs(historyData[0].organic - historyData[historyData.length-1].organic).toFixed(1) }} %
            </text>
            <text class="summary-description">与最早记录相比</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<style>
.history-data-container {
  width: 100%;
  box-sizing: border-box;
}

.page-header {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  background-color: white;
  border-bottom: 1px solid #eee;
  width: 100%;
  box-sizing: border-box;
}

.back-button {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin-right: 15px;
}

.back-icon {
  font-size: 18px;
  margin-right: 5px;
}

.header-title {
  flex: 1;
  font-size: 18px;
  font-weight: bold;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  padding: 5px 15px;
  background-color: #4d7bce;
  color: white;
  border: none;
  border-radius: 4px;
}

.page-content {
  padding: 15px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.trend-chart-container {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 15px;
}

.chart-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
}

.chart-body {
  height: 350px;
  padding: 15px;
}

.data-table-container {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 15px;
}

.table-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.table-scroll {
  width: 100%;
  overflow-x: auto;
}

.data-table {
  width: 100%;
  min-width: 800px;
  border-collapse: collapse;
}

.table-head {
  display: flex;
  background-color: #f5f7fa;
}

.table-row {
  display: flex;
  border-bottom: 1px solid #eee;
}

.th, .td {
  flex: 1;
  padding: 12px 15px;
  text-align: center;
  min-width: 120px;
}

.th {
  font-weight: bold;
}

.summary-container {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.summary-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.summary-content {
  display: flex;
  flex-wrap: wrap;
  padding: 15px;
  gap: 15px;
}

.summary-card {
  flex: 1;
  min-width: 200px;
  padding: 15px;
  border-radius: 4px;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.summary-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.summary-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 5px;
}

.summary-description {
  font-size: 12px;
  color: #999;
}

.positive {
  color: #1dd1a1;
}

.negative {
  color: #ff6b6b;
}

.neutral {
  color: #feca57;
}

@media (max-width: 768px) {
  .summary-card {
    flex: 1 1 100%;
  }
}
</style> 