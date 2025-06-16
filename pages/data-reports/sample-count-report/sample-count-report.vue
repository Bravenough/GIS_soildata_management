<template>
  <view class="report-page-container">
    <view class="page-header">
      <text class="header-title">样本总数详情</text>
    </view>
    <view class="content-area">
      <text>此处将展示样本总数的详细列表或进一步分析。</text>
      <button @click="goBack" class="back-button">返回</button>
    </view>
  </view>
</template>

<script>
export default {
  name: 'SampleCountReport',
  methods: {
    goBack() {
      uni.navigateBack();
    }
  }
};
</script>

<style scoped>
.report-page-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
  box-sizing: border-box;
}
.page-header {
  margin-bottom: 20px;
}
.header-title {
  font-size: 20px;
  font-weight: bold;
}
.content-area {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  text-align: center;
}
.back-button {
  margin-top: 20px;
  background-color: #4d7bce;
  color: white;
}
</style> 