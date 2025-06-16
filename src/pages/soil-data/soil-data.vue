<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
// 直接引入echarts
import * as echarts from 'echarts';
import * as XLSX from 'xlsx'; // 导入xlsx
import soilDataAPI from '@/utils/api.js';

export default {
  name: 'SoilDataView',
  setup() {
    const currentPage = ref(1);
    const totalPages = ref(10);
    
    // 定义图表实例引用
    let regionChart = null;
    let phChart = null;
    let trendChart = null;
    let textureChart = null;
    
    // 检查环境
    const checkEnvironment = () => {
      console.log('当前环境检查:');
      console.log('- window对象:', typeof window !== 'undefined');
      console.log('- document对象:', typeof document !== 'undefined');
      console.log('- uni对象:', typeof uni !== 'undefined');
      console.log('- echarts对象:', typeof echarts !== 'undefined');
      
      if (typeof window !== 'undefined' && !window.echarts) {
        console.log('将echarts挂载到window对象');
        window.echarts = echarts;
      }
    };
    
    // 土壤数据（从数据库加载）
    const mockSoilData = ref([]);
    
    // 图表数据
    const regionNutrientData = ref([]);
    const phDistributionData = ref([]);
    const soilTextureData = ref([]);
    const nutrientTrendData = ref([]);
    
    // 加载土壤数据表格
    const loadSoilDataTable = async () => {
      try {
        console.log('开始加载土壤数据表格...');
        const result = await soilDataAPI.getSoilDataTable(currentPage.value, 10);
        mockSoilData.value = result.data;
        totalPages.value = result.totalPages;
        console.log('土壤数据表格加载完成，共', result.total, '条数据');
      } catch (error) {
        console.error('加载土壤数据表格失败:', error);
        // 使用模拟数据作为后备方案
        mockSoilData.value = [
          { id: 'BJ001', time: '2024-01-15', location: '北京市海淀区', ph: 6.8, nitrogen: 85, phosphorus: 45, potassium: 120, organic: 2.3, texture: '砂壤土' },
          { id: 'SH001', time: '2024-01-14', location: '上海市浦东新区', ph: 7.2, nitrogen: 65, phosphorus: 55, potassium: 90, organic: 1.8, texture: '壤土' },
          { id: 'CD001', time: '2024-01-13', location: '成都市武侯区', ph: 6.5, nitrogen: 75, phosphorus: 35, potassium: 110, organic: 2.1, texture: '粘壤土' },
          { id: 'HRB001', time: '2024-01-12', location: '哈尔滨市道里区', ph: 5.9, nitrogen: 45, phosphorus: 25, potassium: 80, organic: 3.2, texture: '黑土' },
          { id: 'GZ001', time: '2024-01-11', location: '广州市天河区', ph: 7.5, nitrogen: 95, phosphorus: 65, potassium: 130, organic: 1.5, texture: '砂质土' }
        ];
      }
    };
    
    // 加载图表数据
    const loadChartData = async () => {
      try {
        console.log('开始加载图表数据...');
        const [regionData, phData, textureData, trendData] = await Promise.all([
          soilDataAPI.getRegionNutrientStats(),
          soilDataAPI.getPhDistributionStats(),
          soilDataAPI.getSoilTextureStats(),
          soilDataAPI.getNutrientTrendData()
        ]);
        
        regionNutrientData.value = regionData;
        phDistributionData.value = phData;
        soilTextureData.value = textureData;
        nutrientTrendData.value = trendData;
        
        console.log('图表数据加载完成');
        
        // 如果图表已经初始化，则更新配置
        if (regionChart && phChart && trendChart && textureChart) {
          updateChartConfigs();
        }
      } catch (error) {
        console.error('加载图表数据失败:', error);
      }
    };
    
    // 更新图表配置
    const updateChartConfigs = () => {
      if (!regionChart || !phChart || !trendChart || !textureChart) {
        console.log('图表实例未初始化，跳过更新配置');
        return;
      }
      
      console.log('开始更新图表配置...');
      
      // 更新区域养分图表
      if (regionNutrientData.value.length > 0) {
        updateRegionNutrientChart();
      }
      
      // 更新pH分布图表
      if (phDistributionData.value.length > 0) {
        updatePhDistributionChart();
      }
      
      // 更新土壤质地图表
      if (soilTextureData.value.length > 0) {
        updateSoilTextureChart();
      }
      
      // 更新养分趋势图表
      if (nutrientTrendData.value.length > 0) {
        updateNutrientTrendChart();
      }
    };
    
    // 更新区域养分图表
    const updateRegionNutrientChart = () => {
      const provinces = regionNutrientData.value.map(item => item.province);
      const nitrogenData = regionNutrientData.value.map(item => item.nitrogen);
      const phosphorusData = regionNutrientData.value.map(item => item.phosphorus);
      const potassiumData = regionNutrientData.value.map(item => item.potassium);
      const organicData = regionNutrientData.value.map(item => item.organic);
      
      regionChart.setOption({
        xAxis: {
          data: provinces
        },
        series: [
          {
            name: '氮含量',
            data: nitrogenData
          },
          {
            name: '磷含量',
            data: phosphorusData
          },
          {
            name: '钾含量',
            data: potassiumData
          },
          {
            name: '有机质',
            data: organicData
          }
        ]
      });
    };
    
    // 更新pH分布图表
    const updatePhDistributionChart = () => {
      phChart.setOption({
        series: [
          {
            data: phDistributionData.value.map(item => ({
              name: item.name,
              value: item.value
            }))
          }
        ]
      });
    };
    
    // 更新土壤质地图表
    const updateSoilTextureChart = () => {
      textureChart.setOption({
        series: [
          {
            data: soilTextureData.value.map(item => ({
              name: item.name,
              value: item.value
            }))
          }
        ]
      });
    };
    
    // 更新养分趋势图表
    const updateNutrientTrendChart = () => {
      const months = nutrientTrendData.value.map(item => item.month);
      const nitrogenData = nutrientTrendData.value.map(item => item.nitrogen);
      const phosphorusData = nutrientTrendData.value.map(item => item.phosphorus);
      const potassiumData = nutrientTrendData.value.map(item => item.potassium);
      const organicData = nutrientTrendData.value.map(item => item.organic);
      
      trendChart.setOption({
        xAxis: {
          data: months
        },
        series: [
          {
            name: '氮含量',
            data: nitrogenData
          },
          {
            name: '磷含量',
            data: phosphorusData
          },
          {
            name: '钾含量',
            data: potassiumData
          },
          {
            name: '有机质',
            data: organicData
          }
        ]
      });
    };
    
    // 初始化图表
    const initCharts = () => {
      console.log('开始初始化图表...');
      checkEnvironment();
      
      // 检查echarts是否正确载入
      if (!echarts) {
        console.error('ECharts未找到，请确保正确引入ECharts库');
        return;
      }
      
      console.log('ECharts版本:', echarts.version);
      
      try {
        // 针对uni-app平台处理
        if (typeof uni !== 'undefined') {
          console.log('使用uni-app选择器查询DOM');
          // 使用uni-app的查询选择器获取元素
          const query = uni.createSelectorQuery();
          query.select('#region-nutrient-chart').boundingClientRect();
          query.select('#ph-distribution-chart').boundingClientRect();
          query.select('#nutrient-trend-chart').boundingClientRect();
          query.select('#soil-texture-chart').boundingClientRect();
          
          query.exec(function(res) {
            console.log('查询选择器结果:', res);
            
            if (!res || res.length < 4 || !res[0] || !res[1] || !res[2] || !res[3]) {
              console.error('图表容器DOM元素未找到', res);
              // 延迟再次尝试
              setTimeout(initCharts, 300);
              return;
            }
            
            console.log('所有图表DOM元素已找到，开始初始化');
            console.log('图表容器尺寸:', {
              region: { width: res[0].width, height: res[0].height },
              ph: { width: res[1].width, height: res[1].height },
              trend: { width: res[2].width, height: res[2].height },
              texture: { width: res[3].width, height: res[3].height }
            });
            
            // 检查容器尺寸是否合理
            if (res[0].width < 10 || res[0].height < 10) {
              console.error('图表容器尺寸太小:', res[0]);
              setTimeout(initCharts, 300);
              return;
            }
            
            // 使用uni-app方式获取DOM元素
            initECharts();
          });
        } else {
          // 在非uni-app环境下直接使用DOM API
          console.log('在标准Web环境中初始化图表');
          setTimeout(initECharts, 0);
        }
      } catch (error) {
        console.error('图表初始化失败:', error);
        console.error('错误堆栈:', error.stack);
        setTimeout(initCharts, 300);
      }
    };
    
    // 实际的ECharts初始化函数
    const initECharts = () => {
      try {
        console.log('开始实际初始化ECharts实例');
        
        // 获取DOM元素
        const regionChartEl = document.getElementById('region-nutrient-chart');
        const phChartEl = document.getElementById('ph-distribution-chart');
        const trendChartEl = document.getElementById('nutrient-trend-chart');
        const textureChartEl = document.getElementById('soil-texture-chart');
        
        if (!regionChartEl || !phChartEl || !trendChartEl || !textureChartEl) {
          console.error('无法通过document.getElementById获取图表元素');
          return;
        }
        
        // 初始化之前先清理之前的实例
        if (regionChart) regionChart.dispose();
        if (phChart) phChart.dispose();
        if (trendChart) trendChart.dispose();
        if (textureChart) textureChart.dispose();
        
        // 初始化图表
        regionChart = echarts.init(regionChartEl);
        phChart = echarts.init(phChartEl);
        trendChart = echarts.init(trendChartEl);
        textureChart = echarts.init(textureChartEl);
        
        // 更新图表配置
        updateChartConfigs();
        
      // 各地区土壤养分平均值图表
        regionChart.setOption({
          title: {
            text: '各地区土壤养分平均值',
            left: 'center',
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            },
            formatter: function(params) {
              let result = params[0].name + '<br/>';
              params.forEach(param => {
                result += 
                  `<span style="display:inline-block;margin-right:4px;border-radius:10px;width:10px;height:10px;background-color:${param.color};"></span>` +
                  `${param.seriesName}: ${param.value} mg/kg<br/>`;
              });
              return result;
            }
          },
          legend: {
            data: ['氮含量', '磷含量', '钾含量', '有机质'],
            bottom: 0
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '15%',
            top: '15%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: ['北京', '上海', '成都', '哈尔滨', '广州', '重庆', '西安'],
            axisLabel: {
              interval: 0,
              rotate: 30
            }
          },
          yAxis: [
            {
            type: 'value',
              name: '氮磷钾 (mg/kg)',
              min: 0,
              max: 150,
              interval: 30,
              axisLabel: {
                formatter: '{value}'
              }
            },
            {
              type: 'value',
              name: '有机质 (%)',
              min: 0,
              max: 5,
              interval: 1,
              axisLabel: {
                formatter: '{value}'
              }
            }
          ],
          series: [
            {
              name: '氮含量',
              type: 'bar',
              barWidth: '15%',
              data: [82.5, 67.5, 73.5, 46.5, 92.5, 88, 76],
              itemStyle: { color: '#ff6b6b' }
            },
            {
              name: '磷含量',
              type: 'bar',
              barWidth: '15%',
              data: [42.5, 52.5, 36.5, 26.5, 62.5, 47, 39],
              itemStyle: { color: '#48dbfb' }
            },
            {
              name: '钾含量',
              type: 'bar',
              barWidth: '15%',
              data: [117.5, 92.5, 107.5, 82.5, 127.5, 105, 98],
              itemStyle: { color: '#1dd1a1' }
            },
            {
              name: '有机质',
              type: 'line',
              yAxisIndex: 1,
              symbol: 'circle',
              symbolSize: 8,
              data: [2.35, 1.85, 2.05, 3.10, 1.55, 2.5, 2.1],
              itemStyle: { color: '#feca57' },
              lineStyle: {
                width: 3
              }
            }
          ]
        });
        
        // pH分布图
        phChart.setOption({
          title: {
            text: '土壤pH值分布',
            left: 'center',
            textStyle: {
              fontSize: 14
            },
            subtext: '按采样点数量统计'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} 个样本点 ({d}%)'
          },
          legend: {
            orient: 'vertical',
            right: 10,
            top: 'center',
            data: ['强酸性(≤5.5)', '弱酸性(5.5-6.5)', '中性(6.5-7.5)', '碱性(≥7.5)']
          },
          series: [
            {
              name: 'pH值分布',
              type: 'pie',
              radius: ['40%', '70%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: true,
                formatter: '{b}: {c} ({d}%)'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: '14',
                  fontWeight: 'bold'
                },
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              },
              data: [
                { 
                  value: 1, 
                  name: '强酸性(≤5.5)',
                  itemStyle: { color: '#ff6b6b' }
                },
                { 
                  value: 3, 
                  name: '弱酸性(5.5-6.5)',
                  itemStyle: { color: '#ff9f43' }
                },
                { 
                  value: 5, 
                  name: '中性(6.5-7.5)',
                  itemStyle: { color: '#1dd1a1' }
                },
                { 
                  value: 1, 
                  name: '碱性(≥7.5)',
                  itemStyle: { color: '#54a0ff' }
                }
              ]
            }
          ]
        });
        
        // 养分趋势图
        trendChart.setOption({
          title: {
            text: '养分含量时间趋势 (2023年)',
            left: 'center',
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross',
              label: {
                backgroundColor: '#6a7985'
              }
            }
          },
          legend: {
            data: ['氮含量', '磷含量', '钾含量', '有机质'],
            bottom: 0
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
          grid: {
            left: '3%',
            right: '4%',
            bottom: '15%',
            top: '15%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
          },
          yAxis: [
            {
            type: 'value',
              name: 'mg/kg',
              min: 0,
              max: 140,
              position: 'left',
              axisLine: {
                show: true,
                lineStyle: {
                  color: '#5470c6'
                }
              },
              axisLabel: {
                formatter: '{value}'
              }
            },
            {
              type: 'value',
              name: '有机质 (%)',
              min: 0,
              max: 3.5,
              position: 'right',
              axisLine: {
                show: true,
                lineStyle: {
                  color: '#feca57'
                }
              },
              axisLabel: {
                formatter: '{value}'
              }
            }
          ],
          series: [
            {
              name: '氮含量',
              type: 'line',
              smooth: true,
              data: [65, 68, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92],
              itemStyle: { color: '#ff6b6b' },
              markPoint: {
                data: [
                  { type: 'max', name: '最大值' },
                  { type: 'min', name: '最小值' }
                ]
              }
            },
            {
              name: '磷含量',
              type: 'line',
              smooth: true,
              data: [32, 34, 35, 37, 40, 42, 45, 47, 50, 52, 55, 57],
              itemStyle: { color: '#48dbfb' }
            },
            {
              name: '钾含量',
              type: 'line',
              smooth: true,
              data: [92, 95, 98, 102, 105, 110, 112, 115, 118, 120, 122, 125],
              itemStyle: { color: '#1dd1a1' }
            },
            {
              name: '有机质',
              type: 'line',
              smooth: true,
              yAxisIndex: 1,
              data: [1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.4, 2.5, 2.6, 2.7],
              itemStyle: { color: '#feca57' },
              areaStyle: {
                opacity: 0.2
              }
            }
          ]
        });
        
        // 土壤质地分布
        textureChart.setOption({
          title: {
            text: '土壤质地分布',
            left: 'center',
            textStyle: {
              fontSize: 14
            },
            subtext: '基于采样点统计'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c}个样本点 ({d}%)'
          },
          legend: {
            type: 'scroll',
            orient: 'horizontal',
            bottom: 0,
            data: ['砂质土', '壤土', '砂壤土', '粘壤土', '黑土', '粘土']
          },
          series: [
            {
              name: '土壤质地',
              type: 'pie',
              radius: '65%',
              center: ['50%', '45%'],
              selectedMode: 'single',
              data: [
                { 
                  value: 3, 
                  name: '砂质土',
                  itemStyle: { color: '#f6e58d' }
                },
                { 
                  value: 2, 
                  name: '壤土',
                  itemStyle: { color: '#f0932b' }
                },
                { 
                  value: 2, 
                  name: '砂壤土',
                  itemStyle: { color: '#eb4d4b' }
                },
                { 
                  value: 2, 
                  name: '粘壤土',
                  itemStyle: { color: '#6ab04c' }
                },
                { 
                  value: 2, 
                  name: '黑土',
                  itemStyle: { color: '#130f40' }
                },
                { 
                  value: 1, 
                  name: '粘土',
                  itemStyle: { color: '#4834d4' } 
                }
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              },
              label: {
                formatter: '{b}: {d}%',
                position: 'outside'
              },
              labelLine: {
                show: true
              }
            }
          ]
        });
        
        // 窗口大小调整处理
        const handleResize = () => {
          console.log('窗口大小变化，重新调整图表大小');
          regionChart && regionChart.resize();
          phChart && phChart.resize();
          trendChart && trendChart.resize();
          textureChart && textureChart.resize();
        };
        
        window.addEventListener('resize', handleResize);
        
        // 监听页面显示事件
        uni.$on('soil-data-shown', handleResize);
        
        // 返回清理函数，用于onBeforeUnmount调用
        return () => {
          window.removeEventListener('resize', handleResize);
          uni.$off('soil-data-shown');
        };
      } catch (error) {
        console.error('ECharts实例化失败:', error);
        console.error('错误堆栈:', error.stack);
      }
    };
    
    // 处理分页
    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
      }
    };
    
    onMounted(async () => {
      console.log('组件已挂载，准备加载数据和初始化图表...');
      
      // 首先加载数据
      await Promise.all([
        loadSoilDataTable(),
        loadChartData()
      ]);
      
      // 延迟一点初始化图表，确保DOM元素已渲染完成
      setTimeout(() => {
        initCharts();
      }, 500);
    });
    
    // 组件卸载前清理资源
    onBeforeUnmount(() => {
      console.log('组件即将卸载，清理图表实例...');
      if (regionChart) regionChart.dispose();
      if (phChart) phChart.dispose();
      if (trendChart) trendChart.dispose();
      if (textureChart) textureChart.dispose();
      
      // 移除事件监听
      uni.$off('soil-data-shown');
    });

    const exportToCSV = () => {
      if (!mockSoilData.value || mockSoilData.value.length === 0) {
        uni.showToast({ title: '没有数据可导出', icon: 'none' });
        return;
      }
      const dataToExport = mockSoilData.value;
      const headers = ['采样点ID', '采样时间', '采样地点', 'pH值', '氮(mg/kg)', '磷(mg/kg)', '钾(mg/kg)', '有机质(%)', '土壤质地'];
      const csvRows = [];
      csvRows.push(headers.join(','));

      dataToExport.forEach(item => {
        const row = [
          item.id,
          item.time,
          item.location,
          item.ph,
          item.nitrogen,
          item.phosphorus,
          item.potassium,
          item.organic,
          item.texture
        ];
        csvRows.push(row.join(','));
      });

      const csvString = csvRows.join('\\n');
      const universalBOM = '\\uFEFF'; // UTF-8 BOM
      const blob = new Blob([universalBOM + csvString], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      if (link.download !== undefined) { // Check for download attribute
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', 'soil_data.csv');
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      } else {
        uni.showToast({ title: '浏览器不支持直接下载', icon: 'none' });
      }
    };

    const exportToExcel = () => {
      if (!mockSoilData.value || mockSoilData.value.length === 0) {
        uni.showToast({ title: '没有数据可导出', icon: 'none' });
        return;
      }
      const dataToExport = mockSoilData.value;
      const headers = ['采样点ID', '采样时间', '采样地点', 'pH值', '氮(mg/kg)', '磷(mg/kg)', '钾(mg/kg)', '有机质(%)', '土壤质地'];
      
      const aoa = [
        headers,
        ...dataToExport.map(item => [
          item.id,
          item.time,
          item.location,
          item.ph,
          item.nitrogen,
          item.phosphorus,
          item.potassium,
          item.organic,
          item.texture
        ])
      ];

      const ws = XLSX.utils.aoa_to_sheet(aoa);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, '土壤数据');
      XLSX.writeFile(wb, 'soil_data.xlsx');
    };

    const navigateToSampleCountReport = () => {
      uni.navigateTo({ url: '/pages/data-reports/sample-count-report/sample-count-report' });
    };

    const navigateToProvinceCoverageReport = () => {
      uni.navigateTo({ url: '/pages/data-reports/province-coverage-report/province-coverage-report' });
    };

    const navigateToDataIntegrityReport = () => {
      uni.navigateTo({ url: '/pages/data-reports/data-integrity-report/data-integrity-report' });
    };

    const navigateToAnomalyPointsReport = () => {
      uni.navigateTo({ url: '/pages/data-reports/anomaly-points-report/anomaly-points-report' });
    };
    
    return {
      mockSoilData,
      currentPage,
      totalPages,
      goToPage,
      exportToCSV,
      exportToExcel,
      navigateToSampleCountReport,
      navigateToProvinceCoverageReport,
      navigateToDataIntegrityReport,
      navigateToAnomalyPointsReport
    };
  }
};
</script>

<template>
  <view class="page-container" id="soil-data-page">
    <view class="page-header">
      <text class="header-title">土壤数据统计与分析</text>
    </view>
    <view class="data-dashboard">
      <view class="stats-cards">
        <view class="stat-card" @click="navigateToSampleCountReport">
          <view class="stat-icon">叶</view>
          <view class="stat-content">
            <text class="stat-value">1,245</text>
            <text class="stat-label">样本总数</text>
          </view>
        </view>
        <view class="stat-card" @click="navigateToProvinceCoverageReport">
          <view class="stat-icon">图</view>
          <view class="stat-content">
            <text class="stat-value">28</text>
            <text class="stat-label">覆盖省份</text>
          </view>
        </view>
        <view class="stat-card" @click="navigateToDataIntegrityReport">
          <view class="stat-icon">表</view>
          <view class="stat-content">
            <text class="stat-value">86%</text>
            <text class="stat-label">数据完整率</text>
          </view>
        </view>
        <view class="stat-card" @click="navigateToAnomalyPointsReport">
          <view class="stat-icon">警</view>
          <view class="stat-content">
            <text class="stat-value">48</text>
            <text class="stat-label">异常点位</text>
          </view>
        </view>
      </view>
      
      <view class="data-filters">
        <view class="filter-row">
          <view class="filter-group">
            <text>选择地区</text>
            <picker :range="['全国', '华北地区', '华东地区', '华南地区', '西部地区']">
              <view class="picker-view">全国</view>
            </picker>
          </view>
          <view class="filter-group">
            <text>选择时间范围</text>
            <picker :range="['最近7天', '最近30天', '最近90天', '最近1年', '自定义...']">
              <view class="picker-view">最近1年</view>
            </picker>
          </view>
          <view class="filter-group">
            <text>数据类型</text>
            <picker :range="['氮含量', '磷含量', '钾含量', '有机质', '全部']">
              <view class="picker-view">全部</view>
            </picker>
          </view>
          <button class="btn filter-btn" type="primary">应用筛选</button>
        </view>
      </view>
      
      <view class="chart-grid">
        <view class="chart-item">
          <view class="chart-header">
            <text class="section-title">各地区土壤养分平均值</text>
          </view>
          <view class="chart-body" id="region-nutrient-chart"></view>
        </view>
        <view class="chart-item">
          <view class="chart-header">
            <text class="section-title">土壤pH值分布</text>
          </view>
          <view class="chart-body" id="ph-distribution-chart"></view>
        </view>
        <view class="chart-item">
          <view class="chart-header">
            <text class="section-title">养分含量时间趋势</text>
          </view>
          <view class="chart-body" id="nutrient-trend-chart"></view>
        </view>
        <view class="chart-item">
          <view class="chart-header">
            <text class="section-title">土壤质地分布</text>
          </view>
          <view class="chart-body" id="soil-texture-chart"></view>
        </view>
      </view>
      
      <view class="data-table-section">
        <view class="section-header">
          <text class="section-title">土壤样本数据表</text>
          <view class="section-actions">
            <button class="btn btn-outline" size="mini" @click="exportToExcel">导出Excel</button>
            <button class="btn btn-outline" size="mini" @click="exportToCSV">导出CSV</button>
            <button class="btn" type="primary" size="mini">刷新数据</button>
          </view>
        </view>
        <scroll-view class="data-table-container" scroll-x="true">
          <view class="data-table">
            <view class="table-header">
              <view class="th">采样点ID</view>
              <view class="th">采样时间</view>
              <view class="th">采样地点</view>
              <view class="th">pH值</view>
              <view class="th">氮 (mg/kg)</view>
              <view class="th">磷 (mg/kg)</view>
              <view class="th">钾 (mg/kg)</view>
              <view class="th">有机质 (%)</view>
              <view class="th">土壤质地</view>
              <view class="th">操作</view>
            </view>
            <view class="table-body">
              <view class="tr" v-for="item in mockSoilData" :key="item.id">
                <view class="td">{{ item.id }}</view>
                <view class="td">{{ item.time }}</view>
                <view class="td">{{ item.location }}</view>
                <view class="td">{{ item.ph }}</view>
                <view class="td">{{ item.nitrogen }}</view>
                <view class="td">{{ item.phosphorus }}</view>
                <view class="td">{{ item.potassium }}</view>
                <view class="td">{{ item.organic }}</view>
                <view class="td">{{ item.texture }}</view>
                <view class="td">
                  <view class="table-actions">
                    <button class="action-btn" size="mini">查看</button>
                    <button class="action-btn" size="mini">编辑</button>
                  </view>
                </view>
              </view>
            </view>
          </view>
        </scroll-view>
        <view class="pagination">
          <button class="page-btn" :disabled="currentPage === 1" @click="goToPage(1)" size="mini">
            首页
          </button>
          <button class="page-btn" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)" size="mini">
            上一页
          </button>
          <view class="page-info">第 <text>{{ currentPage }}</text> 页，共 <text>{{ totalPages }}</text> 页</view>
          <button class="page-btn" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)" size="mini">
            下一页
          </button>
          <button class="page-btn" :disabled="currentPage === totalPages" @click="goToPage(totalPages)" size="mini">
            末页
          </button>
        </view>
      </view>
    </view>
  </view>
</template>

<style>
.page-container {
  width: 100%;
  box-sizing: border-box;
  overflow-x: hidden;  /* 防止水平溢出 */
}

.page-header {
  padding: 20px;
  background-color: white;
  border-bottom: 1px solid #eee;
  width: 100%;
  box-sizing: border-box;
}

.header-title {
  font-size: 18px;
  font-weight: bold;
}

.data-dashboard {
  padding: 15px;
  width: 100%;
  box-sizing: border-box;
  max-width: 100%;
  overflow-x: hidden;
}

.stats-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
  width: 100%;
  box-sizing: border-box;
}

.stat-card {
  flex: 1;
  min-width: 160px;
  max-width: calc(50% - 15px); /* 在小屏幕上每行最多显示2个 */
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 15px;
  display: flex;
  align-items: center;
  box-sizing: border-box;
}

.stat-icon {
  width: 40px;
  height: 40px;
  background-color: #4d7bce;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-right: 15px;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
  min-width: 0; /* 防止内容溢出 */
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.data-filters {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 15px;
  margin-bottom: 20px;
  width: 100%;
  box-sizing: border-box;
  overflow-x: auto; /* 允许在小屏幕上滚动 */
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: flex-end;
  min-width: 600px; /* 确保在小屏幕上可以滚动查看 */
}

.filter-group {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 150px;
  max-width: 200px;
}

.filter-group text {
  font-size: 14px;
  color: #555;
  margin-bottom: 5px;
}

.picker-view {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f8f8f8;
  width: 100%;
  box-sizing: border-box;
}

.filter-btn {
  padding: 0 20px;
  height: 40px;
  line-height: 40px;
  flex-shrink: 0;
}

.chart-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
  width: 100%;
  box-sizing: border-box;
}

.chart-item {
  flex: 1 1 calc(50% - 15px); /* 每行最多2个图表 */
  min-width: 300px;
  max-width: 100%; /* 确保在小屏幕上不会超出容器 */
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
  box-sizing: border-box;
}

.chart-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
  width: 100%;
  box-sizing: border-box;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
}

.chart-body {
  height: 300px;
  padding: 15px;
  width: 100%;
  position: relative;
  background-color: #fff;
  box-sizing: border-box;
}

.data-table-section {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
  margin-bottom: 20px;
  width: 100%;
  box-sizing: border-box;
}

.section-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  width: 100%;
  box-sizing: border-box;
}

.section-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.data-table-container {
  width: 100%;
  overflow-x: auto;
  box-sizing: border-box;
  -webkit-overflow-scrolling: touch; /* 在iOS上提供更好的滚动体验 */
}

.data-table {
  min-width: 800px; /* 确保表格在小屏幕上可以滚动查看 */
  width: 100%;
  border-collapse: collapse;
  box-sizing: border-box;
}

.table-header {
  display: flex;
  background-color: #f5f7fa;
  min-width: 800px;
  width: 100%;
  box-sizing: border-box;
}

.table-body {
  display: flex;
  flex-direction: column;
  min-width: 800px;
  width: 100%;
  box-sizing: border-box;
}

.tr {
  display: flex;
  border-bottom: 1px solid #eee;
  min-width: 800px;
  width: 100%;
  box-sizing: border-box;
}

.th, .td {
  padding: 12px 15px;
  text-align: left;
  flex: 1;
  min-width: 120px;
  word-break: break-word; /* 允许长文本换行 */
  box-sizing: border-box;
}

.th {
  font-weight: bold;
  color: #333;
}

.table-actions {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.action-btn {
  font-size: 12px;
  padding: 0 10px;
  line-height: 24px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 15px;
  gap: 10px;
  flex-wrap: wrap;
  width: 100%;
  box-sizing: border-box;
}

.page-btn {
  font-size: 12px;
  padding: 0 10px;
  flex-shrink: 0;
}

.page-info {
  margin: 0 15px;
  color: #666;
  font-size: 14px;
  white-space: nowrap;
}

.page-info text {
  color: #4d7bce;
  font-weight: bold;
}

/* 响应式调整 */
@media screen and (max-width: 768px) {
  .chart-item {
    flex: 1 1 100%; /* 在小屏幕上一行只显示一个图表 */
  }
  
  .filter-group {
    max-width: none;
    width: 100%;
  }
  
  .stat-card {
    max-width: 100%; /* 在小屏幕上一行只显示一个统计卡片 */
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .section-actions {
    margin-top: 10px;
    width: 100%;
  }
}

/* 适配uni-app平台的样式调整 */
/* #ifdef MP-WEIXIN */
.page-container {
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
}
/* #endif */
</style> 