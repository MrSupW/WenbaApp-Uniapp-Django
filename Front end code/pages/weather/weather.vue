<template>
	<view class='container animation-slide-left' >
		<region-picker @change="changeRegion" class="region-picker" @changeRegion="changeRegion">
			<text class="tip-text">点击此处更换地区哟</text>
		</region-picker>
		<text class="tmp-text">{{tmp}}℃ {{cond_txt}}</text>
		<image :src="image_url"></image>
		<view class="detail">
			<view class="bar">
				<view class="box">相对湿度</view>
				<view class="box">气压</view>
				<view class="box">能见度</view>
			</view>
			<view class="bar active">
				<view class="box">{{hum}}%</view>
				<view class="box">{{pres}}hPa</view>
				<view class="box">{{vis}}Km</view>
			</view>
			<view class="bar">
				<view class="box">风向</view>
				<view class="box">风速</view>
				<view class="box">风力</view>
			</view>
			<view class="bar active">
				<view class="box">{{wind_dir}}</view>
				<view class="box">{{wind_spd}}Km/h</view>
				<view class="box">{{wind_sc}}级</view>
			</view>
		</view>
		<view class="bg">
			<image src="../../static/images/bgimage_2.jpg" mode=""></image>
		</view>
	</view>
</template>

<script>
	import regionPicker from '../../components/region-picker/region-picker.vue'
	export default {
		data() {
			return {
				city: '周口市',
				tmp: 19,
				cond_code: 999,
				cond_txt: '多云',
				wind_dir: '西北',
				wind_sc: '3-4',
				wind_spd: 15,
				hum: 40,
				pres: '1020',
				vis: 10,
				image_url: '../../static/images/999.png',
				dialogShow: false
			}
		},
		components: {
			regionPicker
		},
		methods: {
			changeRegion(city) {
				// console.log("city",city)
				this.city = city
				this.getWeather(this.city) //更新天气   
			},
			getWeather(city) {
				var that = this //this不可以直接在微信API内部使用
				uni.request({
					url: 'https://free-api.heweather.net/s6/weather/now?',
					data: {
						location: city,
						key: '95be21217325428690cb3048fd428419'
					},
					success: (res) => {
						let detail = res.data.HeWeather6[0].now
						console.log(detail)
						this.tmp = detail.tmp
						this.cond_code = detail.cond_code
						this.cond_text = detail.cond_text
						this.wind_dir = detail.wind_dir
						this.wind_sc = detail.wind_sc
						this.wind_spd = detail.wind_spd
						this.hum = detail.hum
						this.pres = detail.pres
						this.vis = detail.vis
						this.image_url = "../../static/images/" + detail.cond_code + '.png'
					},
					fail: function(res) {
						console.log('failed')
					}
				})
			},
		}
	}
</script>

<style>
	/* pages/index/index.wxss */

	.container {
		height: calc(100vh - 200rpx);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-around;
	}

	.detail {
		width: 100%;
		display: flex;
		flex-direction: column;
	}

	.bar {
		display: flex;
		flex-direction: row;
		margin: 20rpx 0;
	}

	.box {
		width: 33.3%;
		text-align: center;
	}

	.tmp-text {
		font-size: 80rpx;
		color: #0000ff;
	}

	image {
		width: 300rpx;
		height: 300rpx;
	}

	.active {
		font-weight: bold;
		font-size: 50rpx;
	}

	.tip-text {
		font-size: 35rpx;
		color: #052afc;
	}

	.region-picker {
		/* align-items: center; */
		text-align: center;
	}
	.bg{
		z-index: -99;
		position: fixed;
		top: 0;
		right: 0;
		left: 0;
	}
	.bg image{
		width: 100%;
		height: calc(100vh - 10rpx);
	}
</style>
