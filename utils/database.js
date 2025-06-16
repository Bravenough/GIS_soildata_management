// 数据库连接和查询服务
const mysql = require('mysql2/promise');

// 数据库连接配置
const dbConfig = {
  host: 'localhost',
  port: 3306,
  user: 'root', // 请根据实际情况修改
  password: '050316', // 请根据实际情况修改
  database: 'soil_data',
  charset: 'utf8mb4',
  connectionLimit: 10,
  acquireTimeout: 60000,
  timeout: 60000
};

// 创建连接池
const pool = mysql.createPool(dbConfig);

// 数据库查询封装
class DatabaseService {
  // 获取土壤样本数据（用于地图显示）
  async getSoilSamples(filters = {}) {
    try {
      let sql = `
        SELECT 
          s.id,
          s.sample_code,
          s.sampling_date as sampleTime,
          s.latitude,
          s.longitude,
          s.sampler_name as remark,
          CONCAT(r.province, r.city, r.county) as region,
          st.type_name as soilType,
          t.ph_value as pH,
          t.total_nitrogen as nitrogen,
          t.available_phosphorus as phosphorus,
          t.available_potassium as potassium,
          t.organic_matter as organic
        FROM soil_samples s
        LEFT JOIN regions r ON s.region_id = r.id
        LEFT JOIN soil_types st ON s.soil_type_id = st.id
        LEFT JOIN soil_test_data t ON s.id = t.sample_id
        WHERE 1=1
      `;
      
      const params = [];
      
      // 添加筛选条件
      if (filters.province) {
        sql += ' AND r.province = ?';
        params.push(filters.province);
      }
      
      if (filters.phMin !== undefined) {
        sql += ' AND t.ph_value >= ?';
        params.push(filters.phMin);
      }
      
      if (filters.phMax !== undefined) {
        sql += ' AND t.ph_value <= ?';
        params.push(filters.phMax);
      }
      
      if (filters.dateStart) {
        sql += ' AND s.sampling_date >= ?';
        params.push(filters.dateStart);
      }
      
      if (filters.dateEnd) {
        sql += ' AND s.sampling_date <= ?';
        params.push(filters.dateEnd);
      }
      
      sql += ' ORDER BY s.sampling_date DESC LIMIT 1000';
      
      const [rows] = await pool.execute(sql, params);
      return rows.map(row => ({
        id: row.sample_code || row.id,
        name: `${row.region}采样点`,
        value: [parseFloat(row.longitude) || 0, parseFloat(row.latitude) || 0, row.nitrogen || 0],
        sampleTime: row.sampleTime,
        region: row.region,
        pH: parseFloat(row.pH) || 7.0,
        nitrogen: parseFloat(row.nitrogen) || 0,
        phosphorus: parseFloat(row.phosphorus) || 0,
        potassium: parseFloat(row.potassium) || 0,
        organic: parseFloat(row.organic) || 0,
        soilType: row.soilType || '未知',
        remark: row.remark || ''
      }));
    } catch (error) {
      console.error('获取土壤样本数据失败:', error);
      throw error;
    }
  }

  // 获取土壤数据统计表格（用于数据管理页面）
  async getSoilDataTable(page = 1, pageSize = 10, filters = {}) {
    try {
      const offset = (page - 1) * pageSize;
      
      let countSql = `
        SELECT COUNT(*) as total
        FROM soil_samples s
        LEFT JOIN regions r ON s.region_id = r.id
        LEFT JOIN soil_types st ON s.soil_type_id = st.id
        LEFT JOIN soil_test_data t ON s.id = t.sample_id
        WHERE 1=1
      `;
      
      let dataSql = `
        SELECT 
          s.id,
          s.sample_code,
          s.sampling_date as time,
          CONCAT(r.province, r.city, r.county) as location,
          t.ph_value as ph,
          t.total_nitrogen as nitrogen,
          t.available_phosphorus as phosphorus,
          t.available_potassium as potassium,
          t.organic_matter as organic,
          st.type_name as texture
        FROM soil_samples s
        LEFT JOIN regions r ON s.region_id = r.id
        LEFT JOIN soil_types st ON s.soil_type_id = st.id
        LEFT JOIN soil_test_data t ON s.id = t.sample_id
        WHERE 1=1
      `;
      
      const params = [];
      
      // 添加筛选条件
      if (filters.location) {
        const locationFilter = ' AND (r.province LIKE ? OR r.city LIKE ? OR r.county LIKE ?)';
        countSql += locationFilter;
        dataSql += locationFilter;
        const locationParam = `%${filters.location}%`;
        params.push(locationParam, locationParam, locationParam);
      }
      
      if (filters.phMin !== undefined) {
        countSql += ' AND t.ph_value >= ?';
        dataSql += ' AND t.ph_value >= ?';
        params.push(filters.phMin);
      }
      
      if (filters.phMax !== undefined) {
        countSql += ' AND t.ph_value <= ?';
        dataSql += ' AND t.ph_value <= ?';
        params.push(filters.phMax);
      }
      
      dataSql += ' ORDER BY s.sampling_date DESC LIMIT ? OFFSET ?';
      
      // 获取总数
      const [countResult] = await pool.execute(countSql, params);
      const total = countResult[0].total;
      
      // 获取分页数据 - 确保参数是数字类型
      const dataParams = [...params, parseInt(pageSize), parseInt(offset)];
      const [rows] = await pool.execute(dataSql, dataParams);
      
      return {
        data: rows.map(row => ({
          id: row.sample_code || row.id,
          time: row.time,
          location: row.location,
          ph: parseFloat(row.ph) || 0,
          nitrogen: parseFloat(row.nitrogen) || 0,
          phosphorus: parseFloat(row.phosphorus) || 0,
          potassium: parseFloat(row.potassium) || 0,
          organic: parseFloat(row.organic) || 0,
          texture: row.texture || '未知'
        })),
        total,
        page,
        pageSize,
        totalPages: Math.ceil(total / pageSize)
      };
    } catch (error) {
      console.error('获取土壤数据表格失败:', error);
      throw error;
    }
  }

  // 获取区域养分统计数据
  async getRegionNutrientStats() {
    try {
      const sql = `
        SELECT 
          r.province,
          AVG(t.total_nitrogen) as avg_nitrogen,
          AVG(t.available_phosphorus) as avg_phosphorus,
          AVG(t.available_potassium) as avg_potassium,
          AVG(t.organic_matter) as avg_organic,
          COUNT(s.id) as sample_count
        FROM soil_samples s
        LEFT JOIN regions r ON s.region_id = r.id
        LEFT JOIN soil_test_data t ON s.id = t.sample_id
        WHERE r.province IS NOT NULL
        GROUP BY r.province
        HAVING sample_count > 0
        ORDER BY sample_count DESC
        LIMIT 10
      `;
      
      const [rows] = await pool.execute(sql);
      return rows.map(row => ({
        province: row.province,
        nitrogen: parseFloat(row.avg_nitrogen) || 0,
        phosphorus: parseFloat(row.avg_phosphorus) || 0,
        potassium: parseFloat(row.avg_potassium) || 0,
        organic: parseFloat(row.avg_organic) || 0,
        sampleCount: row.sample_count
      }));
    } catch (error) {
      console.error('获取区域养分统计失败:', error);
      throw error;
    }
  }

  // 获取pH值分布统计
  async getPhDistributionStats() {
    try {
      const sql = `
        SELECT 
          CASE 
            WHEN t.ph_value < 5.5 THEN '强酸性(<5.5)'
            WHEN t.ph_value < 6.5 THEN '酸性(5.5-6.5)'
            WHEN t.ph_value < 7.5 THEN '中性(6.5-7.5)'
            WHEN t.ph_value < 8.5 THEN '弱碱性(7.5-8.5)'
            ELSE '强碱性(>8.5)'
          END as ph_range,
          COUNT(*) as count
        FROM soil_test_data t
        WHERE t.ph_value IS NOT NULL
        GROUP BY ph_range
        ORDER BY MIN(t.ph_value)
      `;
      
      const [rows] = await pool.execute(sql);
      return rows.map(row => ({
        name: row.ph_range,
        value: row.count
      }));
    } catch (error) {
      console.error('获取pH分布统计失败:', error);
      throw error;
    }
  }

  // 获取土壤质地分布统计
  async getSoilTextureStats() {
    try {
      const sql = `
        SELECT 
          st.type_name as texture,
          COUNT(s.id) as count
        FROM soil_samples s
        LEFT JOIN soil_types st ON s.soil_type_id = st.id
        WHERE st.type_name IS NOT NULL
        GROUP BY st.type_name
        ORDER BY count DESC
      `;
      
      const [rows] = await pool.execute(sql);
      return rows.map(row => ({
        name: row.texture,
        value: row.count
      }));
    } catch (error) {
      console.error('获取土壤质地统计失败:', error);
      throw error;
    }
  }

  // 获取养分趋势数据
  async getNutrientTrendData(months = 12) {
    try {
      const sql = `
        SELECT 
          DATE_FORMAT(s.sampling_date, '%Y-%m') as month,
          AVG(t.total_nitrogen) as avg_nitrogen,
          AVG(t.available_phosphorus) as avg_phosphorus,
          AVG(t.available_potassium) as avg_potassium,
          AVG(t.organic_matter) as avg_organic,
          COUNT(s.id) as sample_count
        FROM soil_samples s
        LEFT JOIN soil_test_data t ON s.id = t.sample_id
        WHERE s.sampling_date >= DATE_SUB(NOW(), INTERVAL ? MONTH)
        GROUP BY DATE_FORMAT(s.sampling_date, '%Y-%m')
        ORDER BY month
      `;
      
      const [rows] = await pool.execute(sql, [months]);
      return rows.map(row => ({
        month: row.month,
        nitrogen: parseFloat(row.avg_nitrogen) || 0,
        phosphorus: parseFloat(row.avg_phosphorus) || 0,
        potassium: parseFloat(row.avg_potassium) || 0,
        organic: parseFloat(row.avg_organic) || 0,
        sampleCount: row.sample_count
      }));
    } catch (error) {
      console.error('获取养分趋势数据失败:', error);
      throw error;
    }
  }

  // 获取土壤质量评估数据
  async getSoilQualityAssessment(sampleId) {
    try {
      const sql = `
        SELECT 
          qa.quality_level,
          qa.quality_score,
          qa.nitrogen_level,
          qa.phosphorus_level,
          qa.potassium_level,
          qa.ph_level,
          qa.organic_matter_level,
          qa.recommendations
        FROM soil_quality_assessment qa
        WHERE qa.sample_id = ?
      `;
      
      const [rows] = await pool.execute(sql, [sampleId]);
      return rows[0] || null;
    } catch (error) {
      console.error('获取土壤质量评估失败:', error);
      throw error;
    }
  }

  // 获取历史监测数据
  async getHistoricalData(stationId, dateRange = 30) {
    try {
      const sql = `
        SELECT 
          hmd.monitoring_date,
          hmd.ph_value,
          hmd.organic_matter,
          hmd.moisture_content,
          hmd.temperature
        FROM historical_monitoring_data hmd
        LEFT JOIN monitoring_stations ms ON hmd.station_id = ms.id
        WHERE ms.station_code = ? 
        AND hmd.monitoring_date >= DATE_SUB(NOW(), INTERVAL ? DAY)
        ORDER BY hmd.monitoring_date ASC
      `;
      
      const [rows] = await pool.execute(sql, [stationId, dateRange]);
      return rows.map(row => ({
        date: row.monitoring_date,
        ph: parseFloat(row.ph_value) || 0,
        organic: parseFloat(row.organic_matter) || 0,
        moisture: parseFloat(row.moisture_content) || 0,
        temperature: parseFloat(row.temperature) || 0
      }));
    } catch (error) {
      console.error('获取历史监测数据失败:', error);
      throw error;
    }
  }

  // 获取统计概况数据
  async getStatisticsOverview() {
    try {
      const [sampleCount] = await pool.execute('SELECT COUNT(*) as count FROM soil_samples');
      
      // 安全地查询省份数量
      let provinceCount = [{ count: 0 }];
      try {
        [provinceCount] = await pool.execute('SELECT COUNT(DISTINCT province) as count FROM regions WHERE province IS NOT NULL');
      } catch (err) {
        console.warn('regions表不存在，使用默认值');
      }
      
              // 安全地查询质量分布
        let qualityStats = [];
        try {
          [qualityStats] = await pool.execute(`
            SELECT 
              overall_quality as quality_level,
              COUNT(*) as count
            FROM soil_quality_assessment 
            GROUP BY overall_quality
          `);
        } catch (err) {
          console.warn('soil_quality_assessment表字段不匹配，使用默认值');
          qualityStats = [];
        }
      
      // 安全地查询平均pH值
      let avgPh = [{ avg_ph: 7.0 }];
      try {
        [avgPh] = await pool.execute('SELECT AVG(ph_value) as avg_ph FROM soil_test_data WHERE ph_value IS NOT NULL');
      } catch (err) {
        console.warn('soil_test_data表不存在，使用默认值');
      }

      return {
        totalSamples: sampleCount[0].count,
        provincesCovered: provinceCount[0].count,
        averagePh: parseFloat(avgPh[0].avg_ph) || 7.0,
        qualityDistribution: qualityStats.map(row => ({
          level: row.quality_level,
          count: row.count
        }))
      };
    } catch (error) {
      console.error('获取统计概况失败:', error);
      throw error;
    }
  }

  // 关闭数据库连接池
  async close() {
    await pool.end();
  }
}

module.exports = new DatabaseService(); 