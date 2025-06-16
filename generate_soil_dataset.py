#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
土壤问诊数据集生成器
自动生成大量用于微调大模型的土壤诊断对话数据
"""

import json
import random
import itertools

class SoilDiagnosisDataGenerator:
    def __init__(self):
        # 土壤类型
        self.soil_types = ["潮土", "黄土", "红土", "黑土", "沙土", "粘土", "壤土", "水稻土", "褐土", "盐碱土"]
        
        # 作物类型
        self.crops = ["玉米", "小麦", "水稻", "大豆", "番茄", "黄瓜", "辣椒", "茄子", "白菜", "萝卜", 
                     "胡萝卜", "马铃薯", "红薯", "花生", "棉花", "油菜", "苹果", "梨", "桃", "葡萄"]
        
        # 地区
        self.regions = ["河北省", "山东省", "河南省", "江苏省", "安徽省", "湖北省", "湖南省", "广东省", 
                       "四川省", "陕西省", "山西省", "甘肃省", "新疆", "内蒙古", "东北地区", "华北平原"]
        
        # pH值范围
        self.ph_values = [4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0]
        
        # 有机质含量范围
        self.organic_matter = [0.8, 1.2, 1.5, 1.8, 2.0, 2.2, 2.5, 2.8, 3.0, 3.5, 4.0]
        
        # 问题类型模板
        self.problem_templates = {
            "土壤检测": self.generate_soil_test_qa,
            "缺素诊断": self.generate_deficiency_qa,
            "土壤改良": self.generate_improvement_qa,
            "施肥方案": self.generate_fertilizer_qa,
            "病害诊断": self.generate_disease_qa,
            "作物适宜性": self.generate_suitability_qa,
            "盐碱地治理": self.generate_salinity_qa,
            "有机农业": self.generate_organic_qa,
            "水分管理": self.generate_water_qa,
            "土壤板结": self.generate_compaction_qa
        }
        
    def generate_soil_test_qa(self):
        """生成土壤检测分析类问答"""
        region = random.choice(self.regions)
        soil_type = random.choice(self.soil_types)
        crop = random.choice(self.crops)
        ph = random.choice(self.ph_values)
        organic = random.choice(self.organic_matter)
        nitrogen = random.randint(20, 120)
        phosphorus = random.randint(8, 50)
        potassium = random.randint(60, 200)
        
        instruction = "请分析这份土壤检测报告"
        input_text = f"采样地点：{region}；土壤类型：{soil_type}；pH值：{ph}；有机质：{organic}%；速效氮：{nitrogen}mg/kg；速效磷：{phosphorus}mg/kg；速效钾：{potassium}mg/kg；种植作物：{crop}"
        
        # 生成分析结果
        ph_analysis = self.analyze_ph(ph)
        organic_analysis = self.analyze_organic_matter(organic)
        npk_analysis = self.analyze_npk(nitrogen, phosphorus, potassium, crop)
        
        output = f"""**土壤检测报告分析：**

**基本信息：**
- 采样地点：{region}
- 土壤类型：{soil_type}
- 目标作物：{crop}

**土壤肥力评价：**
1. **酸碱度（pH {ph}）**：{ph_analysis}
2. **有机质（{organic}%）**：{organic_analysis}
3. **氮磷钾状况**：{npk_analysis}

**施肥建议：**
{self.generate_fertilizer_recommendation(nitrogen, phosphorus, potassium, crop)}

**改良建议：**
{self.generate_improvement_suggestion(ph, organic, soil_type)}"""
        
        return {
            "instruction": instruction,
            "input": input_text,
            "output": output
        }
    
    def generate_deficiency_qa(self):
        """生成缺素症状诊断类问答"""
        deficiency_types = {
            "氮": {"症状": "叶片发黄，从下往上黄化", "原因": "氮素缺乏", "解决": "追施尿素15-20kg/亩"},
            "磷": {"症状": "叶片发红发紫，植株矮小", "原因": "磷素缺乏", "解决": "施用过磷酸钙20-30kg/亩"},
            "钾": {"症状": "叶片边缘焦枯", "原因": "钾素缺乏", "解决": "追施硫酸钾15-20kg/亩"},
            "铁": {"症状": "新叶黄绿相间条纹", "原因": "缺铁症", "解决": "叶面喷施硫酸亚铁0.2%溶液"},
            "锌": {"症状": "叶片小而黄，嫩梢短", "原因": "缺锌症", "解决": "叶面喷施硫酸锌0.1%溶液"},
            "硼": {"症状": "花而不实，果实畸形", "原因": "缺硼症", "解决": "叶面喷施硼砂0.1%溶液"}
        }
        
        element = random.choice(list(deficiency_types.keys()))
        crop = random.choice(self.crops)
        deficiency = deficiency_types[element]
        
        instruction = f"{crop}出现缺素症状，请诊断"
        input_text = f"作物：{crop}；症状：{deficiency['症状']}；土壤pH：{random.choice(self.ph_values)}；最近施肥情况：复合肥"
        
        output = f"""**{deficiency['原因']}诊断：**

**症状分析：**
- {deficiency['症状']}：典型的{element}素缺乏症状
- 发生原因：土壤中{element}素供应不足或吸收受阻

**解决方案：**

**立即措施：**
1. **{deficiency['解决']}**
2. **叶面补充**：快速补充{element}素
3. **连续处理**：每7-10天处理一次，连续2-3次

**预防措施：**
1. **平衡施肥**：注重{element}素的补充
2. **土壤改良**：改善土壤理化性质
3. **定期检测**：监测土壤养分状况

**预期效果：**
处理后7-10天症状开始改善，15-20天基本恢复正常。"""
        
        return {
            "instruction": instruction,
            "input": input_text,
            "output": output
        }
    
    def generate_improvement_qa(self):
        """生成土壤改良类问答"""
        problems = {
            "酸性土壤": {
                "特征": "pH值偏低，作物生长不良",
                "改良": "施用石灰或白云石粉调节pH值"
            },
            "碱性土壤": {
                "特征": "pH值偏高，微量元素缺乏",
                "改良": "施用硫磺粉或酸性肥料降低pH值"
            },
            "盐碱土": {
                "特征": "土壤盐分高，作物难以生存",
                "改良": "排水洗盐，施用石膏改良"
            },
            "板结土壤": {
                "特征": "土壤坚硬，透气性差",
                "改良": "深翻松土，增施有机肥"
            },
            "贫瘠土壤": {
                "特征": "有机质含量低，肥力差",
                "改良": "大量施用有机肥，培肥土壤"
            }
        }
        
        problem_type = random.choice(list(problems.keys()))
        problem = problems[problem_type]
        soil_type = random.choice(self.soil_types)
        
        instruction = f"如何改良{problem_type}？"
        input_text = f"土壤类型：{soil_type}；问题：{problem['特征']}；面积：10亩"
        
        output = f"""**{problem_type}改良方案：**

**问题诊断：**
- 土壤类型：{soil_type}
- 主要问题：{problem['特征']}
- 需要系统性改良

**改良措施：**

**主要方法：**
1. **{problem['改良']}**
2. **有机改良**：大量施用有机肥3000-5000kg/亩
3. **物理改良**：深耕松土，改善土壤结构

**配套措施：**
1. **排水系统**：建立完善的排水网络
2. **生物改良**：种植适宜的改良作物
3. **化学调理**：使用土壤调理剂

**实施计划：**
- **第1年**：重点改良，大量投入
- **第2年**：巩固效果，持续改良
- **第3年**：维护管理，监测效果

**预期效果：**
经过2-3年系统改良，土壤理化性质明显改善，作物产量提高30-50%。"""
        
        return {
            "instruction": instruction,
            "input": input_text,
            "output": output
        }
    
    def analyze_ph(self, ph):
        """分析pH值"""
        if ph < 5.5:
            return "强酸性，需要调节"
        elif ph < 6.5:
            return "酸性，部分作物可能受影响"
        elif ph <= 7.5:
            return "适宜，大多数作物适合"
        elif ph <= 8.5:
            return "偏碱性，注意微量元素补充"
        else:
            return "强碱性，需要降低pH值"
    
    def analyze_organic_matter(self, organic):
        """分析有机质含量"""
        if organic < 1.0:
            return "严重缺乏，需要大量补充"
        elif organic < 2.0:
            return "偏低，需要增加投入"
        elif organic <= 3.0:
            return "中等水平，符合一般要求"
        else:
            return "丰富，土壤肥力较好"
    
    def analyze_npk(self, n, p, k, crop):
        """分析氮磷钾状况"""
        n_status = "充足" if n > 80 else "中等" if n > 40 else "偏低"
        p_status = "充足" if p > 30 else "中等" if p > 15 else "偏低"
        k_status = "充足" if k > 150 else "中等" if k > 80 else "偏低"
        
        return f"氮素{n_status}({n}mg/kg)，磷素{p_status}({p}mg/kg)，钾素{k_status}({k}mg/kg)"
    
    def generate_fertilizer_recommendation(self, n, p, k, crop):
        """生成施肥建议"""
        recommendations = []
        
        if n < 60:
            recommendations.append("- **补充氮肥**：追施尿素15-20kg/亩")
        if p < 20:
            recommendations.append("- **补充磷肥**：施用过磷酸钙20-30kg/亩")
        if k < 100:
            recommendations.append("- **补充钾肥**：施用硫酸钾10-15kg/亩")
        
        recommendations.append("- **有机肥**：施用腐熟农家肥2000-3000kg/亩")
        recommendations.append("- **叶面肥**：生长期喷施磷酸二氢钾")
        
        return "\n".join(recommendations)
    
    def generate_improvement_suggestion(self, ph, organic, soil_type):
        """生成改良建议"""
        suggestions = []
        
        if ph < 6.0:
            suggestions.append("- **调节酸性**：施用石灰100-200kg/亩")
        elif ph > 8.0:
            suggestions.append("- **降低碱性**：施用硫磺粉或酸性肥料")
        
        if organic < 2.0:
            suggestions.append("- **提高有机质**：增施有机肥，秸秆还田")
        
        suggestions.append("- **改善结构**：深耕松土，建立团粒结构")
        suggestions.append("- **合理轮作**：实施科学的轮作制度")
        
        return "\n".join(suggestions)
    
    def generate_fertilizer_qa(self):
        """生成施肥方案类问答"""
        crop = random.choice(self.crops)
        soil_type = random.choice(self.soil_types)
        target_yield = random.randint(3000, 6000)
        current_yield = random.randint(2000, target_yield-500)
        
        instruction = f"制定{crop}施肥方案"
        input_text = f"作物：{crop}；土壤类型：{soil_type}；目前产量：{current_yield}kg/亩；目标产量：{target_yield}kg/亩"
        
        output = f"""**{crop}施肥方案：**

**现状分析：**
- 当前产量：{current_yield}kg/亩
- 目标产量：{target_yield}kg/亩
- 增产空间：{target_yield-current_yield}kg/亩

**施肥计划：**

**基肥（播种前）：**
- 有机肥：腐熟农家肥2000-3000kg/亩
- 复合肥：15-15-15复合肥30-40kg/亩

**追肥计划：**
- 第一次：生长前期追施尿素10-15kg/亩
- 第二次：生长旺期追施复合肥20kg/亩
- 第三次：后期追施钾肥10kg/亩

**叶面肥：**
- 关键期喷施磷酸二氢钾0.2%溶液2-3次

**预期效果：**
通过科学施肥可实现目标产量，提高{crop}品质和经济效益。"""
        
        return {
            "instruction": instruction,
            "input": input_text,
            "output": output
        }
    
    def generate_disease_qa(self):
        """生成病害诊断类问答"""
        diseases = {
            "根腐病": {"症状": "根系发黑腐烂，叶片萎蔫", "原因": "土壤积水，病菌感染"},
            "立枯病": {"症状": "幼苗猝倒，茎基部缢缩", "原因": "土壤湿度大，病原菌侵染"},
            "青枯病": {"症状": "叶片萎蔫，茎秆维管束变褐", "原因": "细菌感染，土壤传播"}
        }
        
        disease = random.choice(list(diseases.keys()))
        crop = random.choice(self.crops)
        disease_info = diseases[disease]
        
        instruction = f"{crop}{disease}防治方法"
        input_text = f"作物：{crop}；症状：{disease_info['症状']}；发病原因：{disease_info['原因']}"
        
        output = f"""**{crop}{disease}防治方案：**

**病害诊断：**
- 病害名称：{disease}
- 主要症状：{disease_info['症状']}
- 发病原因：{disease_info['原因']}

**防治措施：**

**农业防治：**
1. **土壤改良**：改善排水，避免积水
2. **轮作倒茬**：与非寄主作物轮作
3. **种子处理**：播前种子消毒

**化学防治：**
1. **土壤消毒**：使用多菌灵等杀菌剂
2. **喷雾防治**：定期喷施保护性杀菌剂
3. **灌根处理**：发病初期药剂灌根

**预防措施：**
- 选用抗病品种
- 科学水肥管理
- 及时清除病残体
- 加强田间监测"""
        
        return {
            "instruction": instruction,
            "input": input_text,
            "output": output
        }
    
    def generate_suitability_qa(self):
        """生成作物适宜性类问答"""
        soil_type = random.choice(self.soil_types)
        ph = random.choice(self.ph_values)
        region = random.choice(self.regions)
        
        instruction = "这块地适合种什么作物？"
        input_text = f"土壤类型：{soil_type}；pH值：{ph}；地理位置：{region}；排水条件：良好"
        
        # 根据土壤条件推荐作物
        suitable_crops = self.get_suitable_crops(soil_type, ph)
        
        output = f"""**土地适宜性分析：**

**土壤条件：**
- 土壤类型：{soil_type}
- pH值：{ph}
- 地理位置：{region}
- 排水条件：良好

**推荐作物：**

**最适宜作物：**
{chr(10).join([f"- **{crop}**：{reason}" for crop, reason in suitable_crops[:3]])}

**适宜作物：**
{chr(10).join([f"- {crop}" for crop, _ in suitable_crops[3:6]])}

**种植建议：**
1. **土壤改良**：根据作物需求调整土壤条件
2. **科学施肥**：制定针对性施肥方案  
3. **合理轮作**：建立可持续种植制度

**注意事项：**
- 定期检测土壤理化性质
- 选择优质抗逆品种
- 加强田间管理"""
        
        return {
            "instruction": instruction,
            "input": input_text,
            "output": output
        }
    
    def generate_salinity_qa(self):
        """生成盐碱地治理类问答"""
        instruction = "盐碱地如何改良？"
        ec_value = round(random.uniform(2.0, 6.0), 1)
        ph = round(random.uniform(8.0, 9.5), 1)
        
        input_text = f"土壤EC值：{ec_value}ms/cm；pH值：{ph}；面积：20亩；主要问题：土壤盐分高"
        
        salinity_level = "轻度" if ec_value < 3 else "中度" if ec_value < 5 else "重度"
        
        output = f"""**盐碱地改良方案：**

**盐碱化评估：**
- EC值：{ec_value}ms/cm（{salinity_level}盐化）
- pH值：{ph}（强碱性）
- 改良难度：{"较大" if ec_value > 4 else "中等"}

**改良策略：**

**排水洗盐：**
1. **建设排水系统**：开挖排水沟网
2. **大水洗盐**：充分淋洗表层盐分
3. **暗管排水**：安装暗管系统

**化学改良：**
1. **施用石膏**：2000-3000kg/亩
2. **酸性改良剂**：硫磺粉100-200kg/亩
3. **有机物料**：腐殖酸钠200kg/亩

**生物改良：**
1. **耐盐植物**：种植盐地碱蓬、柽柳等
2. **改良作物**：向日葵、甜菜等耐盐作物
3. **微生物改良**：施用耐盐菌剂

**预期效果：**
经过2-3年系统改良，EC值可降至2.0以下，基本满足常规作物种植要求。"""
        
        return {
            "instruction": instruction,
            "input": input_text,
            "output": output
        }
    
    def generate_organic_qa(self):
        """生成有机农业类问答"""
        instruction = "有机农业土壤管理建议"
        transition_year = random.randint(1, 3)
        area = random.randint(5, 50)
        
        input_text = f"转换期：第{transition_year}年；面积：{area}亩；目标：获得有机认证；要求：不使用化学农药化肥"
        
        output = f"""**有机农业土壤管理方案：**

**转换期管理：**
- 当前阶段：第{transition_year}年转换期
- 认证要求：还需{4-transition_year}年达到认证标准
- 管理目标：建立健康土壤生态系统

**土壤培肥计划：**

**有机质提升：**
1. **有机肥投入**：腐熟农家肥4000-5000kg/亩
2. **绿肥种植**：紫花苜蓿、红花草等
3. **秸秆还田**：作物秸秆全量还田

**生物活性改善：**
1. **微生物菌剂**：施用复合菌剂50kg/亩
2. **生物防治**：引入天敌昆虫
3. **轮作制度**：豆科-禾本科轮作

**病虫害防治（有机方法）：**
1. **物理防治**：防虫网、诱虫灯
2. **生物农药**：BT、阿维菌素等
3. **植物源农药**：除虫菊、苦参等

**认证准备：**
- 建立完整的生产记录
- 定期进行土壤检测
- 准备有机认证材料

**经济效益：**
有机产品售价提高50-100%，扣除投入成本，预计增收30-50%。"""
        
        return {
            "instruction": instruction,
            "input": input_text,
            "output": output
        }
    
    def generate_water_qa(self):
        """生成水分管理类问答"""
        instruction = "农田水分管理指导"
        crop = random.choice(self.crops)
        problem = random.choice(["干旱缺水", "积水涝害", "水分不均"])
        
        input_text = f"作物：{crop}；问题：{problem}；土壤类型：{random.choice(self.soil_types)}；灌溉条件：一般"
        
        output = f"""**{crop}水分管理方案：**

**问题诊断：**
- 作物：{crop}
- 主要问题：{problem}
- 需要系统性水分管理

**管理策略：**

**灌溉制度：**
1. **灌溉时机**：根据土壤墒情和作物需水确定
2. **灌溉量**：每次20-30mm，小水勤浇
3. **灌溉方式**：推荐滴灌或喷灌

**保墒措施：**
1. **覆盖保墒**：地膜覆盖或秸秆覆盖
2. **中耕松土**：及时中耕，减少蒸发
3. **合理密植**：优化群体结构

**排水管理：**
1. **排水沟系**：建立完善的排水网络
2. **起垄栽培**：提高畦面，利于排水
3. **应急排涝**：暴雨后及时排除积水

**技术措施：**
- 安装土壤墒情监测设备
- 建立灌溉预报预警系统
- 推广节水灌溉技术

**预期效果：**
合理的水分管理可提高{crop}产量15-25%，节约用水20-30%。"""
        
        return {
            "instruction": instruction,
            "input": input_text,
            "output": output
        }
    
    def generate_compaction_qa(self):
        """生成土壤板结类问答"""
        instruction = "土壤板结如何处理？"
        years = random.randint(3, 10)
        area = random.randint(10, 100)
        
        input_text = f"农田种植{years}年；土壤板结严重；雨后积水；作物根系浅；面积：{area}亩"
        
        output = f"""**土壤板结综合治理方案：**

**问题分析：**
- 种植年限：{years}年
- 板结程度：严重
- 影响：排水不良，根系发育受阻
- 治理面积：{area}亩

**治理措施：**

**机械改良：**
1. **深松作业**：深度40-50cm，打破犁底层
2. **深翻改土**：秋季深翻，改善土壤结构
3. **分层处理**：表层松土，深层改良

**有机改良：**
1. **大量施用有机肥**：5000-8000kg/亩
2. **秸秆还田**：粉碎后翻压入土
3. **生物菌肥**：增加土壤微生物活性

**生物改良：**
1. **种植绿肥**：深根作物改善土壤
2. **蚯蚓改土**：投放蚯蚓疏松土壤
3. **微生物活化**：施用微生物制剂

**工程措施：**
1. **排水系统**：开挖排水沟
2. **起垄栽培**：改善田面排水
3. **覆盖栽培**：减少土表板结

**实施计划：**
- 第1年：机械改良+大量有机肥
- 第2年：生物改良+维护管理
- 第3年：效果监测+持续改进

**投资预算：**
总投资约{area*300}-{area*500}元，2-3年内可见明显效果。"""
        
        return {
            "instruction": instruction,
            "input": input_text,
            "output": output
        }
    
    def get_suitable_crops(self, soil_type, ph):
        """根据土壤条件获取适宜作物"""
        crops_data = [
            ("玉米", "适应性强，产量潜力大"),
            ("小麦", "适合多种土壤类型"),
            ("大豆", "固氮改良土壤"),
            ("花生", "喜沙质土壤"),
            ("红薯", "耐瘠薄，适应性强"),
            ("马铃薯", "块茎作物，易管理"),
            ("番茄", "经济价值高"),
            ("黄瓜", "设施栽培效益好")
        ]
        
        random.shuffle(crops_data)
        return crops_data
    
    def generate_dataset(self, total_samples=5000):
        """生成完整数据集"""
        dataset = []
        samples_per_type = total_samples // len(self.problem_templates)
        
        for problem_type, generator_func in self.problem_templates.items():
            print(f"正在生成{problem_type}类型数据...")
            for _ in range(samples_per_type):
                try:
                    qa_pair = generator_func()
                    dataset.append(qa_pair)
                except Exception as e:
                    print(f"生成数据时出错: {e}")
                    continue
        
        # 补充剩余数据
        remaining = total_samples - len(dataset)
        for _ in range(remaining):
            generator_func = random.choice(list(self.problem_templates.values()))
            try:
                qa_pair = generator_func()
                dataset.append(qa_pair)
            except Exception as e:
                continue
        
        return dataset

def main():
    """主函数"""
    print("开始生成土壤问诊数据集...")
    
    generator = SoilDiagnosisDataGenerator()
    dataset = generator.generate_dataset(5000)
    
    print(f"成功生成 {len(dataset)} 条数据")
    
    # 保存数据集
    with open('soil_diagnosis_complete.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    print("数据集已保存到 soil_diagnosis_complete.json")
    
    # 生成数据集信息文件
    dataset_info = {
        "soil_diagnosis_dataset": {
            "file_name": "soil_diagnosis_complete.json",
            "formatting": "alpaca",
            "columns": {
                "prompt": "instruction",
                "query": "input",
                "response": "output"
            },
            "num_samples": len(dataset)
        }
    }
    
    with open('dataset_info.json', 'w', encoding='utf-8') as f:
        json.dump(dataset_info, f, ensure_ascii=False, indent=2)
    
    print("数据集信息已保存到 dataset_info.json")
    print("数据集生成完成！")

if __name__ == "__main__":
    main() 