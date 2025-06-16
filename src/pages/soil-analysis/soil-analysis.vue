<script>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import * as echarts from 'echarts';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export default {
  name: 'SoilAnalysisChat',
  setup() {
    // 页面状态和数据
    const sampleData = ref(null);
    const isLoading = ref(true); // 初始加载状态，获取样本数据
    const aiIsTyping = ref(false); // AI是否正在输入

    // 对话消息列表
    const messages = ref([]);
    // 用户当前输入
    const userInput = ref(''); 
    // 聊天记录滚动容器的引用
    const chatMessagesContainer = ref(null);

    // 预设分析话题
    const suggestedTopics = ref([
      { id: 'overall_assessment', label: '土壤综合评估' },
      { id: 'ph_analysis', label: 'pH值分析与建议' },
      { id: 'nitrogen_analysis', label: '氮含量分析与建议' },
      { id: 'phosphorus_analysis', label: '磷含量分析与建议' },
      { id: 'potassium_analysis', label: '钾含量分析与建议' },
      { id: 'organic_analysis', label: '有机质分析与建议' },
      { id: 'suitable_crops', label: '适宜作物推荐' },
      { id: 'improvement_recommendations', label: '综合改进建议' },
    ]);

    onMounted(() => {
      console.log('土壤分析对话页面已挂载');
      uni.$on('soil-sample-data', (data) => {
        console.log('对话页接收到土壤样本数据:', data);
        if (data) {
          sampleData.value = data;
          initializeChat();
        } else {
          // 如果没有数据传入，则使用模拟数据并提示
          addMessageToChat('ai', '未能获取到有效的采样点数据，将使用模拟数据进行演示。');
          generateMockData();
          initializeChat();
        }
        isLoading.value = false;
      });

      // 如果一段时间后仍未收到数据，则主动加载模拟数据
      setTimeout(() => {
        if (!sampleData.value) {
          console.log('超时，使用模拟数据');
          addMessageToChat('ai', '未能获取到有效的采样点数据，将使用模拟数据进行演示。');
          generateMockData();
          initializeChat();
          isLoading.value = false;
        }
      }, 3000); 
    });

    const initializeChat = () => {
      messages.value = []; // 清空旧消息
      let greeting = `你好！我是土壤智能分析助手。已加载采样点 "${sampleData.value.name}" 的数据。`;
      addMessageToChat('ai', greeting);
      addMessageToChat('ai', '请选择您感兴趣的分析话题，或直接向我提问（功能开发中）。', true, suggestedTopics.value);
    };

    const generateMockData = () => {
      sampleData.value = {
        id: 'MOCK001',
        name: '模拟采样点Alpha',
        time: '2023-10-26 10:00',
        region: '虚拟示范区',
        ph: 6.2,
        nitrogen: 75,
        phosphorus: 35,
        potassium: 90,
        organic: 2.1,
        soilType: '沙壤土',
        phEvaluation: '土壤pH值为6.2，属于弱酸性土壤，适合多数作物生长，但对喜碱性作物可能需要适度调整。',
        nitrogenEvaluation: '氮含量为75mg/kg，处于中等水平，能满足一般作物生长需求，但高需氮作物可能需要补充。',
        phosphorusEvaluation: '磷含量为35mg/kg，中等偏低，建议适量补充磷肥，特别是作物苗期和花果期。 ',
        potassiumEvaluation: '钾含量为90mg/kg，处于中等水平，对于需钾量大的作物，后期可能需要追施钾肥。',
        organicEvaluation: '有机质含量为2.1%，属于中等水平，建议通过增施有机肥或秸秆还田来逐步提升。 ',
        soilTypeEvaluation: '土壤类型为沙壤土，该类土壤通气透水性良好，但保肥保水能力相对较弱。'
      };
    };

    const addMessageToChat = (sender, text, isHtml = false, topics = []) => {
      messages.value.push({ 
        id: Date.now() + Math.random(), 
        sender, 
        text, 
        isHtml, 
        topics 
      });
      scrollToBottom();
    };

    const handleTopicSelect = (topic) => {
      console.log('选择的话题:', topic);
      addMessageToChat('user', `我想了解关于"${topic.label}"的信息。`);
      aiIsTyping.value = true;
      // 移除话题按钮
      const lastMessage = messages.value[messages.value.length - 2]; // AI发的上一条带按钮的消息
      if (lastMessage && lastMessage.sender === 'ai' && lastMessage.topics && lastMessage.topics.length > 0) {
        lastMessage.topics = []; 
      }

      setTimeout(() => {
        generateAIResponseForTopic(topic.id);
        aiIsTyping.value = false;
      }, 1000 + Math.random() * 1000);
    };
    
    const handleSendMessage = () => {
      if (!userInput.value.trim()) return;
      addMessageToChat('user', userInput.value);
      const query = userInput.value;
      userInput.value = '';
      aiIsTyping.value = true;
      setTimeout(() => {
        // 简单模拟回复，实际应基于query内容
        addMessageToChat('ai', `关于"${query}"的详细分析功能正在开发中。您可以先选择预设话题了解更多信息。`, true, suggestedTopics.value);
        aiIsTyping.value = false;
      }, 1000);
    };

    const generateAIResponseForTopic = (topicId) => {
      if (!sampleData.value) {
        addMessageToChat('ai', '抱歉，缺少必要的土壤数据，无法进行分析。');
        return;
      }
      const data = sampleData.value;
      let response = '';

      switch (topicId) {
        case 'overall_assessment':
          const score = calculateOverallScore(data);
          const quality = getQualityLevel(score);
          response = `<strong>土壤综合评估</strong> <br>采样点 "${data.name}"：<br>- <strong>综合评分</strong>: ${score}分 (${quality.level})<br>- <strong>评价</strong>: ${quality.description}<br>- <strong>土壤类型</strong>: ${data.soilType} (${data.soilTypeEvaluation || '暂无详细评价'})`;
          break;
        case 'ph_analysis':
          response = `<strong>pH值分析与建议 (${data.ph})</strong><br>${data.phEvaluation || '暂无详细评价'}<br>建议：${getpHRecommendation(data.ph)}`;
          break;
        case 'nitrogen_analysis':
          response = `<strong>氮含量分析与建议 (${data.nitrogen} mg/kg)</strong><br>${data.nitrogenEvaluation || '暂无详细评价'}<br>建议：${getNutrientRecommendation('nitrogen', data.nitrogen)}`;
          break;
        case 'phosphorus_analysis':
          response = `<strong>磷含量分析与建议 (${data.phosphorus} mg/kg)</strong><br>${data.phosphorusEvaluation || '暂无详细评价'}<br>建议：${getNutrientRecommendation('phosphorus', data.phosphorus)}`;
          break;
        case 'potassium_analysis':
          response = `<strong>钾含量分析与建议 (${data.potassium} mg/kg)</strong><br>${data.potassiumEvaluation || '暂无详细评价'}<br>建议：${getNutrientRecommendation('potassium', data.potassium)}`;
          break;
        case 'organic_analysis':
          response = `<strong>有机质分析与建议 (${data.organic}%)</strong><br>${data.organicEvaluation || '暂无详细评价'}<br>建议：${getNutrientRecommendation('organic', data.organic)}`;
          break;
        case 'suitable_crops':
          const crops = generateSuitableCrops(data);
          response = `<strong>适宜作物推荐</strong><br>根据当前土壤数据 (pH: ${data.ph}, 土壤类型: ${data.soilType})，推荐种植以下作物：<br>`;
          crops.forEach(crop => {
            response += `- <strong>${crop.name}</strong>: ${crop.description} (适宜度: ${crop.suitability}%)<br>`;
          });
          if (crops.length === 0) response += '暂无特别推荐的作物，可考虑种植适应性广的本地品种。'
          break;
        case 'improvement_recommendations':
          const recommendations = generateOverallRecommendations(data);
          response = `<strong>综合改进建议</strong><br>`;
          recommendations.forEach(rec => {
            response += `- <strong>${rec.title}</strong>: ${rec.content}<br>`;
          });
          if (recommendations.length === 0) response += '当前土壤状况良好，请继续保持科学管理。'
          break;
        default:
          response = '抱歉，关于这个话题的分析我还在学习中。不如看看其他话题？';
      }
      addMessageToChat('ai', response, true, suggestedTopics.value);
    };

    // --- 以下是辅助分析函数 (大部分可以从旧代码中迁移和调整) ---
    const calculateOverallScore = (data) => {
      let score = 0;
      if (data.ph >= 6.0 && data.ph <= 7.5) score += 25; else if (data.ph >= 5.0 && data.ph < 8.0) score += 15; else score += 5;
      if (data.nitrogen >= 80) score += 15; else if (data.nitrogen >= 50) score += 10; else score += 5;
      if (data.phosphorus >= 40) score += 15; else if (data.phosphorus >= 20) score += 10; else score += 5;
      if (data.potassium >= 100) score += 15; else if (data.potassium >= 60) score += 10; else score += 5;
      if (data.organic >= 2.5) score += 30; else if (data.organic >= 1.5) score += 20; else score += 10;
      return Math.min(100, score); // 确保不超过100分
    };

    const getQualityLevel = (score) => {
      if (score >= 85) return { level: '优质', description: '各项指标均衡，肥力高，非常适合农耕。' };
      if (score >= 70) return { level: '良好', description: '土壤状况良好，适合多数作物，部分指标可优化。' };
      if (score >= 50) return { level: '中等', description: '土壤基本满足作物生长，建议针对性改良。' };
      return { level: '较差', description: '土壤存在明显不足，需大力改良以提高生产力。' };
    };

    const getpHRecommendation = (ph) => {
      if (ph < 5.5) return '土壤过酸，建议施用石灰或草木灰等碱性改良剂进行调节。';
      if (ph > 7.8) return '土壤偏碱，可考虑施用硫磺粉、石膏或酸性有机肥进行改良。';
      if (ph < 6.0) return '土壤略酸，多数作物可适应，若种植喜中性作物可微调。';
      if (ph > 7.5) return '土壤略碱，部分敏感作物可能受影响，可适量补充有机质改善。';
      return 'pH值适宜，请保持良好耕作习惯。';
    };

    const getNutrientRecommendation = (nutrient, value) => {
      switch (nutrient) {
        case 'nitrogen':
          if (value < 50) return '氮含量偏低，显著影响作物生长，应及时补充速效氮肥，并配合有机肥。 ';
          if (value > 120) return '氮含量过高，可能导致作物徒长、病害加重，应控制氮肥施用，增施磷钾肥平衡。 ';
          return '氮含量适中，请根据作物品种和生长期合理施用氮肥。';
        case 'phosphorus':
          if (value < 20) return '磷含量严重不足，影响作物根系发育和开花结果，需重点补充磷肥，如过磷酸钙。 ';
          if (value > 60) return '磷含量偏高，注意过量施磷可能影响微量元素吸收，后续可酌情减量。 ';
          return '磷含量适中，常规施肥即可满足需求。';
        case 'potassium':
          if (value < 60) return '钾含量不足，影响作物抗逆性和品质，应增施钾肥，如硫酸钾或草木灰。 ';
          if (value > 150) return '钾含量过高，可能影响作物对镁、钙的吸收，应避免过量施用钾肥。 ';
          return '钾含量适中，能满足多数作物需求。';
        case 'organic':
          if (value < 1.5) return '有机质含量低，土壤肥力差，保水保肥能力弱，急需大量补充有机物料，如堆肥、厩肥、绿肥等。 ';
          if (value > 3.5) return '有机质含量非常丰富，土壤肥沃，是理想状态。 ';
          return '有机质含量中等，建议继续培肥土壤，逐年提高有机质水平。';
      }
      return '暂无特定建议。';
    };

    const generateSuitableCrops = (data) => {
      const crops = [];
      if (data.ph >= 6.0 && data.ph <= 7.0) {
        crops.push({ name: '玉米', description: '中性土壤表现良好', suitability: 90 });
        crops.push({ name: '小麦', description: 'pH适应范围广', suitability: 85 });
        if (data.organic > 2.0) crops.push({ name: '蔬菜 (如白菜、甘蓝)', description: '喜肥沃中性土壤', suitability: 88 });
      }
      if (data.ph < 6.0) {
        crops.push({ name: '马铃薯', description: '喜微酸性土壤', suitability: 92 });
        crops.push({ name: '茶树', description: '典型的喜酸作物', suitability: 80 });
      }
      if (data.ph > 7.5 && data.soilType.includes('壤')) { // 偏碱性壤土
         crops.push({ name: '高粱', description: '耐碱性较好', suitability: 85 });
         crops.push({ name: '向日葵', description: '对土壤要求不严，一定程度耐碱', suitability: 82 });
      }
      if (data.nitrogen > 80 && data.potassium > 100 && data.organic > 2.0) {
         crops.push({ name: '番茄', description: '需肥量大，当前养分较充足', suitability: 90 });
      }
      if (crops.length === 0) crops.push({name: '本地常见作物', description: '可参考当地种植习惯，并根据具体养分进行调整。' ,suitability: 70})
      return crops.sort((a,b) => b.suitability - a.suitability).slice(0,3); // 返回最合适的3个
    };
    
    const generateOverallRecommendations = (data) => {
      const recs = [];
      recs.push({ title: 'pH值调理', content: getpHRecommendation(data.ph) });
      if (data.organic < 2.0) recs.push({ title: '提升有机质', content: '建议增施腐熟有机肥，如农家肥、商品有机肥，或种植绿肥后翻压还田，以改善土壤结构，提高保水保肥能力。' });
      if (data.nitrogen < 60 || data.phosphorus < 30 || data.potassium < 80) recs.push({ title: '均衡养分', content: '根据测土结果，针对性补充所缺的氮、磷、钾元素，做到平衡施肥，避免单一元素过量或不足。' });
      recs.push({ title: '科学灌溉', content: `根据土壤类型（${data.soilType}）和作物需求合理灌溉，避免大水漫灌，提倡节水灌溉技术。` });
      recs.push({ title: '轮作换茬', content: '避免长期连作同一种或同科作物，实行合理的轮作制度，有助于减轻土传病害，均衡利用土壤养分。'});
      if(recs.length === 0) recs.push({title: '保持良好管理', content: '当前土壤各项指标较为理想，请继续保持科学的田间管理措施。'})
      return recs.slice(0,4);
    };

    const scrollToBottom = () => {
      nextTick(() => {
        const container = chatMessagesContainer.value;
        if (container && container.$el && typeof container.$el.scrollTop !== 'undefined') {
          container.$el.scrollTop = container.$el.scrollHeight;
        } else if (container && typeof container.scrollTop !== 'undefined'){
            container.scrollTop = container.scrollHeight; // Fallback for non-Vue component ref
        }
      });
    };

    const generatePdfReport = async () => {
      if (!sampleData.value) {
        uni.showToast({
          title: '缺少土壤数据，无法生成报告',
          icon: 'none'
        });
        return;
      }

      uni.showLoading({
        title: '正在生成PDF报告...'
      });

      const reportElement = chatMessagesContainer.value;

      if (!reportElement) {
        uni.hideLoading();
        uni.showToast({
          title: '无法找到报告内容元素',
          icon: 'none'
        });
        return;
      }
      
      // Attempt to get the underlying DOM element if reportElement is a Vue component instance
      const elementToCapture = reportElement.$el || reportElement;

      try {
        const canvas = await html2canvas(elementToCapture, {
          useCORS: true,
          backgroundColor: '#FFFFFF', // Ensure a white background for the PDF
          scrollY: -window.scrollY, // Try to capture from the top
          // Adjusting scale might improve quality, but also increases size/processing time
          // scale: 2, 
          // Tweak settings if content is cut off
          // windowWidth: elementToCapture.scrollWidth,
          // windowHeight: elementToCapture.scrollHeight,
        });

        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF({
          orientation: 'p', // portrait
          unit: 'pt', // points
          format: 'a4' // A4 page size
        });

        const imgProps = pdf.getImageProperties(imgData);
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = pdf.internal.pageSize.getHeight();
        const imgWidth = imgProps.width;
        const imgHeight = imgProps.height;

        // Calculate the ratio to fit the image within the PDF page
        const ratio = Math.min(pdfWidth / imgWidth, pdfHeight / imgHeight);
        
        const newImgWidth = imgWidth * ratio;
        const newImgHeight = imgHeight * ratio;

        // Center the image on the page (optional)
        const xOffset = (pdfWidth - newImgWidth) / 2;
        const yOffset = (pdfHeight - newImgHeight) / 2;


        // Handle cases where the content is taller than one page
        let position = 0;
        const pageHeight = pdf.internal.pageSize.getHeight() - 20; // Page height with some margin

        if (newImgHeight <= pageHeight) {
            pdf.addImage(imgData, 'PNG', xOffset, yOffset, newImgWidth, newImgHeight);
        } else {
            let M_WIDTH = pdf.internal.pageSize.getWidth();
            let M_HEIGHT = pdf.internal.pageSize.getHeight();
            let currentHeight = 0;
            while(currentHeight < imgHeight) {
                let H = M_HEIGHT;
                if (currentHeight + H > imgHeight) {
                    H = imgHeight - currentHeight;
                }
                const tempCanvas = document.createElement('canvas');
                tempCanvas.width = imgWidth;
                tempCanvas.height = H;
                const ctx = tempCanvas.getContext('2d');
                ctx.drawImage(canvas, 0, currentHeight, imgWidth, H, 0, 0, imgWidth, H);
                const pageData = tempCanvas.toDataURL('image/png', 1.0);
                
                const pageWidth = pdf.internal.pageSize.getWidth();
                const pageImageHeight = H * (pageWidth / imgWidth);


                if (currentHeight > 0) {
                    pdf.addPage();
                }
                pdf.addImage(pageData, 'PNG', 0, 0, pageWidth, pageImageHeight);
                currentHeight += H;
            }
        }
        

        pdf.save(`${sampleData.value.name}_土壤分析报告.pdf`);
        uni.hideLoading();
        uni.showToast({
          title: '报告已下载',
          icon: 'success'
        });

      } catch (error) {
        uni.hideLoading();
        console.error('PDF生成失败:', error);
        uni.showToast({
          title: '报告生成失败: ' + error.message,
          icon: 'none',
          duration: 3000
        });
      }
    };

    onBeforeUnmount(() => {
      uni.$off('soil-sample-data');
    });

    return {
      sampleData,
      isLoading,
      aiIsTyping,
      messages,
      userInput,
      suggestedTopics,
      handleTopicSelect,
      handleSendMessage,
      chatMessagesContainer,
      calculateOverallScore,
      getQualityLevel,
      getpHRecommendation,
      getNutrientRecommendation,
      generateSuitableCrops,
      generateOverallRecommendations,
      goBack: () => { uni.navigateBack(); },
      generatePdfReport
    };
  }
};
</script>

<template>
  <view class="chat-page-container">
    <!-- 页面头部，显示采样点名称和返回按钮 -->
    <view class="chat-header">
      <view class="back-button" @click="goBack">
        <text class="icon">‹</text>
        <text>返回</text>
      </view>
      <text class="sample-name">{{ sampleData ? sampleData.name : '加载中...' }} 土壤分析</text>
      <view class="header-actions">
        <button class="pdf-button" @click="generatePdfReport">生成PDF报告</button>
      </view>
    </view>

    <!-- 加载指示器 -->
    <view class="loading-indicator" v-if="isLoading">
      <view class="spinner"></view>
      <text>正在加载土壤数据...</text>
    </view>

    <!-- 聊天消息区域 -->
    <scroll-view 
      scroll-y 
      class="chat-messages-container" 
      ref="chatMessagesContainer"
      :scroll-into-view="`msg-${messages.length - 1}`"
      scroll-with-animation
    >
      <view v-for="(message, index) in messages" :key="message.id" :id="`msg-${index}`" 
            :class="['message-bubble', message.sender === 'user' ? 'user-bubble' : 'ai-bubble']">
        
        <view v-if="message.sender === 'ai'" class="avatar ai-avatar">AI</view>
        
        <view class="message-content">
          <rich-text v-if="message.isHtml" :nodes="message.text"></rich-text>
          <text v-else>{{ message.text }}</text>

          <!-- AI消息中的建议话题按钮 -->
          <view v-if="message.sender === 'ai' && message.topics && message.topics.length > 0" class="suggested-topics">
            <button 
              v-for="topic in message.topics" 
              :key="topic.id" 
              class="topic-button"
              @click="handleTopicSelect(topic)">
              {{ topic.label }}
            </button>
          </view>
        </view>
        
        <view v-if="message.sender === 'user'" class="avatar user-avatar">我</view>
      </view>
      
      <!-- AI正在输入提示 -->
      <view v-if="aiIsTyping" class="message-bubble ai-bubble typing-indicator">
        <view class="avatar ai-avatar">AI</view>
        <view class="message-content">
          <view class="typing-dots">
            <text class="dot">.</text>
            <text class="dot">.</text>
            <text class="dot">.</text>
          </view>
        </view>
      </view>
    </scroll-view>

    <!-- 输入区域 -->
    <view class="chat-input-area">
      <input 
        type="text" 
        v-model="userInput" 
        placeholder="输入您的问题... (开发中)"
        class="input-field"
        @confirm="handleSendMessage"
        :disabled="true" 
      />
      <button @click="handleSendMessage" class="send-button" :disabled="true">发送</button>
    </view>
  </view>
</template>

<style>
.chat-page-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f4f7f9; /* 淡雅的背景色 */
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 15px;
  background-color: #ffffff;
  border-bottom: 1px solid #e0e0e0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.back-button {
  display: flex;
  align-items: center;
  color: #4d7bce;
  font-size: 15px;
  cursor: pointer;
  padding: 5px;
}

.back-button .icon {
  font-size: 22px;
  margin-right: 3px;
  font-weight: bold;
}

.sample-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  text-align: center;
  flex-grow: 1;
}
.header-placeholder{
  width: 50px; /* 与返回按钮大致宽度相同以平衡标题 */
}

.header-actions {
  display: flex;
  align-items: center;
}

.pdf-button {
  background-color: #4d7bce;
  color: white;
  border: none;
  padding: 0 18px;
  height: 40px;
  border-radius: 20px; /* 发送按钮圆角 */
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 30px;
  color: #666;
  font-size: 16px;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #f0f0f0;
  border-top-color: #4d7bce;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.chat-messages-container {
  flex-grow: 1;
  padding: 15px;
  overflow-y: auto;
}

.message-bubble {
  display: flex;
  margin-bottom: 15px;
  max-width: 85%;
  align-items: flex-end; /* 确保头像和气泡底部对齐 */
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 14px;
  flex-shrink: 0;
}

.ai-avatar {
  background-color: #4d7bce; /* AI头像颜色 */
  margin-right: 10px;
}

.user-avatar {
  background-color: #42b983; /* 用户头像颜色 */
  margin-left: 10px;
}

.message-content {
  padding: 10px 15px;
  border-radius: 12px;
  line-height: 1.6;
  font-size: 15px;
  word-wrap: break-word;
  overflow-wrap: break-word; 
}

.ai-bubble .message-content {
  background-color: #ffffff; /* AI消息气泡背景色 */
  color: #333;
  border: 1px solid #e8e8e8;
  border-top-left-radius: 0; /* AI气泡尖角效果 */
}

.user-bubble {
  margin-left: auto; /* 用户消息靠右 */
  flex-direction: row-reverse; /* 用户头像在右侧 */
}

.user-bubble .message-content {
  background-color: #4d7bce; /* 用户消息气泡背景色 */
  color: white;
  border-top-right-radius: 0; /* 用户气泡尖角效果 */
}

.suggested-topics {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.topic-button {
  background-color: #eef4ff; /* 按钮背景色 */
  color: #4d7bce; /* 按钮文字颜色 */
  border: 1px solid #cddcff; /* 按钮边框颜色 */
  padding: 6px 12px;
  border-radius: 15px; /* 圆角按钮 */
  font-size: 13px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.topic-button:hover {
  background-color: #dbe8ff;
}

.typing-indicator .message-content {
  padding: 10px 15px;
}

.typing-dots {
  display: flex;
  align-items: center;
}

.typing-dots .dot {
  width: 6px;
  height: 6px;
  background-color: #a0b4d7; /* 打字点的颜色 */
  border-radius: 50%;
  margin: 0 2px;
  animation: typingAnimation 1.4s infinite ease-in-out both;
}

.typing-dots .dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dots .dot:nth-child(2) { animation-delay: -0.16s; }
.typing-dots .dot:nth-child(3) { animation-delay: 0s; }

@keyframes typingAnimation {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1.0); }
}

.chat-input-area {
  display: flex;
  padding: 10px 15px;
  background-color: #ffffff;
  border-top: 1px solid #e0e0e0;
  align-items: center;
}

.input-field {
  flex-grow: 1;
  height: 40px;
  padding: 0 12px;
  border: 1px solid #dcdfe6;
  border-radius: 20px; /* 输入框圆角 */
  font-size: 15px;
  margin-right: 10px;
}

.input-field:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.send-button {
  background-color: #4d7bce;
  color: white;
  border: none;
  padding: 0 18px;
  height: 40px;
  border-radius: 20px; /* 发送按钮圆角 */
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.send-button:disabled {
  background-color: #a0b4d7;
  cursor: not-allowed;
}

/* rich-text 内部标题等简单样式 */
.ai-bubble h1, .ai-bubble h2, .ai-bubble h3 {
  font-weight: bold;
  margin-top: 8px;
  margin-bottom: 4px;
}
.ai-bubble h1 { font-size: 1.2em; }
.ai-bubble h2 { font-size: 1.1em; }
.ai-bubble h3 { font-size: 1.0em; }
.ai-bubble strong { font-weight: bold; }
.ai-bubble em { font-style: italic; }

</style> 