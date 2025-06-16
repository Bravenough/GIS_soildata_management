<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'DistributionView',
  setup() {
    const mapContainer = ref(null);
    const chartInstance = ref(null);
    
    // 初始化中国地图
    const initMap = () => {
      if (window.echarts && mapContainer.value) {
        const chartDom = mapContainer.value;
        chartInstance.value = window.echarts.init(chartDom);
        
        // 此处需要在实际实现时加载中国地图GeoJSON数据
        // 以下为简易示例
        const option = {
          title: {
            text: '全国土壤养分分布',
            subtext: '数据为示例，并非真实数据',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{b}<br/>氮含量: {c}'
          },
          visualMap: {
            min: 0,
            max: 100,
            text: ['高', '低'],
            realtime: false,
            calculable: true,
            inRange: {
              color: ['#f0f9e8', '#bae4bc', '#7bccc4', '#43a2ca', '#0868ac']
            }
          },
          series: [
            {
              name: '氮含量',
              type: 'map',
              map: 'china',
              label: {
                show: true
              },
              data: [
                {name: '北京', value: 85},
                {name: '天津', value: 78},
                {name: '上海', value: 65},
                {name: '重庆', value: 72},
                {name: '河北', value: 80},
                {name: '河南', value: 75},
                {name: '云南', value: 68},
                {name: '辽宁', value: 62},
                {name: '黑龙江', value: 45},
                {name: '湖南', value: 73},
                {name: '安徽', value: 71},
                {name: '山东', value: 82},
                {name: '江苏', value: 76},
                {name: '浙江', value: 77},
                {name: '江西', value: 70},
                {name: '湖北', value: 74},
                {name: '广西', value: 83},
                {name: '甘肃', value: 55},
                {name: '山西', value: 58},
                {name: '陕西', value: 60},
                {name: '吉林', value: 50},
                {name: '福建', value: 78},
                {name: '贵州', value: 65},
                {name: '广东', value: 95},
                {name: '青海', value: 42},
                {name: '西藏', value: 38},
                {name: '四川', value: 75},
                {name: '宁夏', value: 52},
                {name: '海南', value: 86},
                {name: '台湾', value: 80},
                {name: '香港', value: 83},
                {name: '澳门', value: 85}
              ]
            }
          ]
        };
        
        chartInstance.value.setOption(option);
        
        // 窗口大小调整处理
        window.addEventListener('resize', () => {
          if (chartInstance.value) {
            chartInstance.value.resize();
          }
        });
      }
    };
    
    onMounted(() => {
      // 延迟一点初始化，确保DOM已经渲染完成
      setTimeout(initMap, 100);
    });
    
    return {
      mapContainer
    };
  }
};
</script>

<template>
  <view class="page-container" id="distribution-page">
    <view class="page-header">
      <text class="header-title">各省土壤情况分布</text>
    </view>
    
    <view class="control-bar">
      <view class="control-group">
        <text>选择养分指标：</text>
        <picker class="control-select" :range="['氮含量', '磷含量', '钾含量', '有机质含量', 'pH值']">
          <view class="picker-view">氮含量</view>
        </picker>
      </view>
      
      <view class="control-group">
        <text>选择年份：</text>
        <picker class="control-select" :range="['2023年', '2022年', '2021年', '2020年', '2019年']">
          <view class="picker-view">2023年</view>
        </picker>
      </view>
      
      <view class="control-group">
        <text>显示方式：</text>
        <picker class="control-select" :range="['省级', '市级', '县级']">
          <view class="picker-view">省级</view>
        </picker>
      </view>
      
      <button class="btn refresh-btn" type="primary">刷新数据</button>
    </view>
    
    <view class="distribution-container">
      <view class="map-chart" ref="mapContainer"></view>
      
      <view class="province-ranking">
        <view class="ranking-header">
          <text class="section-title">氮含量省份排名</text>
        </view>
        
        <view class="ranking-list">
          <view class="ranking-item">
            <view class="rank">1</view>
            <view class="province">广东</view>
            <view class="value">95 mg/kg</view>
            <view class="bar-container">
              <view class="bar" style="width: 95%;"></view>
            </view>
          </view>
          <view class="ranking-item">
            <view class="rank">2</view>
            <view class="province">海南</view>
            <view class="value">86 mg/kg</view>
            <view class="bar-container">
              <view class="bar" style="width: 86%;"></view>
            </view>
          </view>
          <view class="ranking-item">
            <view class="rank">3</view>
            <view class="province">北京</view>
            <view class="value">85 mg/kg</view>
            <view class="bar-container">
              <view class="bar" style="width: 85%;"></view>
            </view>
          </view>
          <view class="ranking-item">
            <view class="rank">4</view>
            <view class="province">广西</view>
            <view class="value">83 mg/kg</view>
            <view class="bar-container">
              <view class="bar" style="width: 83%;"></view>
            </view>
          </view>
          <view class="ranking-item">
            <view class="rank">5</view>
            <view class="province">山东</view>
            <view class="value">82 mg/kg</view>
            <view class="bar-container">
              <view class="bar" style="width: 82%;"></view>
            </view>
          </view>
        </view>
      </view>
    </view>
    
    <view class="comparison-charts">
      <view class="chart-box">
        <view class="chart-header">
          <text class="section-title">不同区域氮含量对比</text>
        </view>
        <view class="comparison-chart region-chart"></view>
      </view>
      <view class="chart-box">
        <view class="chart-header">
          <text class="section-title">氮含量年度变化趋势</text>
        </view>
        <view class="comparison-chart trend-chart"></view>
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
  flex-wrap: wrap;
  gap: 15px;
  padding: 15px;
  background-color: white;
  margin: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  align-items: flex-end;
}

.control-group {
  display: flex;
  flex-direction: column;
  margin-right: 15px;
}

.control-group text {
  font-size: 14px;
  color: #555;
  margin-bottom: 5px;
}

.picker-view {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 150px;
  background-color: #f8f8f8;
}

.refresh-btn {
  margin-top: 20px;
  padding: 0 20px;
  height: 40px;
  line-height: 40px;
}

.distribution-container {
  display: flex;
  flex-direction: column;
  margin: 15px;
  gap: 15px;
}

.map-chart {
  height: 500px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.province-ranking {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.ranking-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
}

.ranking-list {
  padding: 10px 15px;
}

.ranking-item {
  display: flex;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f5f5f5;
}

.ranking-item:last-child {
  border-bottom: none;
}

.rank {
  width: 30px;
  height: 24px;
  background-color: #f0f7ff;
  color: #4d7bce;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 10px;
}

.province {
  width: 50px;
  margin-right: 10px;
}

.value {
  width: 70px;
  color: #555;
  font-size: 14px;
}

.bar-container {
  flex: 1;
  height: 8px;
  background-color: #f5f5f5;
  border-radius: 4px;
  overflow: hidden;
}

.bar {
  height: 100%;
  background-color: #4d7bce;
  border-radius: 4px;
}

.comparison-charts {
  display: flex;
  flex-direction: column;
  margin: 15px;
  gap: 15px;
}

.chart-box {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

.chart-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.comparison-chart {
  height: 250px;
  padding: 15px;
}

/* 使用条件编译适配不同平台 */
</style> 