window.slideDataMap.set(5, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
    <div class="w-[1350px] h-[720px] mx-auto my-[45px] flex flex-col justify-center">
      <div class="text-center mb-8">
        <h2 class="text-4xl font-light text-gray-900 mb-3">AI用在该用的层，其余刻意不用</h2>
        <p class="text-lg text-gray-400">实时决策走确定性算法——是工程判断，不是能力不足</p>
      </div>
      <div class="flex items-center justify-center gap-4 mb-8">
        <div class="px-4 py-2 rounded-full text-sm text-white" style="background:#1A6DFF">说一句话</div>
        <div class="text-gray-300">→</div>
        <div class="px-4 py-2 rounded-full text-sm text-white" style="background:#7B61FF">AI解析</div>
        <div class="text-gray-300">→</div>
        <div class="px-4 py-2 rounded-full text-sm text-white" style="background:#0FA958">推荐车位</div>
      </div>
      <div class="grid grid-cols-3 gap-6">
        <div class="text-center px-6 py-8 rounded-lg" style="background:#F0F6FF">
          <div class="w-12 h-12 mx-auto mb-4 rounded-full flex items-center justify-center" style="background:#1A6DFF">
            <span class="text-white text-xl">入口</span>
          </div>
          <h3 class="text-base font-semibold text-gray-800 mb-2">LLM意图解析</h3>
          <p class="text-xs text-gray-500 leading-relaxed">"找个离海底捞近、能充电、婴儿车能走的车位"→结构化约束→交推荐引擎执行</p>
        </div>
        <div class="text-center px-6 py-8 rounded-lg" style="background:#F5F0FF">
          <div class="w-12 h-12 mx-auto mb-4 rounded-full flex items-center justify-center" style="background:#7B61FF">
            <span class="text-white text-xl">兜底</span>
          </div>
          <h3 class="text-base font-semibold text-gray-800 mb-2">多模态OCR</h3>
          <p class="text-xs text-gray-500 leading-relaxed">拍停车小票/订单照片→结构化入库→车位绑定兜底</p>
        </div>
        <div class="text-center px-6 py-8 rounded-lg" style="background:#F0FAF5">
          <div class="w-12 h-12 mx-auto mb-4 rounded-full flex items-center justify-center" style="background:#0FA958">
            <span class="text-white text-xl">输出</span>
          </div>
          <h3 class="text-base font-semibold text-gray-800 mb-2">生成式解释</h3>
          <p class="text-xs text-gray-500 leading-relaxed">把推荐结果翻译成"为什么是这个车位"</p>
        </div>
      </div>
      <div class="mt-8 mx-auto max-w-[1100px] px-8 py-4 rounded-lg" style="background:#F8F9FA">
        <p class="text-center text-gray-500 text-sm leading-relaxed">停车链路对时延、可解释、可离线有硬要求，因此实时决策使用确定性算法；大模型只在"理解人话、解释理由、兜底录入"三层发挥作用。<span class="font-semibold text-gray-700">主动把AI约束在合适的层，是工程成熟度的体现，不是能力不足。</span></p>
      </div>
    </div>
  </div>
`);
