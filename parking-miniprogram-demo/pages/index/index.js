const FLOORS = ['B1', 'B3', 'B4', 'B5']

// 各楼层标记点（坐标对应 SVG 800x1000 坐标系）
const MARKERS = {
  B1: [
    { id: 'B1-036', type: 'pin', x: 318, y: 144, label: 'B1-036', typeText: 'B1 普通车位', highlight: true },
    { id: 'E2', type: 'elevator', x: 176, y: 236, label: '2号电梯厅', icon: '梯' },
    { id: 'E4', type: 'elevator', x: 596, y: 236, label: '4号电梯厅', icon: '梯' },
    { id: 'E6', type: 'elevator', x: 176, y: 792, label: '6号电梯厅', icon: '梯' },
    { id: 'E5', type: 'elevator', x: 436, y: 556, label: '5号电梯厅', icon: '梯' },
  ],
  B3: [
    { id: 'E3', type: 'elevator', x: 256, y: 256, label: '3号电梯厅', icon: '梯' },
    { id: 'E7', type: 'elevator', x: 536, y: 696, label: '7号电梯厅', icon: '梯' },
  ],
  B4: [
    { id: 'B4-162', type: 'pin', x: 98, y: 300, label: 'B4-162', typeText: 'B4 普通车位', highlight: false },
    { id: 'E1', type: 'elevator', x: 576, y: 476, label: '1号电梯厅', icon: '梯' },
  ],
  B5: [
    { id: 'E1', type: 'elevator', x: 216, y: 216, label: '1号电梯厅', icon: '梯' },
    { id: 'E8', type: 'elevator', x: 576, y: 216, label: '8号电梯厅', icon: '梯' },
    { id: 'E9', type: 'elevator', x: 216, y: 776, label: '9号电梯厅', icon: '梯' },
  ],
}

Page({
  data: {
    systemInfo: {},
    navBarHeight: 88,
    floors: FLOORS,
    currentFloor: 'B4',
    currentFloorLower: 'b4',
    viewMode: '2D',
    mode: 'route', // overview | spot | route
    mapWidth: 800,
    mapHeight: 1000,
    mapX: 0,
    mapY: 0,
    mapScale: 1,
    mapSrc: '/images/map_b4_route.svg',
    spotMarkers: [],
    selectedSpot: null,
    endSpot: 'B4-B4-162',
    plate: '粤T997LF',
    routeDistance: 7,
    routeTime: 2,
    showSearch: false,
    searchValue: '',
    toastText: '',
  },

  onLoad() {
    this.initSystemInfo()
    this.updateMarkers()
    this.updateMapSrc()
  },

  initSystemInfo() {
    const info = wx.getSystemInfoSync()
    const navBarHeight = info.platform === 'ios' ? 88 : 96

    this.setData({
      systemInfo: info,
      navBarHeight,
    })
  },

  updateMarkers() {
    const markers = MARKERS[this.data.currentFloor] || []
    // 复制并重新计算高亮
    const processed = markers.map(m => ({
      ...m,
      highlight: this.data.mode === 'spot' && this.data.selectedSpot && this.data.selectedSpot.id === m.id
    }))
    this.setData({ spotMarkers: processed })
  },

  updateMapSrc() {
    const { mode, currentFloorLower } = this.data
    const suffix = mode === 'route' && this.data.currentFloor === 'B4' ? '_route' : ''
    this.setData({
      mapSrc: `/images/map_${currentFloorLower}${suffix}.svg`
    })
  },

  onFloorChange(e) {
    const floor = e.currentTarget.dataset.floor
    const index = FLOORS.indexOf(floor)
    this.switchFloor(index)
  },

  onFloorUp() {
    const index = FLOORS.indexOf(this.data.currentFloor)
    if (index > 0) {
      this.switchFloor(index - 1)
    }
  },

  onFloorDown() {
    const index = FLOORS.indexOf(this.data.currentFloor)
    if (index < FLOORS.length - 1) {
      this.switchFloor(index + 1)
    }
  },

  switchFloor(index) {
    const floor = FLOORS[index]
    const lower = floor.toLowerCase()

    // 切楼层时回归总览模式（除 B4 路线演示外）
    let newMode = this.data.mode
    if (newMode === 'route' && floor !== 'B4') {
      newMode = 'overview'
    }

    this.setData({
      currentFloor: floor,
      currentFloorLower: lower,
      mode: newMode,
      selectedSpot: null,
      mapScale: 1,
      mapX: 0,
      mapY: 0,
    }, () => {
      this.updateMapSrc()
      this.updateMarkers()
    })
  },

  toggleViewMode() {
    const next = this.data.viewMode === '2D' ? '3D' : '2D'
    this.setData({ viewMode: next })
    this.showToast(`已切换至 ${next} 视图`)
  },

  onSpotTap(e) {
    const item = e.currentTarget.dataset.item
    if (item.type === 'pin') {
      this.setData({
        mode: 'spot',
        selectedSpot: { ...item },
      }, () => {
        this.updateMarkers()
      })
    }
  },

  setAsDestination() {
    const spot = this.data.selectedSpot
    if (!spot) return
    if (this.data.currentFloor !== 'B4') {
      this.showToast('导航 Demo 仅展示 B4 路线')
      return
    }
    this.setData({
      mode: 'route',
      endSpot: `${this.data.currentFloor}-${spot.id}`,
      selectedSpot: null,
    }, () => {
      this.updateMapSrc()
      this.updateMarkers()
    })
  },

  focusSpot() {
    this.showToast('已聚焦到当前车位')
  },

  closeSpot() {
    this.setData({
      mode: 'overview',
      selectedSpot: null,
    }, () => {
      this.updateMarkers()
    })
  },

  cancelRoute() {
    this.setData({
      mode: 'overview',
      selectedSpot: null,
    }, () => {
      this.updateMapSrc()
      this.updateMarkers()
    })
  },

  startNav() {
    this.showToast('模拟导航开始')
  },

  onSearch() {
    this.setData({ showSearch: true, searchValue: '' })
  },

  closeSearch() {
    this.setData({ showSearch: false })
  },

  onSearchInput(e) {
    this.setData({ searchValue: e.detail.value })
  },

  confirmSearch() {
    const val = this.data.searchValue.trim()
    if (!val) {
      this.showToast('请输入车牌或车位号')
      return
    }
    this.closeSearch()
    // 简单演示：若输入包含 B4-162 切到 B4 路线；若包含 B1-036 切到 B1 选点
    if (val.includes('B4-162') || val.includes('162')) {
      this.setData({
        currentFloor: 'B4',
        currentFloorLower: 'b4',
        mode: 'route',
        endSpot: 'B4-B4-162',
        plate: val.includes('粤') ? val : '粤T997LF',
      }, () => {
        this.updateMapSrc()
        this.updateMarkers()
      })
    } else if (val.includes('B1-036') || val.includes('036')) {
      this.setData({
        currentFloor: 'B1',
        currentFloorLower: 'b1',
        mode: 'spot',
        selectedSpot: { ...MARKERS.B1[0] },
      }, () => {
        this.updateMapSrc()
        this.updateMarkers()
      })
    } else {
      this.showToast(`未找到与「${val}」匹配的车位`)
    }
  },

  onHome() {
    this.showToast('返回首页')
  },

  onMapLoad() {
    console.log('map loaded:', this.data.mapSrc)
  },

  noop() {},

  showToast(text) {
    this.setData({ toastText: text })
    setTimeout(() => {
      this.setData({ toastText: '' })
    }, 2000)
  },
})
