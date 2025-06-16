// 数据库连接测试脚本
const DatabaseService = require('./utils/database.js');

async function testDatabase() {
  console.log('🔍 开始测试数据库连接...');
  
  try {
    // 测试获取统计概况
    console.log('\n📊 测试获取统计概况数据...');
    const overview = await DatabaseService.getStatisticsOverview();
    console.log('✅ 统计概况数据:', overview);
    
    // 测试获取土壤样本数据
    console.log('\n🌱 测试获取土壤样本数据...');
    const samples = await DatabaseService.getSoilSamples();
    console.log(`✅ 土壤样本数据: 共${samples.length}条记录`);
    if (samples.length > 0) {
      console.log('📋 示例数据:', samples[0]);
    }
    
    // 测试获取区域养分统计
    console.log('\n🗺️ 测试获取区域养分统计...');
    const regionStats = await DatabaseService.getRegionNutrientStats();
    console.log(`✅ 区域养分统计: 共${regionStats.length}个省份`);
    
    // 测试获取pH分布统计
    console.log('\n⚗️ 测试获取pH分布统计...');
    const phStats = await DatabaseService.getPhDistributionStats();
    console.log(`✅ pH分布统计: 共${phStats.length}个分类`);
    
    console.log('\n🎉 所有数据库测试通过！');
    
  } catch (error) {
    console.error('❌ 数据库测试失败:', error.message);
    console.error('💡 请检查:');
    console.error('   1. MySQL服务是否启动');
    console.error('   2. 数据库配置是否正确 (utils/database.js)');
    console.error('   3. 数据库和表是否存在');
    console.error('   4. 用户权限是否足够');
  } finally {
    // 关闭数据库连接
    await DatabaseService.close();
    console.log('\n🔒 数据库连接已关闭');
    process.exit(0);
  }
}

// 运行测试
testDatabase(); 