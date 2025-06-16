<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as echarts from 'echarts';

export default {
  name: 'HeatmapView',
  setup() {
    const mapContainer = ref(null);
    let chartInstance = null;
    
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
    
    // 生成模拟热力图数据
    const generateHeatmapData = (nutrient, density = 'medium') => {
      console.log(`生成${nutrient}的热力图数据，密度:${density}`);
      // 基于密度设置点的数量
      const pointCounts = {
        'low': 200,
        'medium': 500,
        'high': 1000
      };
      
      const count = pointCounts[density] || pointCounts.medium;
      
      // 不同养分的数值范围
      const valueRanges = {
        '氮含量': [20, 100],
        '磷含量': [10, 80],
        '钾含量': [30, 150],
        '有机质': [0.5, 5],
        'pH值': [4, 9]
      };
      
      const range = valueRanges[nutrient] || [0, 100];
        
      // 生成随机数据点，但分布不是完全随机的
      // 我们让数据在某些区域集中以形成热点
        const data = [];
      
      // 添加一些热点区域
      const hotspots = [
        { lng: 113.5, lat: 23.0, radius: 3, bias: 0.8 }, // 广东区域
        { lng: 117.0, lat: 36.5, radius: 2.5, bias: 0.7 }, // 山东区域
        { lng: 118.5, lat: 33.0, radius: 2.5, bias: 0.7 }, // 江苏区域
        { lng: 104.0, lat: 30.5, radius: 2, bias: 0.6 }, // 四川区域
        { lng: 113.5, lat: 34.0, radius: 2.5, bias: 0.65 } // 河南区域
      ];
      
      for (let i = 0; i < count; i++) {
        let lng, lat, value;
        
        // 70%的点围绕热点生成，30%随机分布
        if (Math.random() < 0.7) {
          // 选择一个随机热点
          const hotspot = hotspots[Math.floor(Math.random() * hotspots.length)];
          
          // 在热点周围生成点
          const angle = Math.random() * Math.PI * 2;
          const distance = Math.random() * hotspot.radius;
          lng = hotspot.lng + Math.cos(angle) * distance;
          lat = hotspot.lat + Math.sin(angle) * distance;
          
          // 热点区域的值偏高
          const min = range[0] + (range[1] - range[0]) * hotspot.bias;
          value = min + Math.random() * (range[1] - min);
        } else {
          // 随机生成中国范围内的经纬度点
          lng = 100 + Math.random() * 30;
          lat = 20 + Math.random() * 20;
          value = range[0] + Math.random() * (range[1] - range[0]);
        }
        
          data.push([lng, lat, value]);
        }
      
      console.log(`生成了${data.length}个数据点`);
      return data;
    };
    
    // 初始化热力图
    const initHeatmap = (nutrient = '氮含量', year = '2023', density = 'medium') => {
      console.log('开始初始化热力图...');
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
          query.select('.map-chart').boundingClientRect();
          
          query.exec(function(res) {
            console.log('查询选择器结果:', res);
            
            if (!res || res.length < 1 || !res[0]) {
              console.error('热力图容器DOM元素未找到', res);
              // 延迟再次尝试
              setTimeout(() => initHeatmap(nutrient, year, density), 300);
              return;
            }
            
            console.log('热力图DOM元素已找到，开始初始化');
            console.log('容器尺寸:', { width: res[0].width, height: res[0].height });
            
            // 检查容器尺寸是否合理
            if (res[0].width < 10 || res[0].height < 10) {
              console.error('热力图容器尺寸太小:', res[0]);
              setTimeout(() => initHeatmap(nutrient, year, density), 300);
              return;
            }
            
            // 调用渲染函数
            renderChart(nutrient, year, density);
          });
        } else {
          // 标准Web环境
          console.log('在标准Web环境中初始化热力图');
          setTimeout(() => renderChart(nutrient, year, density), 0);
        }
      } catch (error) {
        console.error('热力图初始化失败:', error);
        console.error('错误堆栈:', error.stack);
      }
    };
    
    // 渲染热力图
    const renderChart = (nutrient, year, density) => {
      try {
        console.log(`渲染${nutrient}热力图，年份:${year}，密度:${density}`);
        
        // 获取DOM元素
        const mapEl = document.querySelector('.map-chart');
        if (!mapEl) {
          console.error('无法通过document.querySelector获取热力图元素');
          return;
        }
        
        // 清理之前的实例
        if (chartInstance) {
          console.log('销毁旧的图表实例');
          chartInstance.dispose();
        }
        
        // 创建新实例
        console.log('创建新的ECharts实例');
        chartInstance = echarts.init(mapEl);
        
        // 生成热力图数据
        const data = generateHeatmapData(nutrient, density);
        
        // 设置不同养分的值范围和颜色范围
        const visualRanges = {
          '氮含量': [0, 100],
          '磷含量': [0, 80],
          '钾含量': [0, 150],
          '有机质': [0, 5],
          'pH值': [4, 9]
        };
        
        const visualRange = visualRanges[nutrient] || [0, 100];
        
        // 为pH值使用不同的颜色范围
        let colorRange;
        if (nutrient === 'pH值') {
          colorRange = ['#a50026', '#d73027', '#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8', '#abd9e9', '#74add1', '#4575b4', '#313695'];
        } else {
          colorRange = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026'];
        }
        
        // 单位映射
        const unitMap = {
          '氮含量': 'mg/kg',
          '磷含量': 'mg/kg',
          '钾含量': 'mg/kg',
          '有机质': '%',
          'pH值': ''
        };
        
        // 设置地图配置项
        const option = {
          title: {
            text: '全国土壤养分热力图',
            subtext: `${nutrient}分布 (${year})`,
            left: 'center',
            textStyle: {
              fontSize: 16,
            }
          },
          tooltip: {
            trigger: 'item',
            formatter: function (params) {
              const unit = unitMap[nutrient] || '';
              return `位置: (${params.data[0].toFixed(2)}, ${params.data[1].toFixed(2)})<br>
                     ${nutrient}: ${params.data[2]} ${unit}`;
            }
          },
          visualMap: {
            min: visualRange[0],
            max: visualRange[1],
            calculable: true,
            inRange: {
              color: colorRange
            },
            textStyle: {
              color: '#333'
            },
            left: 'left',
            top: 'bottom'
          },
          geo: {
            map: 'china',
            roam: true,
            label: {
              emphasis: {
                show: true,
                color: '#333'
              }
            },
            zoom: 1.2,
            itemStyle: {
              normal: {
                areaColor: '#f3f3f3',
                borderColor: '#ddd'
              },
              emphasis: {
                areaColor: '#e6f7ff'
              }
            },
            scaleLimit: {
              min: 1,
              max: 5
            }
          },
          series: [
            {
              name: nutrient,
              type: 'heatmap',
              coordinateSystem: 'geo',
              data: data,
              pointSize: 8,
              blurSize: 12
            }
          ]
        };
        
        // 使用配置项设置地图
        console.log('设置热力图配置');
        chartInstance.setOption(option);
        console.log('热力图渲染完成');
        
        // 返回渲染后的图表实例
        return chartInstance;
      } catch (error) {
        console.error('热力图渲染失败:', error);
        console.error('错误堆栈:', error.stack);
      }
    };
    
    // 更新热力图数据
    const updateHeatmap = (nutrient, year, density = 'medium') => {
      console.log(`更新热力图: ${nutrient}, ${year}, ${density}`);
      
      if (!chartInstance) {
        // 如果图表实例不存在，初始化图表
        initHeatmap(nutrient, year, density);
        return;
      }
      
      try {
        // 生成新数据
        const data = generateHeatmapData(nutrient, density);
        
        // 设置不同养分的值范围
        const visualRanges = {
          '氮含量': [0, 100],
          '磷含量': [0, 80],
          '钾含量': [0, 150],
          '有机质': [0, 5],
          'pH值': [4, 9]
        };
        
        const visualRange = visualRanges[nutrient] || [0, 100];
        
        // 为pH值使用不同的颜色范围
        let colorRange;
        if (nutrient === 'pH值') {
          colorRange = ['#a50026', '#d73027', '#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8', '#abd9e9', '#74add1', '#4575b4', '#313695'];
        } else {
          colorRange = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026'];
        }
        
        // 单位映射
        const unitMap = {
          '氮含量': 'mg/kg',
          '磷含量': 'mg/kg',
          '钾含量': 'mg/kg',
          '有机质': '%',
          'pH值': ''
        };
        
        // 更新图表配置
        chartInstance.setOption({
          title: {
            text: '全国土壤养分热力图',
            subtext: `${nutrient}分布 (${year})`
          },
          tooltip: {
            formatter: function (params) {
              const unit = unitMap[nutrient] || '';
              return `位置: (${params.data[0].toFixed(2)}, ${params.data[1].toFixed(2)})<br>
                     ${nutrient}: ${params.data[2]} ${unit}`;
            }
          },
          visualMap: {
            min: visualRange[0],
            max: visualRange[1],
            inRange: {
              color: colorRange
            }
          },
          series: [
            {
              name: nutrient,
              data: data
            }
          ]
        });
        
        console.log('热力图数据更新完成');
      } catch (error) {
        console.error('更新热力图失败:', error);
        console.error('错误堆栈:', error.stack);
      }
    };
        
    // 刷新数据按钮事件处理
    const refreshData = () => {
      console.log('刷新热力图数据');
      
      // 获取当前选择的养分指标和年份
      const nutrientElement = document.querySelector('.nutrient-picker .picker-view');
      const yearElement = document.querySelector('.year-picker .picker-view');
      const densityElement = document.querySelector('.density-picker .picker-view');
      
      const nutrient = nutrientElement ? nutrientElement.innerText : '氮含量';
      const year = yearElement ? yearElement.innerText : '2023';
      const density = densityElement ? 
        { '低': 'low', '中': 'medium', '高': 'high' }[densityElement.innerText] : 'medium';
      
      updateHeatmap(nutrient, year, density);
    };
    
    // 窗口大小变化处理
    const handleResize = () => {
      if (chartInstance) {
        console.log('窗口大小变化，调整热力图大小');
        chartInstance.resize();
      }
    };
    
    onMounted(() => {
      console.log('热力图组件已挂载，准备初始化...');
      // 延迟一点初始化，确保DOM元素已渲染完成
      setTimeout(() => {
        initHeatmap('氮含量', '2023', 'medium');
      }, 500);
      
      // 添加窗口大小调整的事件监听器
      window.addEventListener('resize', handleResize);
      
      // 监听页面显示事件
      uni.$on('heatmap-shown', handleResize);
    });
    
    // 组件卸载前清理资源
    onBeforeUnmount(() => {
      console.log('热力图组件即将卸载，清理资源...');
      // 移除事件监听器
      window.removeEventListener('resize', handleResize);
      uni.$off('heatmap-shown');
      
      // 销毁图表实例
      if (chartInstance) {
        chartInstance.dispose();
        chartInstance = null;
      }
    });
    
    return {
      mapContainer,
      updateHeatmap,
      refreshData
    };
  }
};
</script>

<template>
  <view class="heatmap-container">
    <view class="heatmap-view">
      <view class="map-chart" ref="mapContainer" style="width: 100%; height: 500px; position: relative;"></view>
      
      <view class="control-panel">
        <view class="control-row">
          <view class="control-item nutrient-picker">
            <text class="label">养分指标:</text>
            <picker @change="(e) => updateHeatmap(nutrients[e.detail.value], selectedYear, selectedDensity)" :value="0" :range="nutrients">
              <view class="picker-view">{{selectedNutrient}}</view>
        </picker>
      </view>
      
          <view class="control-item year-picker">
            <text class="label">年份:</text>
            <picker @change="(e) => updateHeatmap(selectedNutrient, years[e.detail.value], selectedDensity)" :value="0" :range="years">
              <view class="picker-view">{{selectedYear}}</view>
        </picker>
      </view>
      
          <view class="control-item density-picker">
            <text class="label">数据密度:</text>
            <picker @change="(e) => updateHeatmap(selectedNutrient, selectedYear, ['low', 'medium', 'high'][e.detail.value])" :value="1" :range="['低', '中', '高']">
              <view class="picker-view">{{{'low': '低', 'medium': '中', 'high': '高'}[selectedDensity]}}</view>
        </picker>
      </view>
      
          <view class="control-item">
            <button class="refresh-btn" @click="refreshData">刷新数据</button>
          </view>
    </view>
      </view>
      
      <view class="data-panel">
        <view class="panel-title">
          <text>热点信息</text>
        </view>
        <view class="hotspot-list">
          <view class="hotspot-item">
            <text class="region">广东区域</text>
            <text class="value">平均值: {{averageValues['广东']}}</text>
          </view>
          <view class="hotspot-item">
            <text class="region">山东区域</text>
            <text class="value">平均值: {{averageValues['山东']}}</text>
          </view>
          <view class="hotspot-item">
            <text class="region">江苏区域</text>
            <text class="value">平均值: {{averageValues['江苏']}}</text>
          </view>
          <view class="hotspot-item">
            <text class="region">四川区域</text>
            <text class="value">平均值: {{averageValues['四川']}}</text>
          </view>
          <view class="hotspot-item">
            <text class="region">河南区域</text>
            <text class="value">平均值: {{averageValues['河南']}}</text>
            </view>
          </view>
        </view>
        
      <view class="legend-panel">
        <view class="panel-title">
          <text>图例说明</text>
        </view>
        <view class="legend-content">
          <view class="legend-color-scale">
            <view class="color-bar" :style="{
              background: selectedNutrient === 'pH值' 
                ? 'linear-gradient(to right, #a50026, #d73027, #f46d43, #fdae61, #fee090, #ffffbf, #e0f3f8, #abd9e9, #74add1, #4575b4, #313695)' 
                : 'linear-gradient(to right, #313695, #4575b4, #74add1, #abd9e9, #e0f3f8, #ffffbf, #fee090, #fdae61, #f46d43, #d73027, #a50026)'
            }"></view>
            <view class="scale-labels">
              <text>{{visualRanges[selectedNutrient][0]}}</text>
              <text>{{visualRanges[selectedNutrient][1]}}</text>
            </view>
          </view>
          <view class="legend-notes">
            <view class="note-item" v-if="selectedNutrient === '氮含量'">
              <text>氮含量(N): 土壤中的氮元素含量，单位为mg/kg，是植物生长的重要元素。</text>
            </view>
            <view class="note-item" v-if="selectedNutrient === '磷含量'">
              <text>磷含量(P): 土壤中的磷元素含量，单位为mg/kg，影响植物的根系发育和开花结果。</text>
            </view>
            <view class="note-item" v-if="selectedNutrient === '钾含量'">
              <text>钾含量(K): 土壤中的钾元素含量，单位为mg/kg，增强植物的抗病虫害能力。</text>
            </view>
            <view class="note-item" v-if="selectedNutrient === '有机质'">
              <text>有机质: 土壤中的有机物质含量，单位为%，影响土壤结构和肥力。</text>
            </view>
            <view class="note-item" v-if="selectedNutrient === 'pH值'">
              <text>pH值: 土壤酸碱度，影响养分的有效性和微生物活动。</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<style lang="scss">
.heatmap-container {
  padding: 15px;
  background-color: #f5f7fa;
  
  .heatmap-view {
    display: flex;
    flex-direction: column;
    gap: 15px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    padding: 15px;
    
    .map-chart {
      border: 1px solid #e8e8e8;
      border-radius: 4px;
      overflow: hidden;
    }
    
    .control-panel {
      background-color: #f8f9fb;
      border-radius: 6px;
      padding: 12px;
      margin-bottom: 10px;
      
      .control-row {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
        align-items: center;
        
        .control-item {
          flex: 1;
          min-width: 120px;
  display: flex;
          align-items: center;

          .label {
  font-size: 14px;
            color: #606266;
            margin-right: 8px;
            white-space: nowrap;
}

.picker-view {
            background-color: #fff;
            border: 1px solid #dcdfe6;
  border-radius: 4px;
            padding: 6px 12px;
            font-size: 14px;
            color: #303133;
            width: 100%;
            text-align: center;
          }
}

.refresh-btn {
          background-color: #409eff;
          color: white;
          border: none;
  border-radius: 4px;
          padding: 6px 16px;
          font-size: 14px;
          
          &:active {
            background-color: #3a8ee6;
          }
        }
      }
}

    .data-panel, .legend-panel {
      background-color: #f8f9fb;
      border-radius: 6px;
  padding: 15px;
      margin-bottom: 10px;

.panel-title {
  font-size: 16px;
        font-weight: 600;
        color: #303133;
        margin-bottom: 10px;
        padding-bottom: 8px;
        border-bottom: 1px solid #ebeef5;
      }
}

.hotspot-list {
      display: flex;
      flex-wrap: wrap;
      gap: 15px;

.hotspot-item {
        background-color: #fff;
        border-radius: 4px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  flex: 1;
        min-width: 150px;
  display: flex;
  flex-direction: column;
        
        .region {
          font-weight: 600;
          color: #303133;
  margin-bottom: 5px;
}

        .value {
          color: #606266;
  font-size: 14px;
        }
      }
}

    .legend-content {
      .legend-color-scale {
        margin-bottom: 15px;

.color-bar {
  height: 20px;
  width: 100%;
  border-radius: 4px;
  margin-bottom: 5px;
}

.scale-labels {
  display: flex;
  justify-content: space-between;

          text {
  font-size: 12px;
            color: #606266;
          }
        }
}

.legend-notes {
        .note-item {
          margin-bottom: 8px;
          
          text {
  font-size: 14px;
            color: #606266;
            line-height: 1.5;
}
        }
      }
    }
  }
}
</style> 