# Chapters: 车记得·复赛PPT

## Page 1: 封面
- **Page Type**: Cover
- **Page Title**: 车记得
- **Page Subtitle**: 给完美金鹰·假日商圈的停车系统，补一层"决策服务"
- **Selected Template**: (Phase 6填)

- **Content Structure**:
  - 主标题：车记得
  - 副标题：给完美金鹰·假日商圈的停车系统，补一层"决策服务"
  - Slogan：让已有的能力真正被用起来，而不是再盖一栋楼
  - 页脚：赛道二 · 商圈服务与用户体验 | 完美金鹰·假日商圈AI大赛 | 复赛提交 2026-10-15

- **Content Density**: Light
- **Narrative Role**: 开场定调，一句话立住项目定位
- **Image Requirements**: 无
- **Page Weight**: Core page

## Page 2: 痛点
- **Page Type**: Content
- **Page Title**: 地下车库里，用户要做三个没有依据的决策
- **Page Subtitle**: 真正的痛点不是"找回车难"，而是停车前后那几秒里没人替用户算
- **Selected Template**: (Phase 6填)

- **Content Structure**: Problem/Solution
  - 核心问题：地库里三个决策全靠用户自己算
  - 三个决策无解表：
    - 决策1：停哪个车位 → 自己切楼层看电梯算距离 → 车位空着但不是"好用"的车位
    - 决策2：走哪个电梯 → 赌哪个近哪个不挤 → 高峰候梯5分钟以上是常态
    - 决策3：哪个桩空着 → 开到某层发现被占再找 → 每发现"被占"就是一次无效绕行
  - 共性结论：三段判断都发生在地库入口到车位之间——信号差、时间紧、发生在最不该判断的时刻

- **Content Density**: Medium
- **Narrative Role**: 建立"值得做"的认知，不堆宏观数字
- **Image Requirements**: 无
- **Page Weight**: Core page

## Page 3: 实地证据
- **Page Type**: Content
- **Page Title**: 连行业标杆也没做这件事
- **Page Subtitle**: 我们去了深圳三家头部停车场实地体验，三家无一例外
- **Selected Template**: (Phase 6填)

- **Content Structure**: Case Study
  - 三案例对比：
    - 前海万象汇（华润）：有AR寻车导航、楼层平面、扶梯距离；没按目的地选车位
    - 前海卓越中心：有输入车牌缴费仅此而已；没车位地图导航找店充电
    - 万象天地（华润·标杆）：有剩余车位实时、车牌自动识别、店铺/电梯/公共设施位置、2D模拟导航；没"去我的目的地该停哪个车位"
  - 结论：全行业把智能都花在"找回车"，没人做"停车前选车位"——包括数据完备度最高的万象天地（基于深圳三场实地调研，2026-10-14）

- **Content Density**: Medium
- **Narrative Role**: 用实地证据同时立"真实问题"和"创新空间"
- **Image Requirements**: 三张截图横向排列（前海万象汇AR导航页/前海卓越缴费页/万象天地模拟导航页），来源assets/research-sz-20261014/
- **Page Weight**: Core page

## Page 4: 方案定位
- **Page Type**: Content
- **Page Title**: 不另起炉灶，只在"设为终点"前插一步
- **Page Subtitle**: 三个增量，全部复用主办方已有能力
- **Selected Template**: (Phase 6填)

- **Content Structure**: Concept
  - 三增量表：
    - ①目的地选车位：输入"去哪"→综合步行+楼层+电梯口推荐最近车位 | 复用已有车位真值、地图、电梯厅标注
    - ②电梯厅选梯：把已标注1-6号电梯厅建成多层图上的边，让算法自己选梯 | 复用已有电梯厅位置数据
    - ③充电桩导航：查空闲桩并导航，状态三级来源+置信度衰减 | 复用已有车位-桩绑定、已有导航
  - 边界（不做什么）：
    - 不重建2D/3D地图：已有精度足够
    - 不重写导航引擎："设为终点→模拟导航"链路直接复用
    - 不新增硬件：零传感器
    - 不另做小程序：云函数挂载到已有小程序
  - 一句话：最好的改进，是让已有的能力真正被用起来

- **Content Density**: Heavy
- **Narrative Role**: 立"怎么做"认知，三功能合并一页讲清
- **Image Requirements**: 无
- **Page Weight**: Core page

## Page 5: AI主张
- **Page Type**: Content
- **Page Title**: AI用在该用的层，其余刻意不用
- **Page Subtitle**: 实时决策走确定性算法——是工程判断，不是能力不足
- **Selected Template**: (Phase 6填)

- **Content Structure**: Argument
  - 核心主张：AI用在三层，其余刻意不用
  - 三层用点表：
    - 入口层·LLM意图解析："找个离海底捞近、能充电、婴儿车能走的车位"→结构化约束→交推荐引擎执行
    - 兜底层·多模态OCR：拍停车小票/订单照片→结构化入库→车位绑定兜底
    - 输出层·生成式解释：把推荐结果翻译成"为什么是这个车位"
  - 圆场口径（原话）：停车链路对时延、可解释、可离线有硬要求，因此实时决策使用确定性算法；大模型只在"理解人话、解释理由、兜底录入"三层发挥作用。主动把AI约束在合适的层，是工程成熟度的体现，不是能力不足。

- **Content Density**: Medium
- **Narrative Role**: 核心——正面回应"AI实际应用"审核维度
- **Image Requirements**: 无
- **Page Weight**: Core page

## Page 6: 完成度
- **Page Type**: Content
- **Page Title**: 可演的AI入口：说一句话，得到一个车位
- **Page Subtitle**: 30秒动线，浏览器内现场可演
- **Selected Template**: (Phase 6填)

- **Content Structure**: Process
  - 30秒动线（4步）：
    - 步骤1：用户输入"去海底捞，要充电"
    - 步骤2：AI识别意图与约束（目的地=海底捞、需充电桩）
    - 步骤3：调用推荐引擎→输出车位卡片+推荐理由+"AI约束已应用：已筛新能源车位"
    - 步骤4：用户点"导航到此车位"复用已有模拟导航
  - demo三连截图描述：首页AI入口卡 / AI解析弹窗三步流水线 / 推荐卡
  - 诚实标注：演示用，当前AI解析为关键词模拟，真实链路接入大模型API；演示车位数桩数为模拟数据非实测

- **Content Density**: Medium
- **Narrative Role**: 回应"完成度"维度——别让评委觉得只是纸面方案
- **Image Requirements**: 无（用文字流程图+卡片样式呈现动线）
- **Page Weight**: Core page

## Page 7: 落地路径
- **Page Type**: Content
- **Page Title**: 先在石岐万象汇单场跑通，再走向商圈级
- **Page Subtitle**: 一期零硬件、零系统改造，可灰度、可观测、可回退
- **Selected Template**: (Phase 6填)

- **Content Structure**: Trend
  - 三阶段：
    - 一期·单场验证：复选至决赛 | 石岐万象汇单场 | 三功能跑通采集真实使用数据
    - 二期·能力沉淀：决赛后1-3月 | 同品牌多场 | 主数据标准化引擎配置化，新场接入只需导表
    - 三期·商圈联动：3-6月 | 假日广场金鹰广场等 | 跨场目的地推荐跨场路径编排
  - 三特性：
    - 可灰度：先开放单楼层+部分商户POI，再扩全场，不影响主流程
    - 可观测：每条推荐记录理由、被拒原因、被采纳率
    - 可回退：决策层异常时自动降级为"仅按空闲车位排序"，主办方可随时关闭
  - 复用项：直接复用主办方已有会员体系，不新增会员流程

- **Content Density**: Medium
- **Narrative Role**: 回应"金鹰商圈落地"维度
- **Image Requirements**: 无
- **Page Weight**: Core page

## Page 8: 合规优势
- **Page Type**: Content
- **Page Title**: 架构上就绕开了车牌敏感信息
- **Page Subtitle**: 最核心的创新功能，恰好是隐私风险最低的那个
- **Selected Template**: (Phase 6填)

- **Content Structure**: Problem/Solution
  - 三红线落地：
    - 微信订阅消息限制：不做自动定时推送；停车时主动授权一次下发凭证，返程前用户主动生成路线
    - 车牌是敏感个人信息：主链路以会员码+车位码绑定；功能①完整发生在停车前，不需要车牌
    - 地库弱网：数据随包内置，路径本地计算；空桩状态读本地缓存并显式标注时效
  - 关键架构优势：功能①（目的地选车位）完整发生在用户进车库之前——用户还没停车、还没输任何车牌，就已经完成了推荐。这不是回避合规，是从架构上绕开了它。

- **Content Density**: Medium
- **Narrative Role**: 正面回应合规隐忧——金鹰落地的隐性卡点
- **Image Requirements**: 无
- **Page Weight**: Secondary page

## Page 9: 团队与未来
- **Page Type**: Ending
- **Page Title**: 从单场提效，走向商圈级客流动线分配
- **Page Subtitle**: 让已有的能力真正被用起来
- **Selected Template**: (Phase 6填)

- **Content Structure**: Summary
  - 团队：产品/负责人______、AI/开发______、运营/现场______（待填）
  - 未来目标：同一目的地可跨场比较"哪个场更好停、更近"——停车位选择从"单场提效"升级为"商圈级客流动线分配"
  - 结语：主办方已建好一座信息完整的停车系统，缺的是最后一步——替用户做那个选择。车记得做的事情很克制：在一堆已经算好的数据之上加一层算法，让"该停哪""走哪个梯""哪个桩空着"有答案。

- **Content Density**: Light
- **Narrative Role**: 收尾——团队可信+可持续+一句话结语
- **Image Requirements**: 无
- **Page Weight**: Core page

## Page 10: 竞品能力矩阵（备份）
- **Page Type**: Content
- **Page Title**: 竞品能力矩阵
- **Page Subtitle**: 被问"凭什么别人做不到"时翻
- **Selected Template**: (Phase 6填)

- **Content Structure**: Comparison
  - 能力矩阵表：
    - ETCP/捷停车/科拓：跨场数据✔ 车位真值✔ 目的地选车位✘ 垂直交通决策✘ 空桩导航部分
    - 华为负一屏/花瓣/iOS地图：跨场数据✘ 车位真值✘ 目的地选车位✘ 垂直交通决策✘ 空桩导航✘
    - 云快充/正充：跨场数据✘ 车位真值部分 目的地选车位✘ 垂直交通决策✘ 空桩导航✔
    - 主办方现有停车系统：跨场数据部分 车位真值✔ 目的地选车位✘ 垂直交通决策✘ 空桩导航✘
    - 车记得（本次）：跨场数据复用 车位真值复用 目的地选车位✔ 垂直交通决策✔ 空桩导航✔
  - 三条结论：
    - 手机厂商恰好在"记车位"停住了——"记住"是行业天花板不是终点
    - 停车管理平台止步于"找到车"——管理侧系统不做目的地推荐
    - 充电平台只管桩不管路——不知道用户在哪个车位去哪个桩最顺

- **Content Density**: Heavy
- **Narrative Role**: 备份——被问差异化时翻
- **Image Requirements**: 无
- **Page Weight**: Secondary page

## Page 11: 技术架构与降级链（备份）
- **Page Type**: Content
- **Page Title**: 技术架构与降级链
- **Page Subtitle**: 被问"技术深度"时翻
- **Selected Template**: (Phase 6填)

- **Content Structure**: Concept
  - 架构：主办方已有停车小程序→只读→车记得决策服务层（推荐引擎/竖向路径图/状态聚合器）→复用→已有地图导航车位真值（不改动）
  - 三张新建主数据（静态可内置）：POI主数据/竖向交通主数据/车位-桩绑定
  - 降级链：
    - 功能①：同场同层近区→半径+1区→其他层→跨场→全满提示"到站前锁位"
    - 功能②：竖向建图来不及→分段编排（层内A*→换乘段→层内A*），当天可用
    - 功能③：主办方接口缺→三级来源+置信度衰减（空闲置信=exp(-τ/15min)），不伪造状态

- **Content Density**: Medium
- **Narrative Role**: 备份——被问技术可行性时翻
- **Image Requirements**: 无
- **Page Weight**: Secondary page
