#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
土壤数据管理系统 - MySQL数据装载演示脚本
"""

import os
import sys
import getpass
from load_data_to_database import DatabaseLoader

def get_mysql_connection():
    """获取MySQL数据库连接信息"""
    print("🔗 请输入MySQL数据库连接信息:")
    print("-" * 40)
    
    host = input("数据库主机 (默认: localhost): ").strip() or "localhost"
    port = input("端口号 (默认: 3306): ").strip() or "3306"
    username = input("用户名: ").strip()
    
    if not username:
        print("❌ 用户名不能为空")
        return None
    
    password = getpass.getpass("密码: ")
    database = input("数据库名 (默认: soil_data): ").strip() or "soil_data"
    
    # 构建连接URL
    database_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4"
    
    return database_url, {
        'host': host,
        'port': port,
        'username': username,
        'database': database
    }

def create_database_if_not_exists(connection_info):
    """如果数据库不存在则创建"""
    import pymysql
    
    try:
        # 连接到MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=connection_info['host'],
            port=int(connection_info['port']),
            user=connection_info['username'],
            password=getpass.getpass("再次输入密码以创建数据库: "),
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # 创建数据库
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{connection_info['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ 数据库 '{connection_info['database']}' 已准备就绪")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 创建数据库失败: {str(e)}")
        return False

def main():
    print("🌱 土壤数据管理系统 - MySQL数据装载演示")
    print("=" * 50)
    
    data_dir = "data"
    
    # 检查数据目录是否存在
    if not os.path.exists(data_dir):
        print(f"❌ 数据目录不存在: {data_dir}")
        print("请先运行 python generate_csv_data.py 生成CSV数据文件")
        return 1
    
    # 检查是否有CSV文件
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    if not csv_files:
        print(f"❌ 在 {data_dir} 目录中没有找到CSV文件")
        print("请先运行 python generate_csv_data.py 生成CSV数据文件")
        return 1
    
    print(f"📁 找到 {len(csv_files)} 个CSV文件")
    
    # 获取数据库连接信息
    connection_result = get_mysql_connection()
    if not connection_result:
        return 1
    
    database_url, connection_info = connection_result
    
    print(f"\n📊 准备连接到 MySQL 数据库:")
    print(f"   主机: {connection_info['host']}:{connection_info['port']}")
    print(f"   用户: {connection_info['username']}")
    print(f"   数据库: {connection_info['database']}")
    
    # 询问是否创建数据库
    create_db = input("\n是否需要创建数据库？(y/n): ").lower().strip()
    if create_db in ['y', 'yes', '是']:
        if not create_database_if_not_exists(connection_info):
            return 1
    
    # 询问是否继续装载
    response = input("\n是否开始装载数据？(y/n): ").lower().strip()
    if response not in ['y', 'yes', '是']:
        print("取消装载")
        return 0
    
    try:
        # 创建装载器
        print("\n🔧 初始化数据库装载器...")
        loader = DatabaseLoader(database_url, data_dir)
        
        # 询问是否重新创建表
        recreate = input("是否重新创建所有表？(y/n): ").lower().strip()
        if recreate in ['y', 'yes', '是']:
            print("🗑️  删除现有表...")
            loader.drop_all_tables()
        
        # 创建表结构
        print("🏗️  创建数据库表结构...")
        loader.create_tables()
        
        # 装载数据
        print("📊 开始装载数据...")
        success = loader.load_all_tables(batch_size=1000)
        
        if success:
            print("\n✅ 数据装载完成！")
            
            # 验证数据
            print("🔍 验证数据装载结果...")
            results = loader.verify_data()
            
            print("\n📈 数据统计:")
            print("-" * 50)
            total_records = 0
            for table_name, count in results.items():
                if isinstance(count, int):
                    total_records += count
                    print(f"{table_name:<30}: {count:>10,} 条")
                else:
                    print(f"{table_name:<30}: {count}")
            
            print("-" * 50)
            print(f"{'总计':<30}: {total_records:>10,} 条")
            
            print(f"\n🎉 数据已成功装载到MySQL数据库!")
            print(f"📊 数据库: {connection_info['database']}")
            
            print("\n💡 使用建议:")
            print("   可以使用MySQL客户端工具连接数据库:")
            print(f"   mysql -h {connection_info['host']} -P {connection_info['port']} -u {connection_info['username']} -p {connection_info['database']}")
            print("   或者使用可视化工具如 MySQL Workbench、phpMyAdmin、Navicat等")
            
            print("\n🔍 示例查询:")
            print("   SELECT COUNT(*) FROM soil_samples;")
            print("   SELECT province, COUNT(*) FROM regions GROUP BY province;")
            print("   SELECT s.sample_code, t.ph_value, t.organic_matter")
            print("   FROM soil_samples s JOIN soil_test_data t ON s.id = t.sample_id")
            print("   WHERE t.ph_value < 6.0 LIMIT 10;")
            
        else:
            print("\n❌ 数据装载失败！")
            return 1
            
    except Exception as e:
        print(f"\n❌ 执行失败: {str(e)}")
        print("\n💡 常见问题排查:")
        print("   1. 检查MySQL服务是否正在运行")
        print("   2. 检查用户名密码是否正确")
        print("   3. 检查用户是否有创建数据库和表的权限")
        print("   4. 检查网络连接是否正常")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 