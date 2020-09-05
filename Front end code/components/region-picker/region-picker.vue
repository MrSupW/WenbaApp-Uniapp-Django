<template>
	<view>
			<view @tap="togglePopup('bottom','popup')" style="padding: 40upx;display: flex;align-items: center;">
				<view v-for="(item, index) in selectList" :key="index">
					{{item.txt}}<span v-show="index == 0 || index == 1">—</span>
				</view>
			</view>
			<uni-popup ref="popup" :type="type" @change="change">
				<view class="select-border">
					<view class="header">
						<view class="title">
							选择地区
						</view>
						<view class="cancel-icon" @tap="cancel('popup')">
							X
						</view>
					</view>
					<view class="select-box">
						<view class="select-item">
							<view class="select-list" @tap="tabEvent(index)" :class="indexTab == index ? 'selected' : ''" v-for="(item, index) in selectList"
							 :key="index">
								{{item.txt}}
							</view>
						</view>
						<view class="select-item-box">
							<!-- 省 -->
							<view class="province-box" v-show="proviceShow">
								<view class="select-list-cont" @tap="provinceEvent(item,index)" v-for="(item,index) in provinceData" :key="item.code">
									{{item.name}}<span class="check" v-show="index == checkOne">√</span>
								</view>
							</view>
							<!-- 市 -->
							<view class="city-box" v-show="cityShow">
								<view class="select-list-cont" @tap="cityEvent(item,index)" v-for="(item,index) in cityData" :key="item.code">
									{{item.name}}<span class="check" v-show="index==checkTwo">√</span>
								</view>
							</view>
							<!-- 区 -->
							<view class="area-box" v-show="areaShow">
								<view class="select-list-cont" @tap="areaEvent(item,index)" v-for="(item,index) in areaData" :key="item.code">
									{{item.name}}<span class="check" v-show="index==checkThree">√</span>
								</view>
							</view>
						</view>
					</view>
				</view>
			</uni-popup>
		</view>
</template>

<script>
	import cityDatas from './city.area.js'
	import uniPopup from './unipop.vue'
export default {
		components: {
			uniPopup
		},
		data() {
			return {
				provinceData: cityDatas,
				cityData: [],
				areaData: [],
				selectList: [{
					txt: '请选择'
				}, {
					txt: '请选择'
				}, {
					txt: '请选择'
				}],
				tabOne: '请选择',
				indexTab: 0,
				proviceShow: true,
				areaShow: false,
				cityShow: false,
				show: false,
				type: '',
				checkOne: null,
				checkTwo: null,
				checkThree: null,
			}
		},
		onLoad() {
 
		},
		watch: {
 
		},
		methods: {
			togglePopup(type, open) {
				this.type = type
				if (open === 'tip') {
					this.show = true
				} else {
					this.$refs[open].open()
				}
			},
			cancel(type) {
				if (type === 'tip') {
					this.show = false
					return
				}
				this.$refs[type].close()
			},
			change(e) {
				if (e.show == true) {
					uni.hideTabBar()
				} else {
					uni.showTabBar()
				}
			},
			tabEvent(index) {
				this.indexTab = index
				if (this.indexTab == 0) {
					this.proviceShow = true
					this.cityShow = false
					this.areaShow = false
					// this.checkOne = null
					this.checkTwo = null
					this.checkThree = null
					// this.cityData = []
					this.areaData = []
					// this.selectList[0].txt = "请选择"
					this.selectList[1].txt = "请选择"
					this.selectList[2].txt = "请选择"
				} else if (this.indexTab == 1) {
					this.proviceShow = false
					this.cityShow = true
					this.areaShow = false
					// this.checkTwo = null
					this.checkThree = null
					// this.areaData = []
					// this.selectList[1].txt = "请选择"
					this.selectList[2].txt = "请选择"
				} else if (this.indexTab == 2) {
					this.proviceShow = false
					this.cityShow = false
					this.areaShow = true
				}
			},
			provinceEvent(data, index) {
				this.checkOne = index
				this.selectList[0].txt = data.name
				this.indexTab = 1
				this.proviceShow = false
				this.cityShow = true
				this.areaShow = false
				this.cityData = data.cityList
			},
			cityEvent(data, index) {
				this.checkTwo = index
				this.selectList[1].txt = data.name
				this.indexTab = 2
				this.proviceShow = false
				this.cityShow = false
				this.areaShow = true
				this.areaData = data.areaList
				// console.log("data.name",data.name)
				this.$emit('changeRegion',data.name)
			},
			areaEvent(data, index) {
				this.checkThree = index
				this.selectList[2].txt = data.name
				this.$emit('changeRegion',this.selectList[1].txt)
			}
		}
	}

</script>

<style>
	view{
		color: #eee;
	}
	.header {
			display: flex;
			align-items: center;
			justify-content: space-between;
			padding: 35upx;
		}
	 
		.title {
			font-size: 34upx;
			font-family: PingFang SC;
			font-weight: bold;
			color: rgba(51, 51, 51, 1);
		}
	 
		.cancel-icon {
			font-size: 34upx;
			color: rgba(153, 153, 153, 1);
		}
	 
		.check {
			padding-left: 17upx;
			color: #FF7E28;
		}
	 
		.select-box {
			height: 1024upx;
		}
	 
		.select-item {
			display: flex;
			align-items: center;
			padding-left: 50upx;
			margin-bottom: 20upx;
			border-bottom: 1px solid #F6F6F6;
		}
	 
		.select-list {
			width: 120upx;
			height: 40upx;
			text-align: center;
			overflow: hidden;
			/*超出部分隐藏*/
			text-overflow: ellipsis;
			/* 超出部分显示省略号 */
			white-space: nowrap;
			/*规定段落中的文本不进行换行 */
			font-size: 30upx;
			font-family: PingFang SC;
			font-weight: bold;
			color: rgba(51, 51, 51, 1);
			margin-right: 30upx;
			border-bottom: 1px solid #FFFFFF;
		}
	 
		.select-list-cont {
			padding-left: 67upx;
			font-size: 30upx;
			font-family: PingFang SC;
			font-weight: 500;
			color: rgba(51, 51, 51, 1);
			line-height: 40px;
		}
	 
		.selected {
			border-bottom: 1px solid #F0AD4E;
			color: rgba(255, 133, 0, 1);
		}
</style>
