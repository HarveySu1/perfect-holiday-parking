window.slideDataMap.set(6, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
    <div class="w-[1350px] h-[720px] mx-auto my-[45px] flex flex-col justify-center">
      <div class="text-center mb-8">
        <h2 class="text-4xl font-light text-gray-900 mb-3">可演的AI入口：说一句话，得到一个车位</h2>
        <p class="text-lg text-gray-400">30秒动线，浏览器内现场可演</p>
      </div>
      <div class="flex items-center justify-between gap-4 mb-8">
        <div class="flex-1 text-center px-4 py-6 rounded-lg border border-gray-200">
          <div class="text-2xl font-light text-gray-300 mb-2">01</div>
          <h3 class="text-sm font-semibold text-gray-800 mb-1">用户输入</h3>
          <p class="text-xs text-gray-500">"去海底捞，要充电"</p>
        </div>
        <div class="text-gray-300 text-xl">→</div>
        <div class="flex-1 text-center px-4 py-6 rounded-lg border border-gray-200">
          <div class="text-2xl font-light text-gray-300 mb-2">02</div>
          <h3 class="text-sm font-semibold text-gray-800 mb-1">AI解析</h3>
          <p class="text-xs text-gray-500">目的地=海底捞<br>需充电桩</p>
        </div>
        <div class="text-gray-300 text-xl">→</div>
        <div class="flex-1 text-center px-4 py-6 rounded-lg border-2" style="border-color:#7B61FF">
          <div class="text-2xl font-light mb-2" style="color:#7B61FF">03</div>
          <h3 class="text-sm font-semibold text-gray-800 mb-1">推荐车位</h3>
          <p class="text-xs text-gray-500">车位卡片+推荐理由</p>
          <p class="text-xs mt-1 font-medium" style="color:#7B61FF">AI约束已应用</p>
        </div>
        <div class="text-gray-300 text-xl">→</div>
        <div class="flex-1 text-center px-4 py-6 rounded-lg border border-gray-200">
          <div class="text-2xl font-light text-gray-300 mb-2">04</div>
          <h3 class="text-sm font-semibold text-gray-800 mb-1">导航复用</h3>
          <p class="text-xs text-gray-500">点"导航到此车位"<br>复用已有模拟导航</p>
        </div>
      </div>
      <div class="mx-auto max-w-[1000px] px-6 py-3 rounded" style="background:#FFF8E8">
        <p class="text-center text-xs text-gray-500 leading-relaxed">⚠️ 演示用：当前AI解析为关键词模拟，真实链路接入大模型API；演示车位数、桩数为模拟数据，非实测</p>
      </div>
    </div>
  </div>
`);
