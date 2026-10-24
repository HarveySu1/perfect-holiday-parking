window.slideDataMap.set(4, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
    <div class="w-[1350px] h-[720px] mx-auto my-[45px] flex flex-col">
      <div class="mb-6">
        <h2 class="text-4xl font-light text-gray-900 mb-3">不另起炉灶，在"设为终点"前插一步</h2>
        <p class="text-lg text-gray-400">三个增量，全部复用主办方已有能力</p>
      </div>
      <div class="grid grid-cols-3 gap-4 mb-6">
        <div class="rounded-lg p-5" style="background:#F0F6FF">
          <div class="text-2xl font-light mb-2" style="color:#1A6DFF">①</div>
          <h3 class="text-base font-semibold text-gray-800 mb-2">目的地选车位</h3>
          <p class="text-xs text-gray-500 leading-relaxed">输入"去哪"→综合步行+楼层+电梯口推荐最近车位</p>
          <p class="text-xs mt-2" style="color:#1A6DFF">复用：车位真值、地图、电梯厅标注</p>
        </div>
        <div class="rounded-lg p-5" style="background:#F5F0FF">
          <div class="text-2xl font-light mb-2" style="color:#7B61FF">②</div>
          <h3 class="text-base font-semibold text-gray-800 mb-2">电梯厅选梯</h3>
          <p class="text-xs text-gray-500 leading-relaxed">把1-6号电梯厅建成多层图上的边，算法自己选梯</p>
          <p class="text-xs mt-2" style="color:#7B61FF">复用：电梯厅位置数据</p>
        </div>
        <div class="rounded-lg p-5" style="background:#F0FAF5">
          <div class="text-2xl font-light mb-2" style="color:#0FA958">③</div>
          <h3 class="text-base font-semibold text-gray-800 mb-2">充电桩导航</h3>
          <p class="text-xs text-gray-500 leading-relaxed">查空闲桩并导航，状态三级来源+置信度衰减</p>
          <p class="text-xs mt-2" style="color:#0FA958">复用：车位-桩绑定、已有导航</p>
        </div>
      </div>
      <div class="grid grid-cols-4 gap-3 mb-4">
        <div class="flex items-center gap-2 px-3 py-2 rounded bg-gray-50">
          <span class="text-xs text-gray-400">不做</span>
          <span class="text-xs text-gray-700">重建地图</span>
        </div>
        <div class="flex items-center gap-2 px-3 py-2 rounded bg-gray-50">
          <span class="text-xs text-gray-400">不做</span>
          <span class="text-xs text-gray-700">重写导航</span>
        </div>
        <div class="flex items-center gap-2 px-3 py-2 rounded bg-gray-50">
          <span class="text-xs text-gray-400">不做</span>
          <span class="text-xs text-gray-700">新增硬件</span>
        </div>
        <div class="flex items-center gap-2 px-3 py-2 rounded bg-gray-50">
          <span class="text-xs text-gray-400">不做</span>
          <span class="text-xs text-gray-700">另做小程序</span>
        </div>
      </div>
      <div class="text-center mt-2">
        <p class="text-gray-400 text-sm">最好的改进，是让已有的能力真正被用起来</p>
      </div>
    </div>
  </div>
`);
