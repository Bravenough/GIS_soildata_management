#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
土壤数据管理系统 - CSV数据生成器
生成完整的数据库表对应的CSV文件
"""

import csv
import random
import json
from datetime import datetime, date, timedelta
import os
import hashlib
from faker import Faker

# 设置中文本地化
fake = Faker('zh_CN')

class SoilDataCSVGenerator:
    def __init__(self):
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # 存储生成的数据供其他表引用
        self.regions = []
        self.soil_types = []
        self.crop_types = []
        self.fertilizer_products = []
        self.users = []
        self.monitoring_stations = []
        self.soil_samples = []
        
    def generate_regions(self):
        """生成行政区域数据"""
        print("生成行政区域数据...")
        
        # 省份数据
        provinces = [
            ("110000", "北京市", 1, None, 39.9042, 116.4074),
            ("120000", "天津市", 1, None, 39.3434, 117.3616),
            ("130000", "河北省", 1, None, 38.0428, 114.5149),
            ("140000", "山西省", 1, None, 37.5777, 112.2922),
            ("150000", "内蒙古自治区", 1, None, 40.8414, 111.7518),
            ("210000", "辽宁省", 1, None, 41.2956, 123.4315),
            ("220000", "吉林省", 1, None, 43.8868, 125.3245),
            ("230000", "黑龙江省", 1, None, 45.7732, 126.6618),
            ("310000", "上海市", 1, None, 31.2304, 121.4737),
            ("320000", "江苏省", 1, None, 32.0415, 118.7672),
            ("330000", "浙江省", 1, None, 30.2741, 120.1551),
            ("340000", "安徽省", 1, None, 31.8612, 117.2272),
            ("350000", "福建省", 1, None, 26.0745, 119.2965),
            ("360000", "江西省", 1, None, 28.6766, 115.9092),
            ("370000", "山东省", 1, None, 36.6758, 117.0009),
            ("410000", "河南省", 1, None, 34.7466, 113.6254),
            ("420000", "湖北省", 1, None, 30.5952, 114.2998),
            ("430000", "湖南省", 1, None, 28.1127, 112.9836),
            ("440000", "广东省", 1, None, 23.1291, 113.2644),
            ("450000", "广西壮族自治区", 1, None, 22.8159, 108.3275),
            ("460000", "海南省", 1, None, 20.0179, 110.3493),
            ("500000", "重庆市", 1, None, 29.5630, 106.5516),
            ("510000", "四川省", 1, None, 30.6171, 104.0648),
            ("520000", "贵州省", 1, None, 26.5783, 106.7135),
            ("530000", "云南省", 1, None, 25.0406, 102.7103),
            ("540000", "西藏自治区", 1, None, 29.6440, 91.1409),
            ("610000", "陕西省", 1, None, 34.3416, 108.9398),
            ("620000", "甘肃省", 1, None, 36.0611, 103.8343),
            ("630000", "青海省", 1, None, 36.6171, 101.7782),
            ("640000", "宁夏回族自治区", 1, None, 38.4681, 106.2731),
            ("650000", "新疆维吾尔自治区", 1, None, 43.7938, 87.6177)
        ]
        
        data = []
        for i, (code, name, level, parent_id, lat, lng) in enumerate(provinces, 1):
            row = {
                'id': i,
                'region_code': code,
                'province': name,
                'city': '',
                'county': '',
                'level': level,
                'parent_id': parent_id,
                'latitude': lat,
                'longitude': lng,
                'created_at': fake.date_time_between(start_date='-2y', end_date='now'),
                'updated_at': fake.date_time_between(start_date='-1y', end_date='now')
            }
            data.append(row)
            self.regions.append(row)
        
        # 生成一些市级数据
        cities_data = [
            ("石家庄市", "130000", 38.0428, 114.5149),
            ("唐山市", "130000", 39.6351, 118.1756),
            ("太原市", "140000", 37.8706, 112.5489),
            ("大同市", "140000", 40.0901, 113.2908),
            ("沈阳市", "210000", 41.6758, 123.4315),
            ("大连市", "210000", 38.9140, 121.6147),
            ("南京市", "320000", 32.0415, 118.7672),
            ("苏州市", "320000", 31.3041, 120.5954),
            ("杭州市", "330000", 30.2741, 120.1551),
            ("宁波市", "330000", 29.8683, 121.5440),
        ]
        
        for city_name, parent_code, lat, lng in cities_data:
            parent_id = next((r['id'] for r in self.regions if r['region_code'] == parent_code), None)
            if parent_id:
                city_id = len(data) + 1
                city_code = parent_code[:2] + str(random.randint(1000, 9999))
                row = {
                    'id': city_id,
                    'region_code': city_code,
                    'province': next(r['province'] for r in self.regions if r['id'] == parent_id),
                    'city': city_name,
                    'county': '',
                    'level': 2,
                    'parent_id': parent_id,
                    'latitude': lat + random.uniform(-0.5, 0.5),
                    'longitude': lng + random.uniform(-0.5, 0.5),
                    'created_at': fake.date_time_between(start_date='-2y', end_date='now'),
                    'updated_at': fake.date_time_between(start_date='-1y', end_date='now')
                }
                data.append(row)
                self.regions.append(row)
        
        # 补充更多区县数据达到1000条
        while len(data) < 1000:
            parent = random.choice([r for r in self.regions if r['level'] <= 2])
            county_id = len(data) + 1
            county_code = parent['region_code'][:4] + str(random.randint(100, 999))
            
            if parent['level'] == 1:  # 省级
                city_name = fake.city_name()
                county_name = ''
                level = 2
            else:  # 市级
                city_name = parent['city']
                county_name = fake.district()
                level = 3
            
            row = {
                'id': county_id,
                'region_code': county_code,
                'province': parent['province'],
                'city': city_name,
                'county': county_name,
                'level': level,
                'parent_id': parent['id'],
                'latitude': parent['latitude'] + random.uniform(-2, 2),
                'longitude': parent['longitude'] + random.uniform(-2, 2),
                'created_at': fake.date_time_between(start_date='-2y', end_date='now'),
                'updated_at': fake.date_time_between(start_date='-1y', end_date='now')
            }
            data.append(row)
            self.regions.append(row)
        
        self.save_csv('regions.csv', data)
        return data
    
    def generate_soil_types(self):
        """生成土壤类型数据"""
        print("生成土壤类型数据...")
        
        soil_types_data = [
            ("CT001", "潮土", "分布在河流冲积平原，质地较轻，适宜多种作物", 6.0, 8.0, "华北平原、长江中下游平原"),
            ("HT001", "黄土", "主要分布在黄土高原，质地疏松，易冲刷", 7.0, 8.5, "陕西、甘肃、山西"),
            ("RT001", "红土", "热带亚热带地区发育的酸性土壤", 4.5, 6.5, "华南、西南地区"),
            ("BT001", "黑土", "有机质丰富，肥力较高的土壤", 6.5, 7.5, "东北平原"),
            ("ST001", "沙土", "质地疏松，透水透气性好", 6.0, 8.0, "华北、西北干旱区"),
            ("ZT001", "粘土", "保水保肥能力强，质地较重", 6.5, 7.5, "长江中下游"),
            ("LT001", "壤土", "理想的农业土壤，肥力中等", 6.0, 7.5, "全国各地"),
            ("MT001", "水稻土", "长期种植水稻形成的土壤", 5.5, 7.0, "南方水稻种植区"),
            ("ZOT001", "褐土", "温带半湿润地区的地带性土壤", 6.5, 8.0, "华北、东北南部"),
            ("YJ001", "盐碱土", "盐分含量较高的土壤", 7.5, 9.0, "华北、西北、东北西部"),
        ]
        
        data = []
        for i, (code, name, desc, ph_min, ph_max, regions) in enumerate(soil_types_data, 1):
            row = {
                'id': i,
                'type_code': code,
                'type_name': name,
                'description': desc,
                'optimal_ph_min': ph_min,
                'optimal_ph_max': ph_max,
                'typical_regions': regions,
                'created_at': fake.date_time_between(start_date='-2y', end_date='now')
            }
            data.append(row)
            self.soil_types.append(row)
        
        # 补充更多土壤类型到50条
        additional_types = [
            "砂壤土", "粉砂土", "粉质粘土", "砂质粘土", "石灰土", "紫色土", 
            "棕壤", "灰化土", "森林土", "草甸土", "沼泽土", "风沙土",
            "石质土", "碱土", "酸性土", "中性土", "富铁土", "钙质土",
            "有机土", "泥炭土", "冲积土", "残积土", "坡积土", "洪积土",
            "海积土", "湖积土", "风积土", "火山土", "冻土", "盐土",
            "碱化土", "潜育土", "氧化土", "还原土", "胶结土", "疏松土",
            "致密土", "多孔土", "层状土", "均质土"
        ]
        
        for i, type_name in enumerate(additional_types, len(data) + 1):
            if len(data) >= 50:
                break
            row = {
                'id': i,
                'type_code': f"ST{i:03d}",
                'type_name': type_name,
                'description': f"{type_name}是{fake.text(max_nb_chars=50)}",
                'optimal_ph_min': round(random.uniform(4.5, 7.0), 1),
                'optimal_ph_max': round(random.uniform(7.0, 9.0), 1),
                'typical_regions': random.choice(["华北地区", "东北地区", "华南地区", "西南地区", "西北地区"]),
                'created_at': fake.date_time_between(start_date='-2y', end_date='now')
            }
            data.append(row)
            self.soil_types.append(row)
        
        self.save_csv('soil_types.csv', data)
        return data
    
    def generate_crop_types(self):
        """生成作物类型数据"""
        print("生成作物类型数据...")
        
        crops_data = [
            ("YM001", "玉米", "粮食作物", 6.0, 7.5, "春季播种，秋季收获", {"N": 180, "P": 80, "K": 150}),
            ("XM001", "小麦", "粮食作物", 6.5, 7.5, "秋季播种，夏季收获", {"N": 160, "P": 70, "K": 120}),
            ("SD001", "水稻", "粮食作物", 5.5, 7.0, "春季播种，秋季收获", {"N": 140, "P": 60, "K": 100}),
            ("DD001", "大豆", "豆类作物", 6.0, 7.0, "春季播种，秋季收获", {"N": 60, "P": 80, "K": 140}),
            ("FQ001", "番茄", "蔬菜", 6.0, 7.0, "春季播种，夏秋收获", {"N": 200, "P": 100, "K": 250}),
            ("HG001", "黄瓜", "蔬菜", 6.0, 7.0, "春夏播种，夏秋收获", {"N": 180, "P": 90, "K": 220}),
            ("LJ001", "辣椒", "蔬菜", 6.0, 7.5, "春季播种，夏秋收获", {"N": 160, "P": 80, "K": 200}),
            ("QZ001", "茄子", "蔬菜", 6.0, 7.0, "春季播种，夏秋收获", {"N": 170, "P": 85, "K": 210}),
            ("BC001", "白菜", "蔬菜", 6.0, 7.5, "秋季播种，冬季收获", {"N": 120, "P": 60, "K": 150}),
            ("LB001", "萝卜", "根茎类", 6.0, 7.0, "秋季播种，冬季收获", {"N": 100, "P": 50, "K": 180}),
        ]
        
        data = []
        for i, (code, name, category, ph_min, ph_max, season, nutrients) in enumerate(crops_data, 1):
            row = {
                'id': i,
                'crop_code': code,
                'crop_name': name,
                'category': category,
                'suitable_ph_min': ph_min,
                'suitable_ph_max': ph_max,
                'growing_season': season,
                'nutrient_requirements': json.dumps(nutrients, ensure_ascii=False),
                'created_at': fake.date_time_between(start_date='-2y', end_date='now')
            }
            data.append(row)
            self.crop_types.append(row)
        
        # 补充更多作物类型到500条
        categories = ["粮食作物", "蔬菜", "水果", "油料作物", "纤维作物", "药材", "花卉", "饲料作物"]
        crop_names = [
            "高粱", "谷子", "燕麦", "荞麦", "薏米", "芝麻", "花生", "向日葵", "油菜", "亚麻",
            "棉花", "大麻", "甘蔗", "甜菜", "烟草", "茶叶", "咖啡", "可可", "橡胶", "桑树",
            "苹果", "梨", "桃", "杏", "李", "樱桃", "葡萄", "柑橘", "柚子", "柠檬",
            "香蕉", "菠萝", "芒果", "荔枝", "龙眼", "杨梅", "草莓", "蓝莓", "猕猴桃", "石榴",
            "菠菜", "韭菜", "芹菜", "莴苣", "生菜", "苋菜", "空心菜", "茼蒿", "香菜", "薄荷",
            "豆角", "豌豆", "蚕豆", "扁豆", "四季豆", "红豆", "绿豆", "黑豆", "芸豆", "鹰嘴豆",
            "冬瓜", "南瓜", "丝瓜", "苦瓜", "西葫芦", "佛手瓜", "菜瓜", "蛇瓜", "瓠瓜", "扁豆",
            "土豆", "红薯", "山药", "芋头", "魔芋", "凉薯", "木薯", "菊芋", "荸荠", "慈菇"
        ]
        
        for i, name in enumerate(crop_names, len(data) + 1):
            if len(data) >= 500:
                break
            category = random.choice(categories)
            row = {
                'id': i,
                'crop_code': f"CR{i:03d}",
                'crop_name': name,
                'category': category,
                'suitable_ph_min': round(random.uniform(5.0, 6.5), 1),
                'suitable_ph_max': round(random.uniform(6.5, 8.0), 1),
                'growing_season': random.choice(["春季播种", "夏季播种", "秋季播种", "四季种植"]),
                'nutrient_requirements': json.dumps({
                    "N": random.randint(80, 250),
                    "P": random.randint(40, 120),
                    "K": random.randint(100, 300)
                }, ensure_ascii=False),
                'created_at': fake.date_time_between(start_date='-2y', end_date='now')
            }
            data.append(row)
            self.crop_types.append(row)
        
        # 继续补充到500条
        while len(data) < 500:
            i = len(data) + 1
            name = f"{fake.word()}作物{i}"
            category = random.choice(categories)
            row = {
                'id': i,
                'crop_code': f"CR{i:03d}",
                'crop_name': name,
                'category': category,
                'suitable_ph_min': round(random.uniform(5.0, 6.5), 1),
                'suitable_ph_max': round(random.uniform(6.5, 8.0), 1),
                'growing_season': random.choice(["春季播种", "夏季播种", "秋季播种", "四季种植"]),
                'nutrient_requirements': json.dumps({
                    "N": random.randint(80, 250),
                    "P": random.randint(40, 120),
                    "K": random.randint(100, 300)
                }, ensure_ascii=False),
                'created_at': fake.date_time_between(start_date='-2y', end_date='now')
            }
            data.append(row)
            self.crop_types.append(row)
        
        self.save_csv('crop_types.csv', data)
        return data
    
    def generate_fertilizer_products(self):
        """生成肥料产品数据"""
        print("生成肥料产品数据...")
        
        fertilizer_data = [
            ("NP001", "尿素", "中化集团", "氮肥", 46.0, 0, 0, 2200),
            ("NP002", "过磷酸钙", "云天化", "磷肥", 0, 16.0, 0, 1800),
            ("NP003", "硫酸钾", "盐湖股份", "钾肥", 0, 0, 50.0, 3200),
            ("NP004", "复合肥15-15-15", "史丹利", "复合肥", 15.0, 15.0, 15.0, 2800),
            ("NP005", "复合肥17-17-17", "金正大", "复合肥", 17.0, 17.0, 17.0, 3000),
            ("NP006", "磷酸二铵", "六国化工", "复合肥", 18.0, 46.0, 0, 3400),
            ("NP007", "硝酸铵", "晋煤集团", "氮肥", 34.0, 0, 0, 2400),
            ("NP008", "氯化钾", "东海钾肥", "钾肥", 0, 0, 60.0, 2900),
            ("NP009", "有机肥", "嘉施利", "有机肥", 5.0, 3.0, 2.0, 1200),
            ("NP010", "生物菌肥", "绿康生化", "生物肥", 8.0, 5.0, 5.0, 2600),
        ]
        
        data = []
        for i, (code, name, manufacturer, type_, n, p, k, price) in enumerate(fertilizer_data, 1):
            trace_elements = {}
            if random.choice([True, False]):
                trace_elements = {
                    "Fe": round(random.uniform(0.1, 2.0), 2),
                    "Zn": round(random.uniform(0.05, 1.0), 2),
                    "B": round(random.uniform(0.02, 0.5), 2)
                }
            
            row = {
                'id': i,
                'product_code': code,
                'product_name': name,
                'manufacturer': manufacturer,
                'fertilizer_type': type_,
                'nitrogen_content': n,
                'phosphorus_content': p,
                'potassium_content': k,
                'trace_elements': json.dumps(trace_elements, ensure_ascii=False) if trace_elements else '',
                'application_method': random.choice(["撒施", "条施", "穴施", "冲施", "叶面喷施"]),
                'price_per_ton': price,
                'shelf_life': random.randint(12, 36),
                'created_at': fake.date_time_between(start_date='-2y', end_date='now')
            }
            data.append(row)
            self.fertilizer_products.append(row)
        
        # 补充更多肥料产品到800条
        manufacturers = ["中化集团", "史丹利", "金正大", "嘉施利", "六国化工", "云天化", "盐湖股份", "东海钾肥"]
        fertilizer_types = ["氮肥", "磷肥", "钾肥", "复合肥", "有机肥", "生物肥", "微量元素肥", "叶面肥"]
        
        while len(data) < 800:
            i = len(data) + 1
            manufacturer = random.choice(manufacturers)
            fert_type = random.choice(fertilizer_types)
            
            if fert_type == "氮肥":
                n_content = round(random.uniform(20, 50), 1)
                p_content = 0
                k_content = 0
                price = random.randint(2000, 2800)
            elif fert_type == "磷肥":
                n_content = 0
                p_content = round(random.uniform(12, 20), 1)
                k_content = 0
                price = random.randint(1500, 2200)
            elif fert_type == "钾肥":
                n_content = 0
                p_content = 0
                k_content = round(random.uniform(40, 65), 1)
                price = random.randint(2800, 3500)
            else:  # 复合肥等
                n_content = round(random.uniform(5, 25), 1)
                p_content = round(random.uniform(5, 25), 1)
                k_content = round(random.uniform(5, 25), 1)
                price = random.randint(2200, 3800)
            
            trace_elements = {}
            if random.choice([True, False]):
                trace_elements = {
                    "Fe": round(random.uniform(0.1, 2.0), 2),
                    "Zn": round(random.uniform(0.05, 1.0), 2),
                    "B": round(random.uniform(0.02, 0.5), 2),
                    "Cu": round(random.uniform(0.02, 0.3), 2),
                    "Mn": round(random.uniform(0.1, 1.5), 2)
                }
            
            row = {
                'id': i,
                'product_code': f"FP{i:03d}",
                'product_name': f"{fert_type}{fake.word()}{i}",
                'manufacturer': manufacturer,
                'fertilizer_type': fert_type,
                'nitrogen_content': n_content,
                'phosphorus_content': p_content,
                'potassium_content': k_content,
                'trace_elements': json.dumps(trace_elements, ensure_ascii=False) if trace_elements else '',
                'application_method': random.choice(["撒施", "条施", "穴施", "冲施", "叶面喷施", "滴灌", "基施"]),
                'price_per_ton': price,
                'shelf_life': random.randint(12, 36),
                'created_at': fake.date_time_between(start_date='-2y', end_date='now')
            }
            data.append(row)
            self.fertilizer_products.append(row)
        
        self.save_csv('fertilizer_products.csv', data)
        return data
    
    def generate_users(self):
        """生成用户数据"""
        print("生成用户数据...")
        
        data = []
        roles = ["admin", "expert", "user", "viewer"]
        organizations = ["农业部", "省农科院", "市农技站", "县农业局", "农业合作社", "种植大户"]
        
        for i in range(1, 2001):
            username = f"user{i:04d}"
            password_hash = hashlib.md5(f"password{i}".encode()).hexdigest()
            
            row = {
                'id': i,
                'username': username,
                'password_hash': password_hash,
                'email': fake.email(),
                'phone': fake.phone_number(),
                'real_name': fake.name(),
                'organization': random.choice(organizations),
                'role': random.choice(roles),
                'region_id': random.choice(self.regions)['id'] if self.regions else None,
                'permissions': json.dumps([
                    "view_data", "export_data", "create_report"
                ], ensure_ascii=False),
                'last_login_time': fake.date_time_between(start_date='-30d', end_date='now'),
                'login_count': random.randint(1, 100),
                'status': random.choice(['active', 'inactive']),
                'created_at': fake.date_time_between(start_date='-2y', end_date='now'),
                'updated_at': fake.date_time_between(start_date='-1y', end_date='now')
            }
            data.append(row)
            self.users.append(row)
        
        self.save_csv('users.csv', data)
        return data
    
    def generate_monitoring_stations(self):
        """生成监测站点数据"""
        print("生成监测站点数据...")
        
        data = []
        station_types = ["国家级", "省级", "市级", "县级", "村级"]
        
        for i in range(1, 2001):
            region = random.choice(self.regions)
            soil_type = random.choice(self.soil_types) if self.soil_types else None
            
            equipment_list = [
                "pH计", "电导率仪", "土壤温度计", "水分仪"
            ]
            if random.choice([True, False]):
                equipment_list.extend(["光谱仪", "X射线荧光仪"])
            
            row = {
                'id': i,
                'station_code': f"ST{region['region_code'][:4]}{i:04d}",
                'station_name': f"{region['province']}{region.get('city', '')}{region.get('county', '')}监测站{i}",
                'region_id': region['id'],
                'latitude': region['latitude'] + random.uniform(-1, 1),
                'longitude': region['longitude'] + random.uniform(-1, 1),
                'altitude': random.randint(0, 3000),
                'station_type': random.choice(station_types),
                'soil_type_id': soil_type['id'] if soil_type else None,
                'establishment_date': fake.date_between(start_date='-10y', end_date='-1y'),
                'equipment_list': json.dumps(equipment_list, ensure_ascii=False),
                'monitoring_frequency': random.choice(["每日", "每周", "每月", "每季度"]),
                'responsible_person': fake.name(),
                'contact_info': fake.phone_number(),
                'status': random.choice(['active', 'maintenance', 'inactive']),
                'created_at': fake.date_time_between(start_date='-2y', end_date='now')
            }
            data.append(row)
            self.monitoring_stations.append(row)
        
        self.save_csv('monitoring_stations.csv', data)
        return data
    
    def generate_soil_samples(self):
        """生成土壤样本数据"""
        print("生成土壤样本数据...")
        
        data = []
        land_use_types = ["农田", "果园", "菜地", "草地", "林地", "荒地"]
        
        for i in range(1, 10001):
            region = random.choice(self.regions)
            soil_type = random.choice(self.soil_types) if self.soil_types else None
            crop = random.choice(self.crop_types) if self.crop_types else None
            
            row = {
                'id': i,
                'sample_code': f"SS{datetime.now().year}{i:06d}",
                'region_id': region['id'],
                'soil_type_id': soil_type['id'] if soil_type else None,
                'latitude': region['latitude'] + random.uniform(-2, 2),
                'longitude': region['longitude'] + random.uniform(-2, 2),
                'altitude': random.randint(0, 4000),
                'sampling_date': fake.date_between(start_date='-3y', end_date='now'),
                'sampling_depth': random.choice([15, 20, 25, 30]),
                'land_use_type': random.choice(land_use_types),
                'crop_id': crop['id'] if crop else None,
                'sampler_name': fake.name(),
                'created_at': fake.date_time_between(start_date='-3y', end_date='now')
            }
            data.append(row)
            self.soil_samples.append(row)
        
        self.save_csv('soil_samples.csv', data)
        return data
    
    def generate_soil_test_data(self):
        """生成土壤检测数据"""
        print("生成土壤检测数据...")
        
        data = []
        institutions = ["国家土壤质量监测中心", "省农科院检测中心", "市农业检测站", "第三方检测机构"]
        
        for sample in self.soil_samples:
            row = {
                'id': sample['id'],
                'sample_id': sample['id'],
                'ph_value': round(random.uniform(4.5, 9.0), 2),
                'organic_matter': round(random.uniform(0.8, 4.5), 2),
                'total_nitrogen': round(random.uniform(500, 2500), 2),
                'available_phosphorus': round(random.uniform(5, 80), 2),
                'available_potassium': round(random.uniform(50, 300), 2),
                'available_nitrogen': round(random.uniform(20, 150), 2),
                'cation_exchange_capacity': round(random.uniform(8, 35), 2),
                'salinity': round(random.uniform(0.1, 5.0), 2),
                'moisture_content': round(random.uniform(10, 40), 2),
                'bulk_density': round(random.uniform(1.1, 1.6), 2),
                'porosity': round(random.uniform(35, 60), 2),
                'test_date': sample['sampling_date'],
                'test_institution': random.choice(institutions),
                'created_at': sample['created_at']
            }
            data.append(row)
        
        self.save_csv('soil_test_data.csv', data)
        return data
    
    def generate_trace_elements(self):
        """生成微量元素检测数据"""
        print("生成微量元素检测数据...")
        
        data = []
        # 随机选择80%的样本进行微量元素检测
        selected_samples = random.sample(self.soil_samples, int(len(self.soil_samples) * 0.8))
        
        for i, sample in enumerate(selected_samples, 1):
            row = {
                'id': i,
                'sample_id': sample['id'],
                'iron': round(random.uniform(10, 300), 2),
                'manganese': round(random.uniform(5, 150), 2),
                'zinc': round(random.uniform(0.5, 15), 2),
                'copper': round(random.uniform(0.2, 8), 2),
                'boron': round(random.uniform(0.1, 2.0), 2),
                'molybdenum': round(random.uniform(0.05, 1.5), 2),
                'chlorine': round(random.uniform(10, 200), 2),
                'sulfur': round(random.uniform(20, 400), 2),
                'calcium': round(random.uniform(500, 8000), 2),
                'magnesium': round(random.uniform(100, 2000), 2),
                'test_date': sample['sampling_date'],
                'created_at': sample['created_at']
            }
            data.append(row)
        
        self.save_csv('trace_elements.csv', data)
        return data
    
    def generate_soil_quality_assessment(self):
        """生成土壤质量评估数据"""
        print("生成土壤质量评估数据...")
        
        data = []
        grades = ["优", "良", "中", "差"]
        assessors = ["张教授", "李专家", "王研究员", "赵工程师", "陈博士"]
        
        for sample in self.soil_samples:
            # 基于土壤检测数据计算评分
            fertility_score = round(random.uniform(60, 95), 2)
            ph_score = round(random.uniform(70, 90), 2)
            organic_matter_score = round(random.uniform(65, 85), 2)
            nutrient_score = round(random.uniform(70, 88), 2)
            physical_property_score = round(random.uniform(75, 92), 2)
            
            comprehensive_score = (fertility_score + ph_score + organic_matter_score + nutrient_score + physical_property_score) / 5
            
            if comprehensive_score >= 85:
                grade = "优"
            elif comprehensive_score >= 75:
                grade = "良"
            elif comprehensive_score >= 65:
                grade = "中"
            else:
                grade = "差"
            
            limiting_factors = []
            if ph_score < 75:
                limiting_factors.append("pH值偏离适宜范围")
            if organic_matter_score < 70:
                limiting_factors.append("有机质含量偏低")
            if nutrient_score < 75:
                limiting_factors.append("养分不平衡")
            
            row = {
                'id': sample['id'],
                'sample_id': sample['id'],
                'fertility_score': fertility_score,
                'ph_score': ph_score,
                'organic_matter_score': organic_matter_score,
                'nutrient_score': nutrient_score,
                'physical_property_score': physical_property_score,
                'comprehensive_grade': grade,
                'limiting_factors': "; ".join(limiting_factors) if limiting_factors else "无明显限制因子",
                'improvement_suggestions': self._generate_improvement_suggestion(),
                'assessment_date': sample['sampling_date'],
                'assessor': random.choice(assessors),
                'created_at': sample['created_at']
            }
            data.append(row)
        
        self.save_csv('soil_quality_assessment.csv', data)
        return data
    
    def generate_crop_suitability(self):
        """生成作物适宜性评估数据"""
        print("生成作物适宜性评估数据...")
        
        data = []
        suitability_levels = ["高度适宜", "中度适宜", "勉强适宜", "不适宜"]
        
        # 为每个样本评估多种作物的适宜性
        for i, sample in enumerate(self.soil_samples):
            # 每个样本评估5-8种作物
            crops_to_assess = random.sample(self.crop_types, random.randint(5, 8))
            
            for j, crop in enumerate(crops_to_assess):
                record_id = i * 8 + j + 1
                suitability_score = round(random.uniform(40, 95), 2)
                
                if suitability_score >= 80:
                    level = "高度适宜"
                    yield_potential = round(random.uniform(800, 1200), 2)
                elif suitability_score >= 70:
                    level = "中度适宜"
                    yield_potential = round(random.uniform(600, 800), 2)
                elif suitability_score >= 60:
                    level = "勉强适宜"
                    yield_potential = round(random.uniform(400, 600), 2)
                else:
                    level = "不适宜"
                    yield_potential = round(random.uniform(200, 400), 2)
                
                limiting_factors = {
                    "ph_limitation": random.choice([True, False]),
                    "nutrient_limitation": random.choice([True, False]),
                    "climate_limitation": random.choice([True, False])
                }
                
                row = {
                    'id': record_id,
                    'sample_id': sample['id'],
                    'crop_id': crop['id'],
                    'suitability_score': suitability_score,
                    'suitability_level': level,
                    'limiting_factors': json.dumps(limiting_factors, ensure_ascii=False),
                    'yield_potential': yield_potential,
                    'risk_assessment': self._generate_risk_assessment(suitability_score),
                    'management_recommendations': self._generate_management_recommendations(),
                    'assessment_date': sample['sampling_date'],
                    'created_at': sample['created_at']
                }
                data.append(row)
                
                if len(data) >= 50000:  # 限制到50000条
                    break
            
            if len(data) >= 50000:
                break
        
        self.save_csv('crop_suitability.csv', data)
        return data
    
    def generate_fertilizer_plans(self):
        """生成施肥方案数据"""
        print("生成施肥方案数据...")
        
        data = []
        plan_creators = ["农技专家", "土壤专家", "作物专家", "系统自动生成"]
        
        # 为部分样本生成施肥方案
        num_plans = min(15000, len(self.soil_samples))
        selected_samples = random.sample(self.soil_samples, num_plans)
        
        for i, sample in enumerate(selected_samples, 1):
            crop = random.choice(self.crop_types)
            
            base_fertilizer = {
                "复合肥": f"{random.randint(30, 60)}kg/亩",
                "有机肥": f"{random.randint(1000, 3000)}kg/亩",
                "石灰": f"{random.randint(50, 150)}kg/亩" if random.choice([True, False]) else ""
            }
            
            topdressing_plan = [
                {
                    "时期": "播种期",
                    "肥料": "复合肥",
                    "用量": f"{random.randint(10, 25)}kg/亩"
                },
                {
                    "时期": "生长期",
                    "肥料": "尿素",
                    "用量": f"{random.randint(15, 30)}kg/亩"
                },
                {
                    "时期": "开花期",
                    "肥料": "磷钾肥",
                    "用量": f"{random.randint(10, 20)}kg/亩"
                }
            ]
            
            total_cost = round(random.uniform(200, 800), 2)
            expected_benefit = round(total_cost * random.uniform(2.5, 4.0), 2)
            
            row = {
                'id': i,
                'sample_id': sample['id'],
                'crop_id': crop['id'],
                'plan_name': f"{crop['crop_name']}专用施肥方案{i}",
                'target_yield': round(random.uniform(400, 1000), 2),
                'base_fertilizer': json.dumps(base_fertilizer, ensure_ascii=False),
                'topdressing_plan': json.dumps(topdressing_plan, ensure_ascii=False),
                'total_cost': total_cost,
                'expected_benefit': expected_benefit,
                'application_instructions': self._generate_application_instructions(),
                'created_date': sample['sampling_date'],
                'creator': random.choice(plan_creators),
                'status': random.choice(['active', 'draft', 'archived']),
                'created_at': sample['created_at']
            }
            data.append(row)
        
        self.save_csv('fertilizer_plans.csv', data)
        return data
    
    def generate_historical_monitoring_data(self):
        """生成历史监测数据"""
        print("生成历史监测数据...")
        
        data = []
        weather_conditions = ["晴", "多云", "阴", "小雨", "中雨", "大雨"]
        growth_stages = ["播种期", "出苗期", "生长期", "开花期", "结果期", "成熟期"]
        
        # 为每个监测站点生成50条历史数据
        for station in self.monitoring_stations:
            for i in range(50):
                monitoring_date = fake.date_between(start_date='-2y', end_date='now')
                
                row = {
                    'id': len(data) + 1,
                    'station_id': station['id'],
                    'monitoring_date': monitoring_date,
                    'ph_value': round(random.uniform(5.0, 8.5), 2),
                    'organic_matter': round(random.uniform(1.0, 4.0), 2),
                    'available_nitrogen': round(random.uniform(30, 120), 2),
                    'available_phosphorus': round(random.uniform(8, 50), 2),
                    'available_potassium': round(random.uniform(80, 250), 2),
                    'moisture_content': round(random.uniform(15, 35), 2),
                    'temperature': round(random.uniform(-5, 35), 2),
                    'salinity': round(random.uniform(0.2, 3.0), 2),
                    'compaction_degree': round(random.uniform(1.0, 5.0), 2),
                    'weather_conditions': random.choice(weather_conditions),
                    'crop_growth_stage': random.choice(growth_stages),
                    'data_quality': random.choice(['normal', 'good', 'excellent']),
                    'remarks': fake.text(max_nb_chars=100) if random.choice([True, False]) else '',
                    'created_at': fake.date_time_between(start_date=monitoring_date, end_date='now')
                }
                data.append(row)
                
                if len(data) >= 100000:  # 限制到100000条
                    break
            
            if len(data) >= 100000:
                break
        
        self.save_csv('historical_monitoring_data.csv', data)
        return data
    
    def generate_operation_logs(self):
        """生成操作日志数据"""
        print("生成操作日志数据...")
        
        data = []
        operation_types = ["查询", "导出", "新增", "修改", "删除", "分析", "生成报告"]
        target_tables = ["soil_samples", "soil_test_data", "crop_suitability", "fertilizer_plans"]
        result_statuses = ["成功", "失败", "警告"]
        
        for i in range(1, 50001):
            user = random.choice(self.users) if self.users else None
            operation_type = random.choice(operation_types)
            target_table = random.choice(target_tables)
            result_status = random.choice(result_statuses)
            
            row = {
                'id': i,
                'user_id': user['id'] if user else None,
                'operation_type': operation_type,
                'target_table': target_table,
                'target_id': random.randint(1, 10000),
                'operation_description': f"用户{operation_type}{target_table}数据",
                'ip_address': fake.ipv4(),
                'user_agent': fake.user_agent(),
                'operation_time': fake.date_time_between(start_date='-1y', end_date='now'),
                'execution_time': round(random.uniform(0.1, 5.0), 3),
                'result_status': result_status,
                'error_message': fake.text(max_nb_chars=100) if result_status == "失败" else '',
            }
            data.append(row)
        
        self.save_csv('operation_logs.csv', data)
        return data
    
    def generate_statistical_reports(self):
        """生成统计分析报告数据"""
        print("生成统计分析报告数据...")
        
        data = []
        report_types = ["月度报告", "季度报告", "年度报告", "专题报告", "区域分析报告"]
        generators = ["系统自动", "专家生成", "管理员生成"]
        
        for i in range(1, 1001):
            region_scope = random.sample([r['province'] for r in self.regions[:10]], random.randint(1, 3))
            
            key_findings = {
                "土壤质量状况": f"{random.randint(70, 90)}%的土壤质量良好",
                "主要问题": random.choice(["酸化问题突出", "有机质偏低", "养分不平衡"]),
                "改良建议": "加强有机肥施用，合理调节pH值"
            }
            
            charts_data = {
                "pH分布": {"酸性": random.randint(20, 40), "中性": random.randint(40, 60), "碱性": random.randint(10, 30)},
                "有机质状况": {"高": random.randint(15, 25), "中": random.randint(50, 70), "低": random.randint(15, 25)}
            }
            
            row = {
                'id': i,
                'report_code': f"RPT{datetime.now().year}{i:04d}",
                'report_title': f"{random.choice(region_scope)}{random.choice(report_types)}",
                'report_type': random.choice(report_types),
                'region_scope': json.dumps(region_scope, ensure_ascii=False),
                'time_period': f"{fake.date_between(start_date='-1y', end_date='-1m')}至{fake.date_between(start_date='-1m', end_date='now')}",
                'data_source': "土壤监测网络",
                'analysis_method': random.choice(["统计分析", "GIS分析", "机器学习", "专家评估"]),
                'key_findings': json.dumps(key_findings, ensure_ascii=False),
                'charts_data': json.dumps(charts_data, ensure_ascii=False),
                'conclusions': fake.text(max_nb_chars=200),
                'recommendations': fake.text(max_nb_chars=200),
                'generated_date': fake.date_between(start_date='-6m', end_date='now'),
                'generator': random.choice(generators),
                'review_status': random.choice(['draft', 'reviewed', 'published']),
                'download_count': random.randint(0, 100),
                'created_at': fake.date_time_between(start_date='-6m', end_date='now')
            }
            data.append(row)
        
        self.save_csv('statistical_reports.csv', data)
        return data
    
    def generate_anomaly_data(self):
        """生成异常数据记录"""
        print("生成异常数据记录数据...")
        
        data = []
        anomaly_types = ["数值异常", "缺失值", "逻辑错误", "重复数据", "超出范围"]
        data_sources = ["soil_test_data", "monitoring_data", "manual_input"]
        severity_levels = ["低", "中", "高", "严重"]
        detection_methods = ["自动检测", "人工发现", "系统校验", "专家审核"]
        
        for i in range(1, 3001):
            row = {
                'id': i,
                'data_source': random.choice(data_sources),
                'source_id': random.randint(1, 10000),
                'anomaly_type': random.choice(anomaly_types),
                'anomaly_field': random.choice(['ph_value', 'organic_matter', 'nitrogen', 'phosphorus', 'potassium']),
                'original_value': str(round(random.uniform(-1, 15), 2)),
                'expected_range': random.choice(['4.5-8.5', '0.8-4.5', '20-150', '5-80', '50-300']),
                'severity_level': random.choice(severity_levels),
                'detection_method': random.choice(detection_methods),
                'detection_date': fake.date_between(start_date='-1y', end_date='now'),
                'handled_status': random.choice(['pending', 'processing', 'resolved', 'ignored']),
                'handler': random.choice(['张工程师', '李专家', '王管理员', '系统自动']),
                'handle_date': fake.date_between(start_date='-6m', end_date='now') if random.choice([True, False]) else None,
                'handle_method': fake.text(max_nb_chars=100) if random.choice([True, False]) else '',
                'remarks': fake.text(max_nb_chars=100) if random.choice([True, False]) else '',
                'created_at': fake.date_time_between(start_date='-1y', end_date='now')
            }
            data.append(row)
        
        self.save_csv('anomaly_data.csv', data)
        return data
    
    def generate_data_dictionary(self):
        """生成数据字典"""
        print("生成数据字典数据...")
        
        data = []
        dict_data = [
            ("soil_type", "CT001", "潮土", "潮土", 1, "", "", "N", "0"),
            ("soil_type", "HT001", "黄土", "黄土", 2, "", "", "N", "0"),
            ("soil_type", "RT001", "红土", "红土", 3, "", "", "N", "0"),
            ("crop_category", "grain", "粮食作物", "粮食作物", 1, "", "", "N", "0"),
            ("crop_category", "vegetable", "蔬菜", "蔬菜", 2, "", "", "N", "0"),
            ("crop_category", "fruit", "水果", "水果", 3, "", "", "N", "0"),
            ("fertilizer_type", "nitrogen", "氮肥", "氮肥", 1, "", "", "N", "0"),
            ("fertilizer_type", "phosphorus", "磷肥", "磷肥", 2, "", "", "N", "0"),
            ("fertilizer_type", "potassium", "钾肥", "钾肥", 3, "", "", "N", "0"),
            ("user_role", "admin", "管理员", "admin", 1, "", "", "N", "0"),
            ("user_role", "expert", "专家", "expert", 2, "", "", "N", "0"),
            ("user_role", "user", "普通用户", "user", 3, "", "", "N", "0"),
            ("status", "active", "正常", "active", 1, "color-success", "", "Y", "0"),
            ("status", "inactive", "停用", "inactive", 2, "color-danger", "", "N", "0"),
            ("quality_grade", "excellent", "优", "优", 1, "color-success", "", "N", "0"),
            ("quality_grade", "good", "良", "良", 2, "color-info", "", "N", "0"),
            ("quality_grade", "fair", "中", "中", 3, "color-warning", "", "N", "0"),
            ("quality_grade", "poor", "差", "差", 4, "color-danger", "", "N", "0"),
        ]
        
        for i, (dict_type, code, label, value, sort, css_class, list_class, is_default, status) in enumerate(dict_data, 1):
            row = {
                'id': i,
                'dict_type': dict_type,
                'dict_code': code,
                'dict_label': label,
                'dict_value': value,
                'dict_sort': sort,
                'css_class': css_class,
                'list_class': list_class,
                'is_default': is_default,
                'status': status,
                'created_at': fake.date_time_between(start_date='-2y', end_date='now'),
                'updated_at': fake.date_time_between(start_date='-1y', end_date='now')
            }
            data.append(row)
        
        # 补充更多字典数据到500条
        dict_types = ["monitoring_frequency", "equipment_type", "weather_condition", "growth_stage", "land_use"]
        while len(data) < 500:
            i = len(data) + 1
            dict_type = random.choice(dict_types)
            code = f"{dict_type}_{i}"
            label = f"{fake.word()}_{i}"
            
            row = {
                'id': i,
                'dict_type': dict_type,
                'dict_code': code,
                'dict_label': label,
                'dict_value': label,
                'dict_sort': i,
                'css_class': '',
                'list_class': '',
                'is_default': 'N',
                'status': '0',
                'created_at': fake.date_time_between(start_date='-2y', end_date='now'),
                'updated_at': fake.date_time_between(start_date='-1y', end_date='now')
            }
            data.append(row)
        
        self.save_csv('data_dictionary.csv', data)
        return data
    
    def _generate_improvement_suggestion(self):
        """生成改良建议"""
        suggestions = [
            "增施有机肥，提高土壤有机质含量",
            "合理施用石灰，调节土壤pH值",
            "深耕松土，改善土壤结构",
            "轮作倒茬，维护土壤生态平衡",
            "科学施肥，平衡土壤养分"
        ]
        return random.choice(suggestions)
    
    def _generate_risk_assessment(self, score):
        """生成风险评估"""
        if score >= 80:
            return "风险较低，适宜种植"
        elif score >= 70:
            return "风险中等，需要适当管理"
        elif score >= 60:
            return "风险较高，需要重点关注"
        else:
            return "风险很高，不建议种植"
    
    def _generate_management_recommendations(self):
        """生成管理建议"""
        recommendations = [
            "加强田间管理，及时灌溉施肥",
            "监测病虫害，及时防治",
            "合理密植，保证通风透光",
            "科学轮作，避免连作障碍",
            "改良土壤，提高地力"
        ]
        return random.choice(recommendations)
    
    def _generate_application_instructions(self):
        """生成施用说明"""
        instructions = [
            "基肥在播种前7-10天施入，深翻入土",
            "追肥分3次施用，根据作物生长情况调整",
            "有机肥需充分腐熟后使用",
            "叶面肥在早晨或傍晚喷施效果最佳",
            "施肥后及时浇水，促进养分吸收"
        ]
        return random.choice(instructions)
    
    def save_csv(self, filename, data):
        """保存数据到CSV文件"""
        if not data:
            return
        
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"已生成 {filename}，共 {len(data)} 条记录")

def main():
    generator = SoilDataCSVGenerator()
    
    # 按依赖关系生成数据
    print("开始生成CSV数据文件...")
    
    # 基础数据
    generator.generate_regions()
    generator.generate_soil_types()
    generator.generate_crop_types()
    generator.generate_fertilizer_products()
    generator.generate_data_dictionary()
    
    # 用户和站点
    generator.generate_users()
    generator.generate_monitoring_stations()
    
    # 土壤样本和检测数据
    generator.generate_soil_samples()
    generator.generate_soil_test_data()
    generator.generate_trace_elements()
    
    # 评估和分析数据
    generator.generate_soil_quality_assessment()
    generator.generate_crop_suitability()
    generator.generate_fertilizer_plans()
    
    # 监测和日志数据
    generator.generate_historical_monitoring_data()
    generator.generate_operation_logs()
    generator.generate_statistical_reports()
    generator.generate_anomaly_data()
    
    print("所有CSV文件生成完成！")

if __name__ == "__main__":
    main()