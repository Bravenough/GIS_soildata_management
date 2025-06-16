<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'ComparisonView',
  setup() {
    // 图表容器引用
    const comparisonChartRef = ref(null);
    const radarChartRef = ref(null);
    const diffChartRef = ref(null);
    
    // 选择的区域和年份
    const selectedRegions = ref(['华北平原', '东北平原', '长江中下游平原', '珠江三角洲']);
    const selectedYears = ref(['2023', '2022']);
    const selectedNutrient = ref('氮含量');
    
    // 图表实例
    const chartInstances = ref({
      comparison: null,
      radar: null,
      diff: null
    });
    
    // 初始化对比柱状图
    const initComparisonChart = () => {
      if (window.echarts && comparisonChartRef.value) {
        chartInstances.value.comparison = window.echarts.init(comparisonChartRef.value);
        
        const option = {
          title: {
            text: '各区域土壤氮含量对比',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          legend: {
            data: ['2023年', '2022年'],
            bottom: '0%'
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '10%',
            top: '15%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: selectedRegions.value
          },
          yAxis: {
            type: 'value',
            name: 'mg/kg',
            nameLocation: 'end'
          },
          series: [
            {
              name: '2023年',
              type: 'bar',
              data: [75, 68, 82, 95],
              itemStyle: {
                color: '#4e79a7'
              }
            },
            {
              name: '2022年',
              type: 'bar',
              data: [68, 65, 78, 85],
              itemStyle: {
                color: '#76b7b2'
              }
            }
          ]
        };
        
        chartInstances.value.comparison.setOption(option);
      }
    };
    
    // 初始化雷达图
    const initRadarChart = () => {
      if (window.echarts && radarChartRef.value) {
        chartInstances.value.radar = window.echarts.init(radarChartRef.value);
        
        const option = {
          title: {
            text: '土壤养分全面对比',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            data: selectedRegions.value,
            bottom: '0%'
          },
          radar: {
            indicator: [
              { name: '氮含量', max: 100 },
              { name: '磷含量', max: 100 },
              { name: '钾含量', max: 100 },
              { name: '有机质', max: 100 },
              { name: 'pH值', max: 14 }
            ],
            center: ['50%', '50%'],
            radius: '65%'
          },
          series: [
            {
              type: 'radar',
              data: [
                {
                  value: [75, 60, 85, 70, 7.5],
                  name: '华北平原',
                  areaStyle: {
                    opacity: 0.1
                  },
                  lineStyle: {
                    width: 2
                  }
                },
                {
                  value: [68, 55, 80, 65, 6.8],
                  name: '东北平原',
                  areaStyle: {
                    opacity: 0.1
                  },
                  lineStyle: {
                    width: 2
                  }
                },
                {
                  value: [82, 70, 75, 80, 6.2],
                  name: '长江中下游平原',
                  areaStyle: {
                    opacity: 0.1
                  },
                  lineStyle: {
                    width: 2
                  }
                },
                {
                  value: [95, 75, 70, 85, 5.8],
                  name: '珠江三角洲',
                  areaStyle: {
                    opacity: 0.1
                  },
                  lineStyle: {
                    width: 2
                  }
                }
              ]
            }
          ]
        };
        
        chartInstances.value.radar.setOption(option);
      }
    };
    
    // 初始化差异图表
    const initDiffChart = () => {
      if (window.echarts && diffChartRef.value) {
        chartInstances.value.diff = window.echarts.init(diffChartRef.value);
        
        const option = {
          title: {
            text: '年度变化趋势',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross'
            }
          },
          legend: {
            data: selectedRegions.value,
            bottom: '0%'
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '10%',
            top: '15%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: ['2019', '2020', '2021', '2022', '2023'],
            boundaryGap: false
          },
          yAxis: {
            type: 'value',
            name: 'mg/kg',
            axisLabel: {
              formatter: '{value}'
            }
          },
          series: [
            {
              name: '华北平原',
              type: 'line',
              data: [55, 60, 65, 68, 75],
              smooth: true,
              lineStyle: {
                width: 3
              }
            },
            {
              name: '东北平原',
              type: 'line',
              data: [50, 55, 60, 65, 68],
              smooth: true,
              lineStyle: {
                width: 3
              }
            },
            {
              name: '长江中下游平原',
              type: 'line',
              data: [65, 70, 75, 78, 82],
              smooth: true,
              lineStyle: {
                width: 3
              }
            },
            {
              name: '珠江三角洲',
              type: 'line',
              data: [72, 78, 82, 85, 95],
              smooth: true,
              lineStyle: {
                width: 3
              }
            }
          ]
        };
        
        chartInstances.value.diff.setOption(option);
      }
    };
    
    // 更新图表数据
    const updateCharts = () => {
      // 这里应该是从API获取数据并更新图表
      // 以下是示例代码，实际应用中应根据选择的区域、年份和养分类型进行查询
      if (chartInstances.value.comparison) {
        chartInstances.value.comparison.setOption({
          title: {
            text: `各区域土壤${selectedNutrient.value}对比`
          },
          xAxis: {
            data: selectedRegions.value
          },
          legend: {
            data: selectedYears.value
          }
          // 更新series数据...
        });
      }
      
      // 同样更新其他图表...
    };
    
    // 添加或移除对比区域
    const toggleRegion = (region) => {
      const index = selectedRegions.value.indexOf(region);
      if (index > -1) {
        selectedRegions.value.splice(index, 1);
      } else {
        selectedRegions.value.push(region);
      }
      updateCharts();
    };
    
    // 更改所选养分类型
    const changeNutrient = (nutrient) => {
      selectedNutrient.value = nutrient;
      updateCharts();
    };
    
    // 组件挂载时初始化图表
    onMounted(() => {
      // 延迟一点初始化，确保DOM已经渲染完成
      setTimeout(() => {
        initComparisonChart();
        initRadarChart();
        initDiffChart();
        
        // 添加窗口大小调整的事件监听器
        window.addEventListener('resize', () => {
          Object.values(chartInstances.value).forEach(chart => {
            if (chart) {
              chart.resize();
            }
          });
        });
      }, 100);
    });
    
    return {
      comparisonChartRef,
      radarChartRef,
      diffChartRef,
      selectedRegions,
      selectedYears,
      selectedNutrient,
      toggleRegion,
      changeNutrient
    };
  }
};
</script>

<template>
  <view class="page-container" id="comparison-page">
    <view class="page-header">
      <text class="header-title">土壤数据对比分析</text>
    </view>
    
    <view class="control-bar">
      <view class="control-section">
        <text class="section-label">选择区域：</text>
        <view class="region-chips">
          <view 
            v-for="region in ['华北平原', '东北平原', '长江中下游平原', '珠江三角洲', '四川盆地', '西北地区']" 
            :key="region"
            class="chip"
            :class="{ active: selectedRegions.includes(region) }"
            @click="toggleRegion(region)"
          >
            <text>{{ region }}</text>
          </view>
        </view>
      </view>
      
      <view class="control-section">
        <text class="section-label">养分指标：</text>
        <view class="nutrient-selector">
          <picker @change="(e) => changeNutrient(e.target.value)" :range="['氮含量', '磷含量', '钾含量', '有机质', 'pH值']">
            <view class="picker-view">{{ selectedNutrient }}</view>
          </picker>
        </view>
      </view>
      
      <view class="control-section">
        <text class="section-label">对比年份：</text>
        <view class="year-selector">
          <checkbox-group>
            <label class="checkbox-label" v-for="year in ['2023', '2022', '2021', '2020']" :key="year">
              <checkbox :value="year" :checked="selectedYears.includes(year)" />
              <text>{{ year }}</text>
            </label>
          </checkbox-group>
        </view>
      </view>
    </view>
    
    <view class="charts-container">
      <view class="chart-card">
        <view class="chart-header">
          <text class="chart-title">区域氮含量对比</text>
        </view>
        <view class="chart-content">
          <view class="chart-area" ref="comparisonChartRef"></view>
        </view>
      </view>
      
      <view class="chart-card">
        <view class="chart-header">
          <text class="chart-title">养分雷达对比</text>
        </view>
        <view class="chart-content">
          <view class="chart-area" ref="radarChartRef"></view>
        </view>
      </view>
      
      <view class="chart-card">
        <view class="chart-header">
          <text class="chart-title">历年变化趋势</text>
        </view>
        <view class="chart-content">
          <view class="chart-area" ref="diffChartRef"></view>
        </view>
      </view>
    </view>
    
    <view class="comparison-results">
      <view class="results-header">
        <text class="section-title">对比结果分析</text>
      </view>
      
      <view class="results-content">
        <view class="result-item">
          <text class="result-title">区域差异</text>
          <text class="result-desc">珠江三角洲地区氮含量显著高于其他区域，比华北平原高出26.7%，比东北平原高出39.7%。这与该地区密集的农业活动和气候条件有关。</text>
        </view>
        
        <view class="result-item">
          <text class="result-title">年度变化</text>
          <text class="result-desc">从2019年到2023年，四个主要平原区域的氮含量均呈现稳定上升趋势，其中珠江三角洲的上升速度最快，年均增长率达到7.2%。</text>
        </view>
        
        <view class="result-item">
          <text class="result-title">养分平衡性</text>
          <text class="result-desc">从雷达图可以看出，珠江三角洲地区虽然氮含量最高，但pH值偏低，可能导致土壤酸化问题。华北平原各项养分指标较为平衡，土壤健康状况优于其他区域。</text>
        </view>
        
        <view class="result-item">
          <text class="result-title">改善建议</text>
          <text class="result-desc">珠江三角洲地区应减少氮肥施用，增加钙镁肥以调节pH值；东北平原需要补充有机质和磷肥；长江中下游平原应增加钾肥施用，提高土壤肥力。</text>
        </view>
      </view>
    </view>
    
    <view class="data-table">
      <view class="table-header">
        <text class="section-title">详细数据对比表</text>
      </view>
      
      <view class="table-scrollable">
        <view class="table">
          <view class="table-head">
            <view class="th">区域</view>
            <view class="th">年份</view>
            <view class="th">氮含量(mg/kg)</view>
            <view class="th">磷含量(mg/kg)</view>
            <view class="th">钾含量(mg/kg)</view>
            <view class="th">有机质(%)</view>
            <view class="th">pH值</view>
          </view>
          
          <view class="table-body">
            <view class="tr">
              <view class="td" rowspan="2">华北平原</view>
              <view class="td">2023</view>
              <view class="td">75</view>
              <view class="td">60</view>
              <view class="td">85</view>
              <view class="td">3.7</view>
              <view class="td">7.5</view>
            </view>
            
            <view class="tr">
              <view class="td">2022</view>
              <view class="td">68</view>
              <view class="td">58</view>
              <view class="td">82</view>
              <view class="td">3.5</view>
              <view class="td">7.4</view>
            </view>
            
            <view class="tr">
              <view class="td" rowspan="2">东北平原</view>
              <view class="td">2023</view>
              <view class="td">68</view>
              <view class="td">55</view>
              <view class="td">80</view>
              <view class="td">3.2</view>
              <view class="td">6.8</view>
            </view>
            
            <view class="tr">
              <view class="td">2022</view>
              <view class="td">65</view>
              <view class="td">52</view>
              <view class="td">78</view>
              <view class="td">3.0</view>
              <view class="td">6.7</view>
            </view>
            
            <view class="tr">
              <view class="td" rowspan="2">长江中下游平原</view>
              <view class="td">2023</view>
              <view class="td">82</view>
              <view class="td">70</view>
              <view class="td">75</view>
              <view class="td">4.0</view>
              <view class="td">6.2</view>
            </view>
            
            <view class="tr">
              <view class="td">2022</view>
              <view class="td">78</view>
              <view class="td">67</view>
              <view class="td">72</view>
              <view class="td">3.8</view>
              <view class="td">6.3</view>
            </view>
            
            <view class="tr">
              <view class="td" rowspan="2">珠江三角洲</view>
              <view class="td">2023</view>
              <view class="td">95</view>
              <view class="td">75</view>
              <view class="td">70</view>
              <view class="td">4.2</view>
              <view class="td">5.8</view>
            </view>
            
            <view class="tr">
              <view class="td">2022</view>
              <view class="td">85</view>
              <view class="td">72</view>
              <view class="td">68</view>
              <view class="td">4.0</view>
              <view class="td">5.9</view>
            </view>
          </view>
        </view>
      </view>
      
      <view class="download-section">
        <button class="btn" type="primary">导出完整对比数据</button>
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

.control-bar {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 15px;
  background-color: white;
  margin: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.control-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.section-label {
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.region-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chip {
  padding: 8px 15px;
  background-color: #f0f0f0;
  border-radius: 20px;
  font-size: 14px;
}

.chip.active {
  background-color: #007aff;
  color: white;
}

.nutrient-selector, .year-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.picker-view {
  padding: 8px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 120px;
  background-color: #f8f8f8;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-right: 15px;
}

.charts-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin: 15px;
}

.chart-card {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

.chart-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.chart-title {
  font-size: 16px;
  font-weight: bold;
}

.chart-content {
  padding: 15px;
}

.chart-area {
  height: 350px;
  width: 100%;
}

.comparison-results {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
  margin: 15px;
}

.results-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
}

.results-content {
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.result-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.result-title {
  font-weight: bold;
  font-size: 15px;
}

.result-desc {
  font-size: 14px;
  color: #555;
  line-height: 1.5;
}

.data-table {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
  margin: 15px;
}

.table-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.table-scrollable {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.th, .td {
  padding: 12px 15px;
  text-align: center;
  border: 1px solid #eee;
}

.th {
  background-color: #f8f8f8;
  font-weight: bold;
}

.tr:nth-child(even) {
  background-color: #fafafa;
}

.tr:hover {
  background-color: #f0f7ff;
}

.download-section {
  padding: 15px;
  display: flex;
  justify-content: center;
}

.btn {
  min-width: 200px;
}

/* 使用条件编译适配不同平台 */
</style> 