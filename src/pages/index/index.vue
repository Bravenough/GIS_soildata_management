<template>
    <view class="page-container">
      <!-- 顶部导航栏 -->
      <view class="top-navbar">
        <view class="flex-spacer"></view>
        
        <view class="user-info-dropdown">
          <view class="user-info">
            <text>当前用户：管理员</text>
            <text class="dropdown-icon">▼</text>
          </view>
          <view class="dropdown-menu">
            <view class="dropdown-item">个人信息</view>
            <view class="dropdown-item">设置</view>
            <view class="dropdown-item">退出登录</view>
          </view>
        </view>
      </view>
      
      <!-- 主内容区 -->
      <view class="main-container">

        
        <!-- 地图和控制区域 -->
        <view class="content-area">
          <!-- 调试信息面板 -->
          <view class="debug-panel" v-if="showDebugPanel">
            <view class="debug-header">
              <text class="debug-title">🔧 调试信息</text>
              <text class="close-btn" @click="showDebugPanel = false">×</text>
            </view>
            <view class="debug-content">
              <view class="debug-item">
                <text class="debug-label">地图状态:</text>
                <text class="debug-value" :class="mapChart ? 'success' : 'error'">
                  {{mapChart ? '已创建' : '未创建'}}
                </text>
              </view>
              <view class="debug-item">
                <text class="debug-label">加载状态:</text>
                <text class="debug-value" :class="isMapLoading ? 'warning' : 'success'">
                  {{isMapLoading ? '加载中...' : '已完成'}}
                </text>
              </view>
              <view class="debug-item">
                <text class="debug-label">错误信息:</text>
                <text class="debug-value error">{{mapError || '无'}}</text>
              </view>
              <view class="debug-item">
                <text class="debug-label">采样点数:</text>
                <text class="debug-value">{{Array.isArray(samplePointsData) ? samplePointsData.length : '非数组'}}</text>
              </view>
              <view class="debug-item">
                <text class="debug-label">数据类型:</text>
                <text class="debug-value">{{typeof samplePointsData}} / {{Array.isArray(samplePointsData) ? '数组' : '非数组'}}</text>
              </view>
              <view class="debug-item">
                <text class="debug-label">ECharts:</text>
                <text class="debug-value">{{typeof echarts}}</text>
              </view>
            </view>
          </view>
          
          <!-- 地图控制工具栏 -->
          <view class="map-toolbar">
            <view class="location-selector">
              <picker :range="['全部地区', '华北地区', '东北地区', '华东地区', '中南地区', '西南地区', '西北地区']">
                <view class="picker-view">全部地区</view>
              </picker>
            </view>
            
            <view class="search-box">
              <input type="text" placeholder="请输入关键字搜索..." />
              <button class="search-btn">搜索</button>
              <button class="filter-btn">筛选</button>
              <button class="map-type-btn">卫星地图</button>
              <button class="reset-btn">重置</button>
            </view>
          </view>
          
          <!-- 主地图区域 -->
          <view class="map-container" id="main-chart" @click="handleMapClick">
            <!-- 添加加载状态指示器 -->
            <view class="map-loading" v-if="isMapLoading">
              <view class="loading-spinner"></view>
              <text>地图加载中...</text>
            </view>
            <view class="map-error" v-if="mapError">
              <text>{{mapError}}</text>
              <button @click="retryLoadMap" class="retry-btn">重试</button>
            </view>
          </view>
          
          <!-- 图层控制面板 -->
          <view class="layer-control-panel" v-if="showLayerPanel">
            <view class="panel-header">
              <text class="panel-title">图层控制</text>
              <text class="close-btn" @click="showLayerPanel = false">×</text>
            </view>
            <view class="layer-options">
              <label class="layer-option">
                <checkbox checked />
                <text>基础地图</text>
              </label>
              <label class="layer-option">
                <checkbox checked />
                <text>氮含量</text>
              </label>
              <label class="layer-option">
                <checkbox />
                <text>磷含量</text>
              </label>
              <label class="layer-option">
                <checkbox />
                <text>钾含量</text>
              </label>
              <label class="layer-option">
                <checkbox />
                <text>有机质含量</text>
              </label>
              <label class="layer-option">
                <checkbox checked />
                <text>采样点</text>
              </label>
            </view>
          </view>
          
          <!-- 数据筛选面板 -->
          <view class="filter-panel" v-if="showFilterPanel">
            <view class="panel-header">
              <text class="panel-title">数据筛选</text>
              <text class="close-btn" @click="showFilterPanel = false">×</text>
            </view>
            <view class="filter-form">
              <view class="filter-group">
                <text class="filter-label">采样时间范围</text>
                <view class="date-range">
                  <picker mode="date">
                    <view class="date-picker">yyyy/mm/日</view>
                  </picker>
                  <text class="range-separator">至</text>
                  <picker mode="date">
                    <view class="date-picker">yyyy/mm/日</view>
                  </picker>
                </view>
              </view>
              
              <view class="filter-group">
                <text class="filter-label">pH值范围</text>
                <view class="slider-container">
                  <input type="number" class="range-input" />
                  <slider min="0" max="14" value="7" show-value />
                  <input type="number" class="range-input" value="14" />
                </view>
                <view class="range-labels">
                  <text>0</text>
                  <text>14</text>
                </view>
              </view>
              
              <view class="filter-group">
                <text class="filter-label">氮含量范围 (mg/kg)</text>
                <view class="slider-container">
                  <input type="number" class="range-input" />
                  <slider min="0" max="200" value="100" show-value />
                  <input type="number" class="range-input" value="200" />
                </view>
                <view class="range-labels">
                  <text>0</text>
                  <text>200</text>
                </view>
              </view>
              
              <view class="filter-group">
                <text class="filter-label">土壤类型</text>
                <view class="checkbox-group">
                  <label class="checkbox-option">
                    <checkbox />
                    <text>砂质土</text>
                  </label>
                  <label class="checkbox-option">
                    <checkbox />
                    <text>壤土</text>
                  </label>
                  <label class="checkbox-option">
                    <checkbox />
                    <text>粘土</text>
                  </label>
                </view>
              </view>
              
              <view class="filter-actions">
                <button class="btn reset-filter-btn">重置筛选</button>
                <button class="btn apply-filter-btn" type="primary">应用筛选</button>
              </view>
            </view>
          </view>
          
          <!-- 图例面板 -->
          <view class="legend-panel">
            <view class="legend-title">土壤养分图例</view>
            <view class="legend-items">
              <view class="legend-item">
                <text class="legend-name">氮含量</text>
                <view class="legend-gradient nitrogen-gradient"></view>
              </view>
              <view class="legend-item">
                <text class="legend-name">磷含量</text>
                <view class="legend-gradient phosphorus-gradient"></view>
              </view>
              <view class="legend-item">
                <text class="legend-name">钾含量</text>
                <view class="legend-gradient potassium-gradient"></view>
              </view>
              <view class="legend-item">
                <text class="legend-name">有机质含量</text>
                <view class="legend-gradient organic-gradient"></view>
              </view>
              <view class="legend-labels">
                <text>低</text>
                <text>高</text>
              </view>
            </view>
          </view>
          
          <!-- 采样点详情面板 -->
          <view class="sample-detail-panel" v-if="showDetailPanel && currentSamplePoint">
            <view class="panel-header">
              <text class="panel-title">土壤采样点详情</text>
              <text class="close-btn" @click="showDetailPanel = false">×</text>
            </view>
            <view class="sample-info">
              <view class="info-row">
                <text class="info-label">采样点ID</text>
                <text class="info-value">{{currentSamplePoint.id}}</text>
              </view>
              <view class="info-row">
                <text class="info-label">采样点名称</text>
                <text class="info-value">{{currentSamplePoint.name}}</text>
              </view>
              <view class="info-row">
                <text class="info-label">采样时间</text>
                <text class="info-value">{{currentSamplePoint.sampleTime}}</text>
              </view>
              <view class="info-row">
                <text class="info-label">行政区划</text>
                <text class="info-value">{{currentSamplePoint.region}}</text>
              </view>
              <view class="info-row">
                <text class="info-label">pH值</text>
                <text class="info-value">{{currentSamplePoint.pH}}</text>
              </view>
              <view class="info-row">
                <text class="info-label">氮含量</text>
                <text class="info-value">{{currentSamplePoint.nitrogen}} mg/kg</text>
              </view>
              <view class="info-row">
                <text class="info-label">磷含量</text>
                <text class="info-value">{{currentSamplePoint.phosphorus}} mg/kg</text>
              </view>
              <view class="info-row">
                <text class="info-label">钾含量</text>
                <text class="info-value">{{currentSamplePoint.potassium}} mg/kg</text>
              </view>
              <view class="info-row">
                <text class="info-label">有机质含量</text>
                <text class="info-value">{{currentSamplePoint.organic}}%</text>
              </view>
              <view class="info-row">
                <text class="info-label">土壤质地</text>
                <text class="info-value">{{currentSamplePoint.soilType}}</text>
              </view>
              <view class="info-row">
                <text class="info-label">备注说明</text>
                <text class="info-value">{{currentSamplePoint.remark}}</text>
              </view>
              <view class="info-row">
                <text class="info-label">坐标</text>
                <text class="info-value">{{currentSamplePoint.value[0]}}, {{currentSamplePoint.value[1]}}</text>
              </view>
            </view>
            <view class="sample-actions">
              <button class="btn" @click="exportData(currentSamplePoint)">导出数据</button>
              <button class="btn" @click="viewHistory(currentSamplePoint)">查看历史</button>
              <button class="btn" type="primary" @click="analyzeData(currentSamplePoint)">土壤分析</button>
            </view>
          </view>
          
          <!-- 养分趋势图面板 -->
          <view class="trend-panel" v-if="showTrendPanel">
            <view class="panel-header">
              <text class="panel-title">土壤养分趋势图</text>
              <text class="close-btn" @click="showTrendPanel = false">×</text>
            </view>
            <view class="trend-tabs">
              <view class="tab active">养分趋势</view>
              <view class="tab">区域对比</view>
              <view class="tab">预测分析</view>
            </view>
            <view class="trend-chart">
              <!-- 趋势图表将在这里渲染 -->
            </view>
          </view>
        </view>
      </view>
      
      <!-- 添加地图工具按钮 -->
                <view class="map-tools">
            <button class="tool-button" @click="showFilterPanel = true">筛选</button>
            <button class="tool-button" @click="showLayerPanel = true">图层</button>
            <button class="tool-button" @click="showTrendPanel = true">趋势图</button>
            <button class="tool-button debug-btn" @click="showDebugPanel = !showDebugPanel">
              🔧 调试
            </button>
          </view>
    </view>
  </template>
  
  <script>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
// 引入中国地图数据
import 'echarts/map/js/china';
import soilDataAPI from '@/utils/api.js';
  
  export default {
    setup() {
      // 地图图表引用
      const mainChartRef = ref(null);
      let mapChart = null;
      
      // 添加地图加载状态
      const isMapLoading = ref(true);
      const mapError = ref('');
      
      // 添加面板显示状态
      const showDetailPanel = ref(false);
      const showFilterPanel = ref(false);
      const showLayerPanel = ref(false);
      const showTrendPanel = ref(false);
      const showDebugPanel = ref(true); // 默认显示调试面板
      
      // 土壤采样点数据（从数据库加载）
      const samplePointsData = ref([]);
      
      // 加载土壤采样点数据
      const loadSamplePointsData = async () => {
        try {
          console.log('📊 [调试] 开始加载土壤采样点数据...');
          console.log('🔍 [调试] API对象检查:', typeof soilDataAPI, soilDataAPI?.getSoilSamples ? '方法存在' : '方法不存在');
          
          const data = await soilDataAPI.getSoilSamples();
          console.log('🔍 [调试] API返回数据类型:', typeof data);
          console.log('🔍 [调试] API返回数据是数组:', Array.isArray(data));
          console.log('🔍 [调试] API返回数据:', data);
          
          // 确保返回的数据是数组
          if (Array.isArray(data)) {
            samplePointsData.value = data;
            console.log('✅ [调试] 土壤采样点数据加载完成，共', data.length, '个采样点');
            console.log('🔍 [调试] 数据示例:', data.slice(0, 2));
          } else {
            console.error('❌ [调试] API返回的数据不是数组，使用默认数据');
            throw new Error('API返回数据格式错误');
          }
        } catch (error) {
          console.error('❌ [调试] 加载土壤采样点数据失败:', error);
          // 使用默认模拟数据作为后备方案
          samplePointsData.value = [
            { 
              id: 'BJ001', 
              name: '北京采样点1', 
              value: [116.4074, 39.9042, 85], 
              sampleTime: '2024-01-15 08:30',
              region: '北京市海淀区温泉镇',
              pH: 6.8,
              nitrogen: 85,
              phosphorus: 45,
              potassium: 120,
              organic: 2.3,
              soilType: '砂壤土',
              remark: '近期施肥，氮含量较高'
            },
            { 
              id: 'SH001', 
              name: '上海采样点1', 
              value: [121.4737, 31.2304, 120], 
              sampleTime: '2024-01-14 09:15',
              region: '上海市浦东新区张江镇',
              pH: 7.2,
              nitrogen: 120,
              phosphorus: 60,
              potassium: 95,
              organic: 3.1,
              soilType: '粘土',
              remark: '土壤肥沃，有机质含量高'
            },
            { 
              id: 'GD001', 
              name: '广东采样点1', 
              value: [113.2644, 23.1291, 83], 
              sampleTime: '2024-01-13 10:45',
              region: '广东省广州市番禺区',
              pH: 5.9,
              nitrogen: 83,
              phosphorus: 52,
              potassium: 88,
              organic: 2.8,
              soilType: '砂壤土',
              remark: '酸性土壤，适合种植水果'
            }
          ];
        }
      };
      
      // 当前选中的采样点
      const currentSamplePoint = ref(null);
      
      // 获取采样点数据 - 修复函数定义
      const getSamplePointsData = () => {
        console.log('🔍 [调试] getSamplePointsData被调用');
        console.log('🔍 [调试] samplePointsData.value类型:', typeof samplePointsData.value);
        console.log('🔍 [调试] samplePointsData.value是数组:', Array.isArray(samplePointsData.value));
        console.log('🔍 [调试] samplePointsData.value值:', samplePointsData.value);
        
        // 确保数据是数组
        if (!Array.isArray(samplePointsData.value)) {
          console.error('❌ [调试] samplePointsData.value不是数组，返回空数组');
          return [];
        }
        
        console.log('✅ [调试] 数据验证通过，共', samplePointsData.value.length, '个点');
        return samplePointsData.value.map(item => ({
          name: item.name,
          value: item.value,
          id: item.id
        }));
      };
      
      // 根据ID获取采样点详情
      const getSamplePointById = (id) => {
        if (!Array.isArray(samplePointsData.value)) {
          console.error('❌ [调试] getSamplePointById: samplePointsData.value不是数组');
          return null;
        }
        return samplePointsData.value.find(item => item.id === id);
      };
      

      
      // 处理地图点击事件，显示样点详情
      const handleMapClick = (event) => {
        console.log('地图点击事件:', event);
      };
      
      // 重试加载地图
      const retryLoadMap = () => {
        console.log('尝试重新加载地图...');
        mapError.value = '';
        isMapLoading.value = true;
        setTimeout(() => {
          initMap();
        }, 500);
      };
      
      // 初始化地图
      const initMap = () => {
        console.log('🚀 [调试] 开始初始化地图...');
        console.log('🔍 [调试] 检查运行环境 - document:', typeof document, ', window:', typeof window);
        console.log('🔍 [调试] 检查echarts:', typeof echarts, ', 版本:', echarts?.version);
        
        isMapLoading.value = true;
        
        try {
          // 获取DOM元素
          console.log('🔍 [调试] 尝试获取DOM元素 #main-chart...');
          const domElement = document.getElementById('main-chart');
          
          if (!domElement) {
            console.error('❌ [调试] 地图容器元素未找到！');
            console.error('❌ [调试] 检查页面是否存在id="main-chart"的元素');
            isMapLoading.value = false;
            mapError.value = '地图容器元素未找到，请重试';
            return;
          }
          
          console.log('✅ [调试] 找到地图容器元素');
          console.log('🔍 [调试] 容器尺寸:', domElement.offsetWidth, 'x', domElement.offsetHeight);
          console.log('🔍 [调试] 容器样式:', {
            display: getComputedStyle(domElement).display,
            visibility: getComputedStyle(domElement).visibility,
            width: getComputedStyle(domElement).width,
            height: getComputedStyle(domElement).height
          });
          
          // 检查容器尺寸
          if (domElement.offsetWidth === 0 || domElement.offsetHeight === 0) {
            console.error('❌ [调试] 容器尺寸为0，可能是CSS样式问题');
            isMapLoading.value = false;
            mapError.value = '地图容器尺寸异常，请检查CSS样式';
            return;
          }
          
          // 销毁旧的实例
          if (mapChart) {
            console.log('🗑️ [调试] 销毁旧的地图实例');
            mapChart.dispose();
          }
          
          // 初始化ECharts实例
          console.log('⚙️ [调试] 正在初始化ECharts实例...');
          console.log('🔍 [调试] echarts.init方法:', typeof echarts.init);
          
          try {
            mapChart = echarts.init(domElement);
            console.log('✅ [调试] ECharts实例创建成功:', !!mapChart);
            console.log('🔍 [调试] 实例方法检查:', {
              setOption: typeof mapChart.setOption,
              on: typeof mapChart.on,
              getWidth: typeof mapChart.getWidth,
              getHeight: typeof mapChart.getHeight
            });
          } catch (echartsError) {
            console.error('❌ [调试] ECharts实例化失败:', echartsError);
            throw echartsError;
          }
          
          // 检查中国地图是否可用
          console.log('🔍 [调试] 检查中国地图注册状态:', {
            getMap: typeof echarts.getMap,
            chinaMap: echarts.getMap ? echarts.getMap('china') : '无getMap方法'
          });
          
          // 准备采样点数据
          console.log('📊 [调试] 准备采样点数据...');
          console.log('🔍 [调试] 检查samplePointsData状态:', {
            type: typeof samplePointsData.value,
            isArray: Array.isArray(samplePointsData.value),
            length: Array.isArray(samplePointsData.value) ? samplePointsData.value.length : 0,
            value: samplePointsData.value
          });
          
          const samplePoints = getSamplePointsData();
          console.log('✅ [调试] 采样点数据准备完毕，共', samplePoints.length, '个点');
          
          if (samplePoints.length > 0) {
            console.log('🔍 [调试] 采样点示例数据:', samplePoints.slice(0, 2));
          } else {
            console.warn('⚠️ [调试] 没有可用的采样点数据，将只显示地图');
          }
          
          // 设置地图配置
          const option = {
            backgroundColor: '#fff',
            title: {
              text: '全国土壤养分分布情况',
              left: 'center',
              textStyle: {
                color: '#333'
              }
            },
            tooltip: {
              trigger: 'item',
              formatter: function(params) {
                if (params.seriesType === 'scatter') {
                  return `${params.data.name}<br/>氮含量: ${params.data.value[2]} mg/kg`;
                } else {
                  return `${params.name}<br/>氮含量: ${params.value} mg/kg`;
                }
              }
            },
            visualMap: {
              min: 0,
              max: 200,
              left: 'left',
              top: 'bottom',
              text: ['高', '低'],
              calculable: true,
              inRange: {
                color: ['#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027']
              }
            },
            geo: {
              map: 'china',
              roam: true,
              scaleLimit: {
                min: 0.5,
                max: 5
              },
              label: {
                show: true,
                fontSize: 12,
                color: '#333'
              },
              itemStyle: {
                areaColor: '#f3f3f3',
                borderColor: '#ccc'
              },
              emphasis: {
                itemStyle: {
                  areaColor: '#cce8ff'
                },
                label: {
                  show: true
                }
              }
            },
            series: [
              {
                name: '氮含量',
                type: 'map',
                map: 'china',
                roam: true,
                label: {
                  show: true
                },
                data: [
                  { name: '北京', value: 85 },
                  { name: '天津', value: 72 },
                  { name: '河北', value: 98 },
                  { name: '山西', value: 56 },
                  { name: '内蒙古', value: 45 },
                  { name: '辽宁', value: 78 },
                  { name: '吉林', value: 67 },
                  { name: '黑龙江', value: 89 },
                  { name: '上海', value: 120 },
                  { name: '江苏', value: 113 },
                  { name: '浙江', value: 92 },
                  { name: '安徽', value: 105 },
                  { name: '福建', value: 87 },
                  { name: '江西', value: 94 },
                  { name: '山东', value: 108 },
                  { name: '河南', value: 115 },
                  { name: '湖北', value: 102 },
                  { name: '湖南', value: 96 },
                  { name: '广东', value: 83 },
                  { name: '广西', value: 76 },
                  { name: '海南', value: 65 },
                  { name: '重庆', value: 88 },
                  { name: '四川', value: 93 },
                  { name: '贵州', value: 71 },
                  { name: '云南', value: 69 },
                  { name: '西藏', value: 35 },
                  { name: '陕西', value: 82 },
                  { name: '甘肃', value: 49 },
                  { name: '青海', value: 40 },
                  { name: '宁夏', value: 52 },
                  { name: '新疆', value: 47 }
                ]
              },
              {
                name: '采样点',
                type: 'scatter',
                coordinateSystem: 'geo',
                symbol: 'pin',
                symbolSize: 20,
                label: {
                  show: false
                },
                emphasis: {
                  label: {
                    show: false
                  }
                },
                itemStyle: {
                  color: '#4d7bce'
                },
                data: samplePoints,
                z: 10
              }
            ]
          };
          
          // 设置地图配置
          console.log('⚙️ [调试] 正在设置地图配置...');
          console.log('🔍 [调试] 地图配置对象:', {
            title: option.title ? '已设置' : '未设置',
            geo: option.geo ? '已设置' : '未设置',
            series: option.series ? `${option.series.length}个系列` : '未设置',
            visualMap: option.visualMap ? '已设置' : '未设置'
          });
          
          try {
            mapChart.setOption(option);
            console.log('✅ [调试] 地图配置设置完成');
            
            // 检查渲染状态
            setTimeout(() => {
              console.log('🔍 [调试] 延时检查渲染状态...');
              console.log('🔍 [调试] 图表尺寸:', {
                width: mapChart.getWidth(),
                height: mapChart.getHeight(),
                isDisposed: mapChart.isDisposed()
              });
            }, 100);
            
          } catch (optionError) {
            console.error('❌ [调试] 设置地图配置失败:', optionError);
            throw optionError;
          }
          
          // 为地图添加点击事件
          mapChart.on('click', function(params) {
            console.log('点击了地图元素:', params);
            
            if (params.componentSubType === 'scatter') {
              console.log('点击了采样点:', params.data.name, 'ID:', params.data.id);
              const pointDetail = getSamplePointById(params.data.id);
              if (pointDetail) {
                currentSamplePoint.value = pointDetail;
                showDetailPanel.value = true;
              }
            } else if (params.componentSubType === 'map') {
              console.log('点击了地图区域:', params.name);
              currentSamplePoint.value = null;
              showDetailPanel.value = false;
            }
          });
          
          // 标记加载完成
          setTimeout(() => {
            console.log('⏰ [调试] 延时标记加载完成...');
            isMapLoading.value = false;
            console.log('🎉 [调试] 地图初始化完成！最终状态检查:');
            console.log('🔍 [调试] mapChart存在:', !!mapChart);
            console.log('🔍 [调试] isMapLoading:', isMapLoading.value);
            console.log('🔍 [调试] mapError:', mapError.value);
            
            if (mapChart && !mapChart.isDisposed()) {
              console.log('✅ [调试] 地图实例状态正常');
            } else {
              console.error('❌ [调试] 地图实例状态异常');
            }
          }, 500);
          
        } catch (error) {
          console.error('❌ [调试] 地图初始化失败，详细错误:', error);
          console.error('❌ [调试] 错误堆栈:', error.stack);
          isMapLoading.value = false;
          mapError.value = `地图初始化失败: ${error.message}`;
        }
      };
      
      // 窗口大小变化时重新绘制图表
      const handleResize = () => {
        if (mapChart) {
          mapChart.resize();
        }
      };
      
      // 组件挂载后初始化
      onMounted(async () => {
        console.log('🚀 [调试] 组件已挂载，准备初始化...');
        console.log('🔍 [调试] 检查全局对象:', {
          document: typeof document,
          window: typeof window,
          echarts: typeof echarts,
          uni: typeof uni
        });
        
        // 检查DOM是否准备就绪
        console.log('🔍 [调试] DOM准备状态:', document.readyState);
        console.log('🔍 [调试] 检查目标容器是否存在:', !!document.getElementById('main-chart'));
        
        try {
          // 首先加载土壤采样点数据
          console.log('📊 [调试] 开始加载土壤采样点数据...');
          await loadSamplePointsData();
          console.log('✅ [调试] 土壤采样点数据加载完成');
          
          // 延迟初始化地图，确保DOM元素已渲染完成
          setTimeout(() => {
            console.log('⏰ [调试] 开始延时初始化地图 (1000ms后)');
            console.log('🔍 [调试] 再次检查目标容器:', !!document.getElementById('main-chart'));
            
            try {
              initMap();
            } catch (mapInitError) {
              console.error('❌ [调试] 地图初始化异常:', mapInitError);
              console.error('❌ [调试] 异常堆栈:', mapInitError.stack);
              isMapLoading.value = false;
              mapError.value = '地图初始化失败，请刷新页面重试';
            }
          }, 1000);
          
          // 监听窗口大小变化
          if (typeof window !== 'undefined') {
            window.addEventListener('resize', handleResize);
            console.log('✅ [调试] 已添加窗口大小变化监听');
          }
          
        } catch (error) {
          console.error('❌ [调试] 组件初始化失败:', error);
          console.error('❌ [调试] 失败堆栈:', error.stack);
          isMapLoading.value = false;
          mapError.value = '系统初始化失败，请刷新页面重试';
        }
      });
      
      // 土壤分析功能
      const analyzeData = (samplePoint) => {
        console.log('分析土壤数据:', samplePoint.id);
        // 显示分析结果弹窗
        uni.showLoading({
          title: '正在生成分析报告...'
        });
        
        // 模拟分析过程
        setTimeout(() => {
          uni.hideLoading();
          
          // 跳转到土壤分析报告页面
          uni.navigateTo({
            url: `/pages/soil-analysis/soil-analysis?id=${samplePoint.id}&name=${encodeURIComponent(samplePoint.name)}&region=${encodeURIComponent(samplePoint.region)}`,
            success: () => {
              console.log('跳转到土壤分析报告页面');
              // 传递采样点数据到报告页面
              uni.$emit('soil-sample-data', {
                id: samplePoint.id,
                name: samplePoint.name,
                time: samplePoint.sampleTime,
                region: samplePoint.region,
                ph: samplePoint.pH,
                nitrogen: samplePoint.nitrogen,
                phosphorus: samplePoint.phosphorus,
                potassium: samplePoint.potassium,
                organic: samplePoint.organic,
                soilType: samplePoint.soilType,
                evaluation: getOverallRating(samplePoint),
                phEvaluation: interpretPH(samplePoint.pH),
                nitrogenEvaluation: interpretNutrient('nitrogen', samplePoint.nitrogen),
                phosphorusEvaluation: interpretNutrient('phosphorus', samplePoint.phosphorus),
                potassiumEvaluation: interpretNutrient('potassium', samplePoint.potassium),
                organicEvaluation: interpretOrganic(samplePoint.organic),
                soilTypeEvaluation: interpretSoilType(samplePoint.soilType),
              });
            },
            fail: (err) => {
              console.error('跳转失败:', err);
              // 如果跳转失败，则显示简单的弹窗
              showSimpleAnalysisReport(samplePoint);
            }
          });
        }, 1500);
      };
      
      // 显示土壤分析报告弹窗
      const showSoilAnalysisReport = (samplePoint) => {
        // 先创建一个临时的报告页面
        const tempPage = {
          url: `/pages/assessment/assessment?id=${samplePoint.id}&name=${encodeURIComponent(samplePoint.name)}&region=${encodeURIComponent(samplePoint.region)}&source=sample_point`,
          success: () => {
            console.log('跳转到土壤分析报告页面');
            // 传递采样点数据到报告页面
            uni.$emit('soil-sample-data', {
              id: samplePoint.id,
              name: samplePoint.name,
              time: samplePoint.sampleTime,
              region: samplePoint.region,
              ph: samplePoint.pH,
              nitrogen: samplePoint.nitrogen,
              phosphorus: samplePoint.phosphorus,
              potassium: samplePoint.potassium,
              organic: samplePoint.organic,
              soilType: samplePoint.soilType,
              evaluation: getOverallRating(samplePoint),
              phEvaluation: interpretPH(samplePoint.pH),
              nitrogenEvaluation: interpretNutrient('nitrogen', samplePoint.nitrogen),
              phosphorusEvaluation: interpretNutrient('phosphorus', samplePoint.phosphorus),
              potassiumEvaluation: interpretNutrient('potassium', samplePoint.potassium),
              organicEvaluation: interpretOrganic(samplePoint.organic),
              soilTypeEvaluation: interpretSoilType(samplePoint.soilType),
            });
          },
          fail: (err) => {
            console.error('跳转失败:', err);
            // 如果跳转失败，则显示简单的弹窗
            showSimpleAnalysisReport(samplePoint);
          }
        };
        
        // 尝试跳转到分析报告页面
        uni.navigateTo(tempPage);
      };
      
      // 显示简单的分析报告弹窗（备选方案）
      const showSimpleAnalysisReport = (samplePoint) => {
        uni.showModal({
          title: '土壤分析报告',
          content: `样点: ${samplePoint.name}\n
采样时间: ${samplePoint.sampleTime}\n
分析结果:\n
1. 土壤pH值(${samplePoint.pH})：${interpretPH(samplePoint.pH)}\n
2. 氮含量(${samplePoint.nitrogen}mg/kg)：${interpretNutrient('nitrogen', samplePoint.nitrogen)}\n
3. 磷含量(${samplePoint.phosphorus}mg/kg)：${interpretNutrient('phosphorus', samplePoint.phosphorus)}\n
4. 钾含量(${samplePoint.potassium}mg/kg)：${interpretNutrient('potassium', samplePoint.potassium)}\n
5. 有机质含量(${samplePoint.organic}%)：${interpretOrganic(samplePoint.organic)}\n
6. 土壤质地评价：${samplePoint.soilType}，${interpretSoilType(samplePoint.soilType)}\n
7. 综合评价：${getOverallRating(samplePoint)}`,
          showCancel: true,
          cancelText: '关闭',
          confirmText: '保存报告',
          success: function(res) {
            if (res.confirm) {
              uni.showToast({
                title: '报告已保存',
                icon: 'success'
              });
            }
          }
        });
      };
      
      // 查看历史数据
      const viewHistory = (samplePoint) => {
        console.log('查看历史数据:', samplePoint.id);
        
        // 创建模拟历史数据，包含趋势变化
        const historicalData = [
          { date: '2023-08-15', ph: 6.7, nitrogen: 82, phosphorus: 43, potassium: 118, organic: 2.2 },
          { date: '2023-07-15', ph: 6.6, nitrogen: 80, phosphorus: 42, potassium: 115, organic: 2.1 },
          { date: '2023-06-15', ph: 6.5, nitrogen: 78, phosphorus: 40, potassium: 110, organic: 2.0 },
          { date: '2023-05-15', ph: 6.4, nitrogen: 75, phosphorus: 38, potassium: 105, organic: 1.9 }
        ];
        
        // 尝试跳转到历史数据页面
        uni.navigateTo({
          url: `/pages/history-data/history-data?id=${samplePoint.id}&name=${encodeURIComponent(samplePoint.name)}`,
          success: () => {
            console.log('跳转到历史数据页面');
            // 传递历史数据
            uni.$emit('sample-history-data', {
              samplePoint: samplePoint,
              history: historicalData
            });
          },
          fail: (err) => {
            console.error('跳转失败:', err);
            // 如果跳转失败，则显示简单的弹窗
            showSimpleHistoryData(samplePoint, historicalData);
          }
        });
      };
      
      // 显示简单的历史数据弹窗（备选方案）
      const showSimpleHistoryData = (samplePoint, historicalData) => {
        let historyContent = `${samplePoint.name} 历史数据:\n\n`;
        historicalData.forEach(record => {
          historyContent += `日期: ${record.date}\n`;
          historyContent += `pH值: ${record.ph}\n`;
          historyContent += `氮含量: ${record.nitrogen} mg/kg\n`;
          historyContent += `磷含量: ${record.phosphorus} mg/kg\n`;
          historyContent += `钾含量: ${record.potassium} mg/kg\n`;
          historyContent += `有机质: ${record.organic}%\n\n`;
        });
        
        uni.showModal({
          title: '历史采样数据',
          content: historyContent,
          showCancel: false,
          confirmText: '关闭'
        });
      };
      
      // 导出数据为CSV
      const exportData = (samplePoint) => {
        console.log('导出数据:', samplePoint.id);
        
        // 构建CSV内容
        const csvHeader = '采样点ID,采样点名称,采样时间,行政区划,pH值,氮含量(mg/kg),磷含量(mg/kg),钾含量(mg/kg),有机质含量(%),土壤质地,备注说明';
        const csvData = `${samplePoint.id},${samplePoint.name},${samplePoint.sampleTime},${samplePoint.region},${samplePoint.pH},${samplePoint.nitrogen},${samplePoint.phosphorus},${samplePoint.potassium},${samplePoint.organic},${samplePoint.soilType},${samplePoint.remark}`;
        const csvContent = `${csvHeader}\n${csvData}`;
        
        // 模拟文件保存
        uni.showLoading({
          title: '正在导出数据...'
        });
        
        setTimeout(() => {
          uni.hideLoading();
          
          // 尝试不同平台的实现
          if (typeof plus !== 'undefined') {
            // App平台实现
            const fileName = `土壤采样数据_${samplePoint.id}.csv`;
            const filePath = `_downloads/${fileName}`;
            
            plus.io.requestFileSystem(plus.io.PUBLIC_DOWNLOADS, fs => {
              fs.root.getFile(fileName, { create: true }, fileEntry => {
                fileEntry.createWriter(writer => {
                  writer.onwrite = () => {
                    uni.showModal({
                      title: '导出成功',
                      content: `文件已保存到：${plus.io.convertLocalFileSystemURL(filePath)}`,
                      showCancel: false
                    });
                  };
                  writer.write(csvContent);
                });
              });
            });
          } else {
            // 其他平台模拟实现
            uni.showModal({
              title: '数据导出成功',
              content: '文件已保存到：/downloads/土壤采样数据_' + samplePoint.id + '.csv',
              showCancel: false,
              success: function() {
                uni.showToast({
                  title: '导出完成',
                  icon: 'success'
                });
              }
            });
          }
        }, 1000);
      };
      
      // 辅助函数 - 解释pH值
      const interpretPH = (ph) => {
        if (ph < 5.5) return '强酸性土壤，需要石灰调节';
        if (ph < 6.5) return '弱酸性土壤，适合大部分作物生长';
        if (ph < 7.5) return '中性土壤，土壤肥力良好';
        return '碱性土壤，可能需要施用硫磺等物质降低pH值';
      };
      
      // 辅助函数 - 解释养分含量
      const interpretNutrient = (type, value) => {
        switch (type) {
          case 'nitrogen':
            if (value < 50) return '含量低，需要增施氮肥';
            if (value < 80) return '含量中等，适量施肥';
            return '含量充足，减少氮肥施用';
          case 'phosphorus':
            if (value < 30) return '含量低，需要增施磷肥';
            if (value < 50) return '含量中等，适量施肥';
            return '含量充足，减少磷肥施用';
          case 'potassium':
            if (value < 70) return '含量低，需要增施钾肥';
            if (value < 100) return '含量中等，适量施肥';
            return '含量充足，减少钾肥施用';
        }
      };
      
      // 辅助函数 - 解释有机质含量
      const interpretOrganic = (value) => {
        if (value < 1.5) return '有机质含量低，建议增加有机肥施用';
        if (value < 2.5) return '有机质含量中等，维持现有施肥量';
        return '有机质含量高，土壤肥力好';
      };
      
      // 辅助函数 - 解释土壤质地
      const interpretSoilType = (type) => {
        switch (type) {
          case '砂质土': return '透气性好，保水保肥能力差，适合根菜类作物';
          case '壤土': return '理想的农业土壤，透气、保水、保肥能力均衡';
          case '粘土': return '保水保肥能力强，但透气性差，适合水稻等作物';
          case '砂壤土': return '透气性较好，保水保肥能力中等';
          case '粘壤土': return '保水保肥能力较好，透气性中等';
          case '黑土': return '有机质含量高，肥力好，适合多种作物';
          default: return '需要实地评估具体特性';
        }
      };
      
      // 辅助函数 - 获取综合评价
      const getOverallRating = (point) => {
        // 简单计算评分
        let score = 0;
        
        // pH值评分
        if (point.pH >= 6.5 && point.pH <= 7.5) score += 25;
        else if ((point.pH >= 5.5 && point.pH < 6.5) || (point.pH > 7.5 && point.pH <= 8.0)) score += 15;
        else score += 5;
        
        // 养分评分
        if (point.nitrogen >= 80) score += 15;
        else if (point.nitrogen >= 50) score += 10;
        else score += 5;
        
        if (point.phosphorus >= 50) score += 15;
        else if (point.phosphorus >= 30) score += 10;
        else score += 5;
        
        if (point.potassium >= 100) score += 15;
        else if (point.potassium >= 70) score += 10;
        else score += 5;
        
        // 有机质评分
        if (point.organic >= 2.5) score += 30;
        else if (point.organic >= 1.5) score += 20;
        else score += 10;
        
        // 评价等级
        if (score >= 85) return '优质土壤，适合多种作物种植，养分丰富，肥力强';
        if (score >= 70) return '良好土壤，适合大部分作物种植，个别养分需要补充';
        if (score >= 50) return '中等土壤，需要适当改良和补充养分';
        return '贫瘠土壤，需要系统改良，增加有机质和基础养分';
      };
      
      return {
        mainChartRef,
        handleMapClick,
        showDetailPanel,
        showFilterPanel,
        showLayerPanel,
        showTrendPanel,
        showDebugPanel,
        isMapLoading,
        mapError,
        retryLoadMap,
        currentSamplePoint,
        analyzeData,
        viewHistory,
        exportData,
        samplePointsData,
        getSamplePointsData,
        getSamplePointById,
        initMap
      };
    }
  };
  </script>
  
  <style>
  .page-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    width: 100%;
    overflow: hidden;
  }
  
  /* 顶部导航栏 */
  .top-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    height: 60px;
    background-color: #4d7bce;
    color: white;
  }
  
  .flex-spacer {
    width: 200px;
  }
  
  .system-title-center {
    font-size: 22px;
    font-weight: bold;
    text-align: center;
    flex: 1;
  }
  
  .user-info-dropdown {
    position: relative;
    width: 200px;
    text-align: right;
  }
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    justify-content: flex-end;
  }
  
  .dropdown-icon {
    font-size: 12px;
  }
  
  .dropdown-menu {
    position: absolute;
    top: 40px;
    right: 0;
    width: 150px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    display: none;
    z-index: 100;
  }
  
  .user-info:hover + .dropdown-menu,
  .dropdown-menu:hover {
    display: block;
  }
  
  .dropdown-item {
    padding: 10px 15px;
    color: #333;
    cursor: pointer;
  }
  
  .dropdown-item:hover {
    background-color: #f5f5f5;
  }
  
  /* 主内容区 */
  .main-container {
    display: flex;
    flex: 1;
    overflow: hidden;
  }
  

  
  /* 内容区域 */
  .content-area {
    flex: 1;
    position: relative;
    overflow: hidden;
  }
  
  /* 地图工具栏 */
  .map-toolbar {
    display: flex;
    justify-content: space-between;
    padding: 10px 15px;
    background-color: white;
    border-bottom: 1px solid #eee;
  }
  
  .location-selector {
    min-width: 120px;
  }
  
  .picker-view {
    padding: 6px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #f8f8f8;
  }
  
  .search-box {
    display: flex;
    gap: 15px;
    align-items: center;
  }
  
  .search-box input {
    width: 250px;
    padding: 6px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .search-btn, .filter-btn, .map-type-btn, .reset-btn {
    padding: 6px 12px;
    border-radius: 4px;
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    font-size: 14px;
    min-width: 60px;
    text-align: center;
    margin: 0 3px;
  }
  
  /* 地图容器 */
  .map-container {
    height: calc(100% - 50px);
    width: 100%;
    background-color: #e8f4f8;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }
  
  /* 添加地图加载状态样式 */
  .map-loading {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    background-color: rgba(255, 255, 255, 0.7);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 5;
    pointer-events: none;
  }
  
  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #4d7bce;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 10px;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .map-error {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    background-color: rgba(255, 255, 255, 0.9);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 5;
    padding: 20px;
    text-align: center;
    color: #f56c6c;
  }
  
  .retry-btn {
    margin-top: 15px;
    padding: 8px 20px;
    background-color: #4d7bce;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  /* 图层控制面板 */
  .layer-control-panel {
    position: absolute;
    top: 70px;
    right: 20px;
    width: 200px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    z-index: 10;
  }
  
  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 15px;
    border-bottom: 1px solid #eee;
  }
  
  .panel-title {
    font-weight: bold;
  }
  
  .close-btn {
    cursor: pointer;
    font-size: 18px;
  }
  
  .layer-options {
    padding: 10px 15px;
  }
  
  .layer-option {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
  }
  
  /* 数据筛选面板 */
  .filter-panel {
    position: absolute;
    top: 70px;
    left: 20px;
    width: 300px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    z-index: 10;
  }
  
  .filter-form {
    padding: 10px 15px;
  }
  
  .filter-group {
    margin-bottom: 15px;
  }
  
  .filter-label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .date-range {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .date-picker {
    flex: 1;
    padding: 6px 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #f8f8f8;
  }
  
  .range-separator {
    color: #666;
  }
  
  .slider-container {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .range-input {
    width: 50px;
    padding: 6px;
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  slider {
    flex: 1;
  }
  
  .range-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 5px;
    color: #666;
    font-size: 12px;
  }
  
  .checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .checkbox-option {
    display: flex;
    align-items: center;
    gap: 5px;
  }
  
  .filter-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }
  
  .btn {
    padding: 8px 15px;
    border-radius: 4px;
    font-size: 14px;
  }
  
  .reset-filter-btn {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
  }
  
  .apply-filter-btn {
    background-color: #4d7bce;
    color: white;
    border: none;
  }
  
  /* 图例面板 */
  .legend-panel {
    position: absolute;
    bottom: 20px;
    right: 20px;
    width: 200px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 10px 15px;
    z-index: 10;
  }
  
  .legend-title {
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .legend-items {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .legend-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }
  
  .legend-name {
    width: 70px;
  }
  
  .legend-gradient {
    flex: 1;
    height: 10px;
    border-radius: 5px;
  }
  
  .nitrogen-gradient {
    background: linear-gradient(to right, #313695, #4575b4, #74add1, #abd9e9, #e0f3f8, #ffffbf, #fee090, #fdae61, #f46d43, #d73027, #a50026);
  }
  
  .phosphorus-gradient {
    background: linear-gradient(to right, #2c7bb6, #abd9e9, #ffffbf, #fdae61, #d7191c);
  }
  
  .potassium-gradient {
    background: linear-gradient(to right, #1a9850, #91cf60, #ffffbf, #fc8d59, #d73027);
  }
  
  .organic-gradient {
    background: linear-gradient(to right, #ffffd9, #edf8b1, #c7e9b4, #7fcdbb, #41b6c4, #1d91c0, #225ea8, #0c2c84);
  }
  
  .legend-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 5px;
    color: #666;
    font-size: 12px;
  }
  
  /* 采样点详情面板 */
  .sample-detail-panel {
    position: absolute;
    top: 70px;
    left: 340px;
    width: 300px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    z-index: 10;
  }
  
  .sample-info {
    padding: 10px 15px;
  }
  
  .info-row {
    display: flex;
    margin-bottom: 8px;
  }
  
  .info-label {
    width: 100px;
    color: #666;
  }
  
  .info-value {
    flex: 1;
    font-weight: bold;
  }
  
  .sample-actions {
    display: flex;
    justify-content: space-between;
    padding: 10px 15px;
    border-top: 1px solid #eee;
  }
  
  /* 养分趋势图面板 */
  .trend-panel {
    position: absolute;
    bottom: 20px;
    left: 20px;
    width: 600px;
    height: 300px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    z-index: 10;
  }
  
  .trend-tabs {
    display: flex;
    border-bottom: 1px solid #eee;
  }
  
  .tab {
    padding: 10px 20px;
    cursor: pointer;
  }
  
  .tab.active {
    border-bottom: 2px solid #4d7bce;
    color: #4d7bce;
    font-weight: bold;
  }
  
  .trend-chart {
    height: calc(100% - 80px);
    padding: 15px;
  }
  
  /* 响应式调整 */
  @media (max-width: 1200px) {
    .trend-panel {
      width: 500px;
    }
  }
  
  @media (max-width: 992px) {
    .sample-detail-panel {
      left: 240px;
    }
    
    .trend-panel {
      width: 400px;
    }
  }
  
  /* 添加地图工具按钮样式 */
  .map-tools {
    position: absolute;
    top: 70px;
    right: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    z-index: 5;
  }
  
  .tool-button {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10px 15px;
    font-size: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    cursor: pointer;
    min-width: 80px;
    text-align: center;
  }
  
  .tool-button:hover {
    background-color: #f8f8f8;
  }
  
  /* 调试面板样式 */
  .debug-panel {
    position: absolute;
    top: 70px;
    right: 120px;
    width: 250px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    z-index: 15;
  }
  
  .debug-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 15px;
    border-bottom: 1px solid #eee;
    background-color: #f8f9fa;
    border-radius: 4px 4px 0 0;
  }
  
  .debug-title {
    font-weight: bold;
    color: #333;
  }
  
  .debug-content {
    padding: 10px 15px;
    max-height: 300px;
    overflow-y: auto;
  }
  
  .debug-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    padding: 5px 0;
    border-bottom: 1px solid #f0f0f0;
  }
  
  .debug-label {
    font-size: 12px;
    color: #666;
    flex: 1;
  }
  
  .debug-value {
    font-size: 12px;
    font-weight: bold;
    flex: 1;
    text-align: right;
  }
  
  .debug-value.success {
    color: #28a745;
  }
  
  .debug-value.error {
    color: #dc3545;
  }
  
  .debug-value.warning {
    color: #ffc107;
  }
  
  .debug-btn {
    background-color: #007bff !important;
    color: white !important;
  }
  </style>