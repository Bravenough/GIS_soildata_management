<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as echarts from 'echarts';
import soilDataAPI from '@/utils/api.js';

export default {
  name: 'AssessmentView',
  setup() {
    const nutrientLevelsRef = ref(null);
    const qualityTrendsRef = ref(null);
    const soilQualityMapRef = ref(null);
    const factorContributionRef = ref(null);
    
    const chartInstances = ref({});
    const currentRegion = ref('全国');
    const currentYear = ref('2023');
    
    // 评估数据
    const assessmentData = ref({
      nutrientLevels: {
        nitrogen: 75,
        phosphorus: 68,
        potassium: 82,
        organic: 80,
        ph: 90,
        trace: 70
      },
      qualityTrends: [],
      regionalStats: [],
      factorContribution: []
    });
    
    // 加载评估数据
    const loadAssessmentData = async () => {
      try {
        console.log('开始加载评估数据...');
        
        // 获取统计概况数据
        const [overview, regionStats, trendData] = await Promise.all([
          soilDataAPI.getStatisticsOverview(),
          soilDataAPI.getRegionNutrientStats(),
          soilDataAPI.getNutrientTrendData()
        ]);
        
        // 更新评估数据
        if (regionStats.length > 0) {
          const avgStats = regionStats.reduce((acc, region) => ({
            nitrogen: acc.nitrogen + region.nitrogen,
            phosphorus: acc.phosphorus + region.phosphorus,
            potassium: acc.potassium + region.potassium,
            organic: acc.organic + region.organic
          }), { nitrogen: 0, phosphorus: 0, potassium: 0, organic: 0 });
          
          const count = regionStats.length;
          assessmentData.value.nutrientLevels = {
            nitrogen: Math.round((avgStats.nitrogen / count) * 0.8), // 转换为百分制
            phosphorus: Math.round((avgStats.phosphorus / count) * 1.2),
            potassium: Math.round((avgStats.potassium / count) * 0.7),
            organic: Math.round((avgStats.organic / count) * 30),
            ph: overview.averagePh ? Math.round((overview.averagePh / 14) * 100) : 70,
            trace: 70 // 默认值，实际应从数据库获取
          };
        }
        
        assessmentData.value.qualityTrends = trendData;
        assessmentData.value.regionalStats = regionStats;
        
        console.log('评估数据加载完成');
        
        // 更新图表
        updateCharts();
        
      } catch (error) {
        console.error('加载评估数据失败:', error);
        // 使用默认数据
        console.log('使用默认评估数据');
      }
    };
    
    // 更新所有图表
    const updateCharts = () => {
      console.log('开始更新图表...');
      
      // 更新养分水平雷达图
      if (chartInstances.value.nutrientLevels) {
        updateNutrientLevelsChart();
      }
      
      // 更新质量趋势图
      if (chartInstances.value.qualityTrends) {
        updateQualityTrendsChart();
      }
    };
    
    // 更新养分水平雷达图
    const updateNutrientLevelsChart = () => {
      const chart = chartInstances.value.nutrientLevels;
      if (!chart) return;
      
      chart.setOption({
        series: [
          {
            data: [
              {
                value: [
                  assessmentData.value.nutrientLevels.nitrogen,
                  assessmentData.value.nutrientLevels.phosphorus,
                  assessmentData.value.nutrientLevels.potassium,
                  assessmentData.value.nutrientLevels.organic,
                  assessmentData.value.nutrientLevels.ph,
                  assessmentData.value.nutrientLevels.trace
                ],
                name: '当前状态'
              },
              {
                value: [90, 85, 90, 95, 95, 90],
                name: '目标水平'
              }
            ]
          }
        ]
      });
    };
    
    // 更新质量趋势图
    const updateQualityTrendsChart = () => {
      const chart = chartInstances.value.qualityTrends;
      if (!chart || !assessmentData.value.qualityTrends.length) return;
      
      const months = assessmentData.value.qualityTrends.map(item => item.month);
      const nitrogenData = assessmentData.value.qualityTrends.map(item => Math.round(item.nitrogen * 0.8));
      const phosphorusData = assessmentData.value.qualityTrends.map(item => Math.round(item.phosphorus * 1.2));
      const potassiumData = assessmentData.value.qualityTrends.map(item => Math.round(item.potassium * 0.7));
      const organicData = assessmentData.value.qualityTrends.map(item => Math.round(item.organic * 30));
      
      // 计算综合评分
      const comprehensiveData = assessmentData.value.qualityTrends.map((item, index) => {
        return Math.round((nitrogenData[index] + phosphorusData[index] + potassiumData[index] + organicData[index]) / 4);
      });
      
      chart.setOption({
        xAxis: {
          data: months
        },
        series: [
          {
            name: '综合评分',
            data: comprehensiveData
          },
          {
            name: '氮水平',
            data: nitrogenData
          },
          {
            name: '磷水平',
            data: phosphorusData
          },
          {
            name: '钾水平',
            data: potassiumData
          },
          {
            name: '有机质',
            data: organicData
          }
        ]
      });
    };
    
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
    
    // 初始化养分水平雷达图
    const initNutrientLevelsChart = () => {
      console.log('初始化养分水平雷达图...');
      try {
        const chartElement = document.querySelector('.nutrient-levels-chart');
        if (!chartElement) {
          console.error('无法找到养分水平雷达图DOM元素');
          return;
        }
        
        const chart = echarts.init(chartElement);
        chartInstances.value.nutrientLevels = chart;
        
        const option = {
          title: {
            text: '土壤养分水平评估',
            left: 'center'
          },
          tooltip: {},
          radar: {
            indicator: [
              { name: '氮含量', max: 100 },
              { name: '磷含量', max: 100 },
              { name: '钾含量', max: 100 },
              { name: '有机质', max: 100 },
              { name: 'pH值适宜度', max: 100 },
              { name: '微量元素', max: 100 }
            ],
            radius: '65%'
          },
          series: [
            {
              name: '养分水平评分',
              type: 'radar',
              data: [
                {
                  value: [
                    assessmentData.value.nutrientLevels.nitrogen,
                    assessmentData.value.nutrientLevels.phosphorus,
                    assessmentData.value.nutrientLevels.potassium,
                    assessmentData.value.nutrientLevels.organic,
                    assessmentData.value.nutrientLevels.ph,
                    assessmentData.value.nutrientLevels.trace
                  ],
                  name: '当前状态',
                  areaStyle: {
                    color: 'rgba(77, 123, 206, 0.3)'
                  },
                  lineStyle: {
                    color: '#4d7bce'
                  },
                  itemStyle: {
                    color: '#4d7bce'
                  }
                },
                {
                  value: [90, 85, 90, 95, 95, 90],
                  name: '目标水平',
                  lineStyle: {
                    color: '#42b983'
                  },
                  itemStyle: {
                    color: '#42b983'
                  }
                }
              ]
            }
          ]
        };
        
        chart.setOption(option);
        console.log('养分水平雷达图初始化完成');
      } catch (error) {
        console.error('养分水平雷达图初始化失败:', error);
        console.error('错误堆栈:', error.stack);
      }
    };
    
    // 初始化土壤质量趋势图
    const initQualityTrendsChart = () => {
      console.log('初始化土壤质量趋势图...');
      try {
        const chartElement = document.querySelector('.quality-trends-chart');
        if (!chartElement) {
          console.error('无法找到土壤质量趋势图DOM元素');
          return;
        }
        
        const chart = echarts.init(chartElement);
        chartInstances.value.qualityTrends = chart;
        
        const option = {
          title: {
            text: '土壤质量历年变化趋势',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['综合评分', '氮水平', '磷水平', '钾水平', '有机质'],
            bottom: 0
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['2018', '2019', '2020', '2021', '2022', '2023']
          },
          yAxis: {
            type: 'value',
            name: '评分',
            max: 100
          },
          series: [
            {
              name: '综合评分',
              type: 'line',
              data: [65, 68, 70, 72, 74, 79],
              lineStyle: {
                width: 3,
                color: '#e65328'
              },
              itemStyle: {
                color: '#e65328'
              }
            },
            {
              name: '氮水平',
              type: 'line',
              data: [60, 65, 68, 70, 73, 75],
              lineStyle: {
                color: '#4d7bce'
              },
              itemStyle: {
                color: '#4d7bce'
              }
            },
            {
              name: '磷水平',
              type: 'line',
              data: [55, 58, 60, 62, 65, 68],
              lineStyle: {
                color: '#42b983'
              },
              itemStyle: {
                color: '#42b983'
              }
            },
            {
              name: '钾水平',
              type: 'line',
              data: [72, 75, 76, 79, 80, 82],
              lineStyle: {
                color: '#f2c037'
              },
              itemStyle: {
                color: '#f2c037'
              }
            },
            {
              name: '有机质',
              type: 'line',
              data: [68, 70, 72, 76, 78, 80],
              lineStyle: {
                color: '#9d56ab'
              },
              itemStyle: {
                color: '#9d56ab'
              }
            }
          ]
        };
        
        chart.setOption(option);
        console.log('土壤质量趋势图初始化完成');
      } catch (error) {
        console.error('土壤质量趋势图初始化失败:', error);
        console.error('错误堆栈:', error.stack);
      }
    };
    
    // 初始化土壤质量分布图
    const initSoilQualityMap = () => {
      console.log('初始化土壤质量分布图...');
      try {
        const chartElement = document.querySelector('.soil-quality-map-chart');
        if (!chartElement) {
          console.error('无法找到土壤质量分布图DOM元素');
          return;
        }
        
        const chart = echarts.init(chartElement);
        chartInstances.value.soilQualityMap = chart;
        
        // 简化示例代码
        const option = {
          title: {
            text: '土壤质量分级分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            data: ['优', '良', '中等', '较差', '差']
          },
          series: [
            {
              name: '土壤质量等级',
              type: 'pie',
              radius: '50%',
              center: ['50%', '60%'],
              data: [
                {value: 15, name: '优', itemStyle: {color: '#42b983'}},
                {value: 30, name: '良', itemStyle: {color: '#91cc75'}},
                {value: 35, name: '中等', itemStyle: {color: '#fac858'}},
                {value: 15, name: '较差', itemStyle: {color: '#ee6666'}},
                {value: 5, name: '差', itemStyle: {color: '#73c0de'}}
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        };
        
        chart.setOption(option);
        console.log('土壤质量分布图初始化完成');
      } catch (error) {
        console.error('土壤质量分布图初始化失败:', error);
        console.error('错误堆栈:', error.stack);
      }
    };
    
    // 初始化影响因素贡献度图
    const initFactorContributionChart = () => {
      console.log('初始化影响因素贡献度图...');
      try {
        const chartElement = document.querySelector('.factor-contribution-chart');
        if (!chartElement) {
          console.error('无法找到影响因素贡献度图DOM元素');
          return;
        }
        
        const chart = echarts.init(chartElement);
        chartInstances.value.factorContribution = chart;
        
        const option = {
          title: {
            text: '影响因素贡献度分析',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{b}: {c}%'
          },
          legend: {
            type: 'scroll',
            orient: 'vertical',
            right: 10,
            top: 20,
            bottom: 20,
          },
          series: [
            {
              name: '影响因素',
              type: 'pie',
              radius: ['40%', '70%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: false,
                position: 'center'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: 20,
                  fontWeight: 'bold'
                }
              },
              labelLine: {
                show: false
              },
              data: [
                {value: 25, name: '有机质含量'},
                {value: 20, name: '养分平衡度'},
                {value: 18, name: 'pH值'},
                {value: 15, name: '农业活动'},
                {value: 10, name: '水资源质量'},
                {value: 7, name: '气候因素'},
                {value: 5, name: '其他'}
              ]
            }
          ]
        };
        
        chart.setOption(option);
        console.log('影响因素贡献度图初始化完成');
      } catch (error) {
        console.error('影响因素贡献度图初始化失败:', error);
        console.error('错误堆栈:', error.stack);
      }
    };
    
    // 初始化所有图表
    const initCharts = () => {
      console.log('开始初始化所有图表...');
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
          query.selectAll('.chart-body').boundingClientRect();
          
          query.exec(function(res) {
            console.log('查询选择器结果:', res);
            
            if (!res || res.length < 1 || !res[0] || res[0].length < 4) {
              console.error('图表容器DOM元素未找到', res);
              // 延迟再次尝试
              setTimeout(() => initCharts(), 300);
              return;
            }
            
            console.log('图表DOM元素已找到，开始初始化');
            
            // 检查容器尺寸是否合理
            for (let i = 0; i < res[0].length; i++) {
              if (res[0][i].width < 10 || res[0][i].height < 10) {
                console.error(`图表容器${i}尺寸太小:`, res[0][i]);
                setTimeout(() => initCharts(), 300);
                return;
              }
            }
            
            // 延迟初始化各个图表
            setTimeout(() => {
              initNutrientLevelsChart();
              initQualityTrendsChart();
              initSoilQualityMap();
              initFactorContributionChart();
            }, 100);
          });
        } else {
          // 标准Web环境
          console.log('在标准Web环境中初始化图表');
          setTimeout(() => {
            initNutrientLevelsChart();
            initQualityTrendsChart();
            initSoilQualityMap();
            initFactorContributionChart();
          }, 100);
        }
      } catch (error) {
        console.error('图表初始化失败:', error);
        console.error('错误堆栈:', error.stack);
      }
    };
    
    // 更新地区数据
    const updateRegion = (e) => {
      const region = e.detail ? e.detail.value : e.target.value;
      const regions = ['全国', '华北', '东北', '华东', '中南', '西南', '西北'];
      currentRegion.value = regions[region] || '全国';
      console.log(`更新地区为: ${currentRegion.value}`);
      
      // 在实际应用中这里应该重新加载该地区的数据
      // 示例中简单更新标题
      for (const key in chartInstances.value) {
        if (chartInstances.value[key]) {
          chartInstances.value[key].setOption({
            title: {
              text: chartInstances.value[key].getOption().title[0].text,
              subtext: `${currentRegion.value} ${currentYear.value}年`
            }
          });
        }
      }
    };
    
    // 更新年份数据
    const updateYear = (e) => {
      const year = e.detail ? e.detail.value : e.target.value;
      const years = ['2023', '2022', '2021', '2020', '2019'];
      currentYear.value = years[year] || '2023';
      console.log(`更新年份为: ${currentYear.value}`);
      
      // 在实际应用中这里应该重新加载该年份的数据
      for (const key in chartInstances.value) {
        if (chartInstances.value[key]) {
          chartInstances.value[key].setOption({
            title: {
              text: chartInstances.value[key].getOption().title[0].text,
              subtext: `${currentRegion.value} ${currentYear.value}年`
            }
          });
        }
      }
    };
    
    // 窗口大小变化处理
    const handleResize = () => {
      console.log('窗口大小变化，调整图表大小');
        for (const key in chartInstances.value) {
          if (chartInstances.value[key]) {
            chartInstances.value[key].resize();
          }
        }
    };
    
    onMounted(async () => {
      console.log('土壤评估分析页面已挂载');
      
      // 先加载数据
      await loadAssessmentData();
      
      // 初始化各个图表
      initCharts();
      
      // 添加窗口大小变化事件监听
      window.addEventListener('resize', handleResize);
      
      // 监听采样点数据事件
      uni.$on('soil-sample-data', (data) => {
        console.log('接收到采样点数据:', data);
        // 将采样点数据转化为当前页面所需格式
        if (data) {
          // 更新页面标题
          document.title = `${data.name} - 土壤分析报告`;
          
          // 可以根据传入的region设置当前区域
          if (data.region) {
            // 提取区域，例如从"北京市海淀区"提取"北京市"
            const regionMatch = data.region.match(/^([\u4e00-\u9fa5]{2,3}市)/);
            if (regionMatch && regionMatch[1]) {
              currentRegion.value = regionMatch[1];
            } else {
              currentRegion.value = '全国';
            }
          }
          
          // 更新养分水平图表
          const nutrientData = [
            { name: '氮含量', value: data.nitrogen, max: 200, evaluation: data.nitrogenEvaluation || '' },
            { name: '磷含量', value: data.phosphorus, max: 100, evaluation: data.phosphorusEvaluation || '' },
            { name: '钾含量', value: data.potassium, max: 200, evaluation: data.potassiumEvaluation || '' },
            { name: 'pH值', value: data.ph, max: 14, evaluation: data.phEvaluation || '' },
            { name: '有机质', value: data.organic, max: 5, evaluation: data.organicEvaluation || '' }
          ];
          
          // 生成一个包含当前采样点数据和模拟历史数据的数组
          const historicalTrendData = generateHistoricalData(data);
          
          // 更新图表数据
          setTimeout(() => {
            updateChartsWithSampleData(nutrientData, historicalTrendData, data);
          }, 300);
        }
      });
    });
    
    // 生成模拟历史数据
    const generateHistoricalData = (currentData) => {
      // 基于当前数据生成模拟的历史趋势
      const years = ['2019', '2020', '2021', '2022', '2023'];
      const result = {
        years: years,
        nitrogen: [],
        phosphorus: [],
        potassium: [],
        ph: [],
        organic: []
      };
      
      // 逐步降低，模拟历年数据
      for (let i = 0; i < years.length; i++) {
        const factor = i / (years.length - 1); // 0到1的系数
        
        // 当i=years.length-1时（即2023年），使用当前值
        // 其他年份根据factor计算模拟值（较老的数据取值较低）
        if (i === years.length - 1) {
          result.nitrogen.push(currentData.nitrogen);
          result.phosphorus.push(currentData.phosphorus);
          result.potassium.push(currentData.potassium);
          result.ph.push(currentData.ph);
          result.organic.push(currentData.organic);
        } else {
          // 模拟历史数据：假设养分含量逐年提高
          result.nitrogen.push(Math.round(currentData.nitrogen * (0.7 + 0.3 * factor)));
          result.phosphorus.push(Math.round(currentData.phosphorus * (0.75 + 0.25 * factor)));
          result.potassium.push(Math.round(currentData.potassium * (0.8 + 0.2 * factor)));
          // pH值范围通常在5.5-8之间波动
          const phBase = currentData.ph > 7 ? (currentData.ph - 0.5) : (currentData.ph + 0.5);
          result.ph.push(Number((phBase * (0.95 + 0.05 * Math.random())).toFixed(1)));
          // 有机质含量
          result.organic.push(Number((currentData.organic * (0.85 + 0.15 * factor)).toFixed(1)));
        }
      }
      
      return result;
    };
    
    // 使用采样点数据更新图表
    const updateChartsWithSampleData = (nutrientData, historicalData, sampleData) => {
      // 更新营养水平图
      if (chartInstances.value.nutrientLevels) {
        const option = {
          title: {
            text: '土壤养分水平分析',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            formatter: function(params) {
              const param = params[0];
              return `${param.name}: ${param.value} ${param.name === 'pH值' ? '' : 'mg/kg'}<br/>${nutrientData.find(item => item.name === param.name)?.evaluation || ''}`;
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: nutrientData.map(item => item.name)
          },
          yAxis: {
            type: 'value',
            max: function(value) {
              return Math.ceil(value.max * 1.2);
            }
          },
          series: [
            {
              name: '养分含量',
              type: 'bar',
              data: nutrientData.map(item => ({
                name: item.name,
                value: item.value,
                itemStyle: {
                  color: getColorForNutrient(item.name, item.value)
                }
              })),
              label: {
                show: true,
                position: 'top',
                formatter: '{c}'
              }
            }
          ]
        };
        chartInstances.value.nutrientLevels.setOption(option);
      }
      
      // 更新质量趋势图
      if (chartInstances.value.qualityTrends) {
        const option = {
          title: {
            text: '土壤养分趋势 (2019-2023)',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['氮含量', '磷含量', '钾含量', 'pH值', '有机质'],
            bottom: 10
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '15%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: historicalData.years
          },
          yAxis: [
            {
              type: 'value',
              name: '养分含量 (mg/kg)',
              min: 0,
              max: 200,
              position: 'left'
            },
            {
              type: 'value',
              name: 'pH值 / 有机质(%)',
              min: 0,
              max: 14,
              position: 'right'
            }
          ],
          series: [
            {
              name: '氮含量',
              type: 'line',
              data: historicalData.nitrogen,
              smooth: true,
              lineStyle: { width: 3 },
              itemStyle: { color: '#ff6b6b' }
            },
            {
              name: '磷含量',
              type: 'line',
              data: historicalData.phosphorus,
              smooth: true,
              lineStyle: { width: 3 },
              itemStyle: { color: '#48dbfb' }
            },
            {
              name: '钾含量',
              type: 'line',
              data: historicalData.potassium,
              smooth: true,
              lineStyle: { width: 3 },
              itemStyle: { color: '#1dd1a1' }
            },
            {
              name: 'pH值',
              type: 'line',
              yAxisIndex: 1,
              data: historicalData.ph,
              smooth: true,
              lineStyle: { width: 3 },
              itemStyle: { color: '#feca57' }
            },
            {
              name: '有机质',
              type: 'line',
              yAxisIndex: 1,
              data: historicalData.organic,
              smooth: true,
              lineStyle: { width: 3 },
              itemStyle: { color: '#a29bfe' }
            }
          ]
        };
        chartInstances.value.qualityTrends.setOption(option);
      }
      
      // 更新土壤质量地图 - 简化为显示当前样点的质量等级
      if (chartInstances.value.soilQualityMap) {
        // 为当前区域分配一个质量评级
        const overallScore = calculateOverallScore(sampleData);
        const regionData = [
          { 
            name: currentRegion.value, 
            value: overallScore,
            quality: getQualityLevelFromScore(overallScore)
          }
        ];
        
        const option = {
          title: {
            text: '土壤质量分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: function(params) {
              if (params.data) {
                return `${params.name}<br/>质量得分: ${params.data.value}<br/>评级: ${params.data.quality}`;
              }
              return params.name;
            }
          },
          visualMap: {
            min: 0,
            max: 100,
            left: 'left',
            top: 'bottom',
            text: ['优', '差'],
            calculable: true,
            inRange: {
              color: ['#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027']
            }
          },
          series: [
            {
              name: '土壤质量评级',
              type: 'map',
              map: 'china',
              roam: true,
              data: regionData,
              itemStyle: {
                areaColor: '#f3f3f3',
                borderColor: '#ccc'
              },
              emphasis: {
                itemStyle: {
                  areaColor: '#cce8ff'
                }
              },
              select: {
                itemStyle: {
                  areaColor: '#cce8ff'
                }
              }
            }
          ]
        };
        chartInstances.value.soilQualityMap.setOption(option);
      }
      
      // 更新影响因子图
      if (chartInstances.value.factorContribution) {
        // 计算各因子得分占比
        const factors = [
          { name: 'pH值', score: calculateFactorScore('ph', sampleData.ph) },
          { name: '氮含量', score: calculateFactorScore('nitrogen', sampleData.nitrogen) },
          { name: '磷含量', score: calculateFactorScore('phosphorus', sampleData.phosphorus) },
          { name: '钾含量', score: calculateFactorScore('potassium', sampleData.potassium) },
          { name: '有机质', score: calculateFactorScore('organic', sampleData.organic) }
        ];
        
        const option = {
          title: {
            text: '土壤质量影响因素分析',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c}分 ({d}%)'
          },
          legend: {
            bottom: 10,
            data: factors.map(item => item.name)
          },
          series: [
            {
              name: '影响因素',
              type: 'pie',
              radius: ['30%', '60%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: true,
                formatter: '{b}: {c}分'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: 14,
                  fontWeight: 'bold'
                }
              },
              data: factors.map(item => ({
                name: item.name,
                value: item.score,
                itemStyle: {
                  color: getColorForFactor(item.name)
                }
              }))
            }
          ]
        };
        chartInstances.value.factorContribution.setOption(option);
      }
    };
    
    // 计算综合得分
    const calculateOverallScore = (data) => {
      let score = 0;
      
      // pH值评分 (满分25分)
      if (data.ph >= 6.5 && data.ph <= 7.5) score += 25;
      else if ((data.ph >= 5.5 && data.ph < 6.5) || (data.ph > 7.5 && data.ph <= 8.0)) score += 15;
      else score += 5;
      
      // 养分评分 (每项满分15分)
      if (data.nitrogen >= 80) score += 15;
      else if (data.nitrogen >= 50) score += 10;
      else score += 5;
      
      if (data.phosphorus >= 50) score += 15;
      else if (data.phosphorus >= 30) score += 10;
      else score += 5;
      
      if (data.potassium >= 100) score += 15;
      else if (data.potassium >= 70) score += 10;
      else score += 5;
      
      // 有机质评分 (满分30分)
      if (data.organic >= 2.5) score += 30;
      else if (data.organic >= 1.5) score += 20;
      else score += 10;
      
      return score;
    };
    
    // 计算各因子得分
    const calculateFactorScore = (factor, value) => {
      switch (factor) {
        case 'ph':
          if (value >= 6.5 && value <= 7.5) return 25;
          else if ((value >= 5.5 && value < 6.5) || (value > 7.5 && value <= 8.0)) return 15;
          else return 5;
        case 'nitrogen':
          if (value >= 80) return 15;
          else if (value >= 50) return 10;
          else return 5;
        case 'phosphorus':
          if (value >= 50) return 15;
          else if (value >= 30) return 10;
          else return 5;
        case 'potassium':
          if (value >= 100) return 15;
          else if (value >= 70) return 10;
          else return 5;
        case 'organic':
          if (value >= 2.5) return 30;
          else if (value >= 1.5) return 20;
          else return 10;
        default:
          return 0;
      }
    };
    
    // 根据得分获取质量等级
    const getQualityLevelFromScore = (score) => {
      if (score >= 85) return '优质';
      if (score >= 70) return '良好';
      if (score >= 50) return '中等';
      return '较差';
    };
    
    // 获取养分指标的颜色
    const getColorForNutrient = (nutrient, value) => {
      switch (nutrient) {
        case '氮含量':
          return value < 50 ? '#ff9f43' : (value < 80 ? '#1dd1a1' : '#ff6b6b');
        case '磷含量':
          return value < 30 ? '#ff9f43' : (value < 50 ? '#1dd1a1' : '#48dbfb');
        case '钾含量':
          return value < 70 ? '#ff9f43' : (value < 100 ? '#1dd1a1' : '#1dd1a1');
        case 'pH值':
          return (value < 5.5 || value > 7.5) ? '#ff9f43' : '#feca57';
        case '有机质':
          return value < 1.5 ? '#ff9f43' : (value < 2.5 ? '#1dd1a1' : '#a29bfe');
        default:
          return '#1dd1a1';
      }
    };
    
    // 获取因子的颜色
    const getColorForFactor = (factor) => {
      switch (factor) {
        case 'pH值': return '#feca57';
        case '氮含量': return '#ff6b6b';
        case '磷含量': return '#48dbfb';
        case '钾含量': return '#1dd1a1';
        case '有机质': return '#a29bfe';
        default: return '#999';
      }
    };
    
    // 组件卸载前清理
    onBeforeUnmount(() => {
      // 移除事件监听
      window.removeEventListener('resize', handleResize);
      // 移除采样点数据事件监听
      uni.$off('soil-sample-data');
      
      // 销毁图表实例
      Object.values(chartInstances.value).forEach(chart => {
        chart && chart.dispose();
      });
    });
    
    return {
      nutrientLevelsRef,
      qualityTrendsRef,
      soilQualityMapRef,
      factorContributionRef,
      currentRegion,
      currentYear,
      updateRegion,
      updateYear
    };
  }
};
</script>

<template>
  <view class="assessment-page">
    <view class="page-header">
      <view class="back-button" @click="goBack">
        <text class="icon">‹</text>
        <text>返回</text>
      </view>
      <text class="page-title">土壤健康评估报告</text>
      <view class="header-actions">
        <button class="action-btn refresh-btn" @click="refreshData">刷新数据</button>
        <button class="action-btn export-btn" @click="exportReport">导出报告</button>
      </view>
    </view>

    <scroll-view scroll-y class="page-content">
      <!-- 基本信息与总览 -->
      <view class="card data-overview-card">
        <view class="card-header">
          <text class="card-title">评估总览</text>
        </view>
        <view class="card-body">
          <view class="overview-item">
            <text class="label">评估区域:</text>
            <text class="value">{{ currentRegion }}</text>
          </view>
          <view class="overview-item">
            <text class="label">评估年份:</text>
            <text class="value">{{ currentYear }}</text>
          </view>
          <view class="overview-item">
            <text class="label">综合健康指数:</text>
            <text class="value score excellent">85分 (优)</text> <!-- 示例数据 -->
          </view>
          <view class="overview-summary">
            <text>该区域土壤健康状况总体良好，各项养分指标均衡，适宜多种作物生长。建议继续保持科学种植和养护措施。</text> <!-- 示例数据 -->
          </view>
        </view>
      </view>

      <!-- 图表展示区 -->
      <view class="charts-grid">
        <view class="card chart-card">
          <view class="card-header">
            <text class="card-title">土壤养分水平</text>
          </view>
          <view class="card-body chart-container-wrapper">
            <view class="nutrient-levels-chart" ref="nutrientLevelsRef" style="width: 100%; height: 300px;"></view>
          </view>
        </view>

        <view class="card chart-card">
          <view class="card-header">
            <text class="card-title">土壤质量历年趋势</text>
          </view>
          <view class="card-body chart-container-wrapper">
            <view class="quality-trends-chart" ref="qualityTrendsRef" style="width: 100%; height: 300px;"></view>
          </view>
        </view>

        <view class="card chart-card">
          <view class="card-header">
            <text class="card-title">土壤质量分级分布</text>
          </view>
          <view class="card-body chart-container-wrapper">
            <view class="soil-quality-map-chart" ref="soilQualityMapRef" style="width: 100%; height: 300px;"></view>
          </view>
        </view>
        
        <view class="card chart-card">
          <view class="card-header">
            <text class="card-title">影响因素贡献度</text> <!-- 假设的第四个图表 -->
          </view>
          <view class="card-body chart-container-wrapper">
            <view class="factor-contribution-chart" ref="factorContributionRef" style="width: 100%; height: 300px;"></view>
          </view>
        </view>
      </view>

      <!-- 详细解读与建议 -->
      <view class="card recommendations-card">
        <view class="card-header">
          <text class="card-title">详细解读与优化建议</text>
        </view>
        <view class="card-body">
          <view class="recommendation-section">
            <text class="section-title">1. 养分均衡性解读</text>
            <text class="section-content">当前土壤氮、磷、钾养分较为均衡，有机质含量中等偏上。pH值处于适宜范围，有利于养分吸收。微量元素含量正常。</text>
          </view>
          <view class="recommendation-section">
            <text class="section-title">2. 土壤结构与活性</text>
            <text class="section-content">土壤团粒结构良好，通气透水性适中。微生物活性较高，有利于有机物分解和养分转化。</text>
          </view>
          <view class="recommendation-section">
            <text class="section-title">3. 优化建议</text>
            <ul class="recommendation-list">
              <li>建议增施生物有机肥，进一步提升土壤有机质含量和微生物多样性。</li>
              <li>根据作物品种和生育期，适量补充中微量元素肥料，防止潜在缺乏。</li>
              <li>推广保护性耕作措施，如秸秆还田、少免耕，减少水土流失，培肥地力。</li>
              <li>定期进行土壤检测，跟踪养分动态变化，实现精准施肥。</li>
            </ul>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<style>
.assessment-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f4f7f9;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 15px;
  background-color: #ffffff;
  border-bottom: 1px solid #e0e0e0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.back-button {
  display: flex;
  align-items: center;
  color: #4d7bce;
  font-size: 15px;
  cursor: pointer;
  padding: 5px;
}

.back-button .icon {
  font-size: 22px;
  margin-right: 3px;
  font-weight: bold;
}

.page-title {
  font-size: 17px;
  font-weight: bold;
  color: #333;
  text-align: center;
  flex-grow: 1;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  font-size: 13px;
  padding: 6px 12px;
  border-radius: 4px;
  border: 1px solid #4d7bce;
  background-color: #4d7bce;
  color: white;
  cursor: pointer;
}

.action-btn.refresh-btn {
  background-color: #eaf2ff;
  color: #4d7bce;
}

.page-content {
  flex-grow: 1;
  padding: 15px;
  overflow-y: auto;
}

.card {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  margin-bottom: 15px;
  overflow: hidden; /* Ensures card styling contains its children */
}

.card-header {
  padding: 12px 15px;
  border-bottom: 1px solid #f0f0f0;
}

.card-title {
  font-size: 16px;
  font-weight: 600; /* Semi-bold */
  color: #3f51b5; /* Indigo color for titles */
}

.card-body {
  padding: 15px;
}

/* Data Overview Card Styles */
.data-overview-card .overview-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  font-size: 14px;
}
.data-overview-card .label {
  color: #555;
}
.data-overview-card .value {
  color: #333;
  font-weight: 500;
}
.data-overview-card .value.score {
  font-size: 15px;
  font-weight: bold;
}
.value.excellent { color: #4caf50; } /* Green for excellent */
.value.good { color: #8bc34a; }    /* Light Green for good */
.value.medium { color: #ffc107; }  /* Amber for medium */
.value.poor { color: #f44336; }    /* Red for poor */

.overview-summary {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #eee;
  font-size: 13px;
  color: #666;
  line-height: 1.6;
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 15px;
}

.chart-card .card-body {
  padding: 10px;
}

.chart-container-wrapper {
  /* Ensures the chart container itself doesn't add extra padding if chart has its own */
  padding: 0;
}

/* Recommendations Card Styles */
.recommendations-card .section-title {
  font-size: 15px;
  font-weight: 500;
  color: #555;
  margin-bottom: 8px;
  display: block;
}

.recommendations-card .section-content {
  font-size: 14px;
  color: #666;
  line-height: 1.7;
  margin-bottom: 15px;
}

.recommendations-card .recommendation-list {
  list-style: disc;
  padding-left: 20px;
  font-size: 14px;
  color: #666;
  line-height: 1.7;
}

.recommendations-card .recommendation-list li {
  margin-bottom: 6px;
}
</style> 