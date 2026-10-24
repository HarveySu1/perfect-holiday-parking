window.slideDataMap.set(8, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
    <div class="w-[1350px] h-[720px] mx-auto my-[45px] flex flex-col justify-center">
      <div class="mb-8">
        <h2 class="text-4xl font-light text-gray-900 mb-3">架构上就绕开了车牌敏感信息</h2>
        <p class="text-lg text-gray-400">最核心的创新功能，恰好是隐私风险最低的那个</p>
      </div>
      <div class="grid grid-cols-3 gap-6 mb-8">
        <div class="rounded-lg p-6 border border-gray-200">
          <div class="flex items-center gap-3 mb-3">
            <div class="w-8 h-8 rounded-full flex items-center justify-center" style="background:#FFF3E2">
              <span class="text-sm">⚠</span>
            </div>
            <h3 class="text-sm font-semibold text-gray-800">订阅消息限制</h3>
          </div>
          <p class="text-xs text-gray-500 leading-relaxed">不做自动定时推送；停车时主动授权一次下发凭证，返程前用户主动生成路线</p>
        </div>
        <div class="rounded-lg p-6 border-2" style="border-color:#1A6DFF">
          <div class="flex items-center gap-3 mb-3">
            <div class="w-8 h-8 rounded-full flex items-center justify-center" style="background:#F0F6FF">
              <span class="text-sm">🔒</span>
            </div>
            <h3 class="text-sm font-semibold text-gray-800">车牌敏感信息</h3>
          </div>
          <p class="text-xs text-gray-500 leading-relaxed">主链路以会员码+车位码绑定；功能①完整发生在停车前，<span class="font-medium" style="color:#1A6DFF">不需要车牌</span></p>
        </div>
        <div class="rounded-lg p-6 border border-gray-200">
          <div class="flex items-center gap-3 mb-3">
            <div class="w-8 h-8 rounded-full flex items-center justify-center" style="background:#F0FAF5">
              <span class="text-sm">📶</span>
            </div>
            <h3 class="text-sm font-semibold text-gray-800">地库弱网</h3>
          </div>
          <p class="text-xs text-gray-500 leading-relaxed">数据随包内置，路径本地计算；空桩状态读本地缓存并显式标注时效</p>
        </div>
      </div>
      <div class="mx-auto max-w-[1100px] px-8 py-5 rounded-lg" style="background:#F0F6FF">
        <p class="text-center text-gray-600 text-sm leading-relaxed">功能①（目的地选车位）完整发生在用户进车库之前——用户还没停车、还没输任何车牌，就已经完成了推荐。<br><span class="font-semibold" style="color:#1A6DFF">这不是回避合规，是从架构上绕开了它。</span></p>
      </div>
    </div>
  </div>
`);
