<template>
  <view class="report-page-container">
    <view class="page-header">
      <text class="header-title">异常点位列表</text>
    </view>
    <view class="content-area">
      <text>此处将列出所有标记为异常的样本点及其详细信息。</text>
      <button @click="goBack" class="back-button">返回</button>
    </view>
  </view>
</template>

<script>
export default {
  name: 'AnomalyPointsReport',
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