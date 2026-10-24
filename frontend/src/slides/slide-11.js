window.slideDataMap.set(11, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
    <div class="w-[1350px] h-[720px] mx-auto my-[45px] flex">
      <div class="w-2" style="background:#7B61FF"></div>
      <div class="flex-1 px-16 flex flex-col justify-center">
        <h2 class="text-4xl font-light text-gray-900 mb-2">技术架构与降级链</h2>
        <p class="text-sm text-gray-400 mb-8">备份页 · 被问"技术深度"时翻</p>
        <div class="mb-6 px-6 py-5 rounded-lg" style="background:#F8F9FA">
          <p class="text-xs text-gray-600 leading-relaxed mb-2">主办方已有停车小程序 → 只读 → <span class="font-semibold" style="color:#7B61FF">车记得决策服务层</span>（推荐引擎 / 竖向路径图 / 状态聚合器）→ 复用 → 已有地图/导航/车位真值（不改动）</p>
          <p class="text-xs text-gray-400 mt-2">部署形态：云函数挂载到已有小程序，不新增App、不新增硬件</p>
        </div>
        <div class="mb-6">
          <p class="text-xs font-semibold text-gray-700 mb-3">三张新建主数据（静态、可内置到小程序包，兼顾弱网）</p>
          <div class="space-y-2">
            <p class="text-xs text-gray-500">• POI主数据：商户名 / 楼层 / 入口 / 所属区</p>
            <p class="text-xs text-gray-500">• 竖向交通主数据：电梯编号 / 停靠层 / 位置（大部分已有，只需补停靠层）</p>
            <p class="text-xs text-gray-500">• 车位-桩绑定</p>
          </div>
        </div>
        <div>
          <p class="text-xs font-semibold text-gray-700 mb-3">降级链（每个功能都有兜底）</p>
          <div class="space-y-2">
            <p class="text-xs text-gray-500">• 功能①：同场同层近区 → 半径+1区 → 其他层 → 跨场 → 全满提示"到站前锁位"</p>
            <p class="text-xs text-gray-500">• 功能②：竖向建图来不及 → 分段编排（层内A* → 换乘段 → 层内A*），当天可用</p>
            <p class="text-xs text-gray-500">• 功能③：主办方接口缺 → 三级来源 + 置信度衰减，不伪造状态</p>
          </div>
        </div>
      </div>
    </div>
  </div>
`);
