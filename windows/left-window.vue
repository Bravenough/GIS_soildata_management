<template>
	<view class="left-window-container">
		<view class="logo-section">
			<text class="title">基于GIS的土壤数据评估及分析信息查询系统</text>
		</view>
		
		<view class="nav-section">
			<view 
				v-for="(item, index) in navItems" 
				:key="index" 
				class="nav-item" 
				:class="{ active: currentPage === item.pagePath }"
				@click="navigateTo(item.pagePath)"
			>
				<view class="nav-item-content">
					<text class="nav-icon">{{ item.icon }}</text>
					<text class="nav-text">{{ item.text }}</text>
				</view>
			</view>
		</view>
		
		<view class="footer-section">
			<text class="footer-text">版本 1.0.0</text>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				currentPage: 'pages/index/index',
				navItems: [
					{
						text: '总览点位展示',
						pagePath: 'pages/index/index',
						icon: '🏠'
					},
					{
						text: '土壤数据',
						pagePath: 'pages/soil-data/soil-data',
						icon: '📊'
					},
					{
						text: '土壤情况热力图',
						pagePath: 'pages/heatmap/heatmap',
						icon: '🔥'
					},
					{
						text: '各省土壤情况分布',
						pagePath: 'pages/distribution/distribution',
						icon: '🗺️'
					},
					{
						text: '提交影响评估',
						pagePath: 'pages/assessment/assessment',
						icon: '📝'
					},
					{
						text: '数据路径查询',
						pagePath: 'pages/query/query',
						icon: '🔍'
					},
					{
						text: '土壤数据对比',
						pagePath: 'pages/comparison/comparison',
						icon: '📈'
					}
				]
			}
		},
		mounted() {
			// 获取当前页面路径
			const pages = getCurrentPages();
			if (pages.length) {
				const page = pages[pages.length - 1];
				this.currentPage = page.route;
			}
			
			// 监听页面切换
			uni.$on('page-change', (route) => {
				this.currentPage = route;
			});
		},
		beforeDestroy() {
			uni.$off('page-change');
		},
		methods: {
			navigateTo(url) {
				// 如果是同一页面，不做处理
				if (this.currentPage === url) return;
				
				// 设置当前页面
				this.currentPage = url;
				
				// 根据不同的页面类型使用不同的导航方法
				uni.redirectTo({
					url: '/' + url,
					success: () => {
						// 发送页面切换事件
						uni.$emit('page-change', url);
					},
					fail: (err) => {
						console.error('页面跳转失败:', err);
					}
				});
			}
		}
	}
</script>

<style>
	.left-window-container {
		display: flex;
		flex-direction: column;
		height: 100%;
		background-color: white;
		color: #333;
		box-sizing: border-box;
		border-right: 1px solid #e0e0e0;
		width: 240px;
	}
	
	.logo-section {
		padding: 15px 10px;
		display: flex;
		justify-content: center;
		align-items: center;
		border-bottom: 1px solid #e0e0e0;
		height: auto;
		min-height: 60px;
	}
	
	.title {
		font-size: 14px;
		font-weight: bold;
		color: #4d7bce;
		text-align: center;
		word-wrap: break-word;
		line-height: 1.4;
	}
	
	.nav-section {
		flex: 1;
		overflow-y: auto;
	}
	
	.nav-item {
		display: flex;
		align-items: center;
		padding: 15px 20px;
		color: #333;
		border-left: 4px solid transparent;
		transition: all 0.3s;
		cursor: pointer;
		height: auto;
	}
	
	.nav-item:hover {
		background-color: #f0f7ff;
		border-left-color: #4d7bce;
		color: #4d7bce;
	}
	
	.nav-item.active {
		background-color: #f0f7ff;
		border-left-color: #4d7bce;
		color: #4d7bce;
	}
	
	.nav-item-content {
		display: flex;
		align-items: center;
		width: 100%;
	}
	
	.nav-icon {
		font-size: 18px;
		margin-right: 10px;
		width: 20px;
		text-align: center;
	}
	
	.nav-text {
		font-size: 14px;
	}
	
	.footer-section {
		padding: 15px;
		text-align: center;
		border-top: 1px solid #e0e0e0;
	}
	
	.footer-text {
		font-size: 12px;
		color: #666;
	}
</style> 