<template>
	<view class="container animation-slide-left">
		<back-top @click.native="backToTop" class="back"></back-top>
		<view>
			<image mode="widthFix" class="figure" :src="article.figure"></image>
		</view>
		<view class="header">
			<text class="title">{{article.inside_title}}</text>
			<view class="article-info">
				<view>
					<text class="date">{{article.date}}</text>
					<text class="seperate">|</text>
					<text class="author">{{article.author}}</text>
				</view>
				<view class="hot-info">
					<text>阅读({{browse_display}})|</text>
					<block v-if="!isFav">
						<image class="fav-image" @click="addFav" src="../../static/images/fav_normal.png" />
						<text @click="addFav">收藏({{fav_num}})</text>
					</block>
					<block v-else>
						<image @click="cancelFav" class="fav-image" src="../../static/images/fav_fill.png" />
						<text @click="cancelFav">已收藏({{fav_num}})</text>
					</block>
				</view>
			</view>
		</view>
		<view class="content">
			<jyf-parser class="content" :html="article.content" />
		</view>
		<view class="approval-wrapper">
			<view class="approval">
				<image @click="approve" src="../../static/images/approve.png"></image>
			</view>
			<text>点赞({{approval_num}})</text>
		</view>
	</view>
</template>

<script>
	import parser from "@/components/jyf-parser/jyf-parser";
	import backTop from '../../components/back-top/back-top.vue'
	import {
		mapState
	} from 'vuex'
	export default {
		data() {
			return {
				id: "",
				article: {},
				html: `content`,
				isFav: false,
				fav_num: 0,
				approval_num: 0,
				browse_num: 0,
				browse_display: '',
				options: null
			}
		},
		components: {
			"jyf-parser": parser,
			backTop,
		},
		computed: {
			...mapState(['baseUrl', 'isLogin','email'])
		},
		methods: {
			//收藏与点赞数据变化
			getChangedNumber(number) {
				if (number >= 1000) {
					return (parseFloat(number) / 1000).toFixed(1) + 'K'
				}
				return number + ''
			},
			// 点赞功能实现
			approve() {
				uni.showToast({
					title: '感谢点赞',
					image: '../../static/images/approve.png',
					duration: 500
				})
				this.approval_num += 1
				this.addApproveNum(this.id)
			},
			//添加收藏
			addFav() {
				if (!this.isLogin) {
					uni.showModal({
						title: '提示',
						content: '您当前未登录 请您先前往个人中心进行登录 点击确认可跳转至个人中心',
						showCancel: true,
						cancelText: '取消',
						confirmText: '确认',
						success: res => {
							if (res.confirm) {
								uni.switchTab({
									url: "/pages/home/home"
								})
							}
						},
						fail: () => {},
						complete: () => {}
					});
					return;
				}
				this.isFav = true
				this.fav_num = ++this.fav_num
				// uni.setStorageSync(this.id, this.article)
				// console.log('keys', uni.getStorageInfoSync().keys)
				this.increaseFavNum(this.id)
			},
			//取消收藏
			cancelFav() {
				// uni.removeStorageSync(this.id)
				this.isFav = false,
					this.fav_num = --this.fav_num
				this.decreaseFavNum(this.id)
			},
			//增加收藏量
			increaseFavNum(id) {
				uni.request({
					url: this.baseUrl + 'api/addfav/',
					method: 'GET',
					data: {
						id: id,
						user_id: this.$store.state.email
					},
					success: res => {
						// console.log(res)
					},
					fail: err => {
						console.log(err)
					},
					complete: () => {}
				});
			},
			//减少收藏量
			decreaseFavNum(id) {
				uni.request({
					url: this.baseUrl + 'api/reducefav/',
					method: 'GET',
					data: {
						id: id,
						user_id: this.$store.state.email
					},
					success: res => {
						console.log(res)
					},
					fail: () => {},
					complete: () => {}
				});
			},
			//增加浏览量
			addBrowseNum(id) {
				uni.request({
					url: this.baseUrl + 'api/addbrowsenum/',
					method: 'GET',
					data: {
						id: id
					},
					success: res => {
						// console.log(res)
						this.browse_num += 1
						this.browse_display = this.getChangedNumber(this.browse_num)
					},
					fail: err => {
						console.log(err)
					},
					complete: () => {}
				})
			},
			//增加点赞量
			addApproveNum(id) {
				uni.request({
					url: this.baseUrl + 'api/addapprovenum/',
					method: 'GET',
					data: {
						id: id
					},
					success: res => {
						// console.log(res)
					},
					fail: () => {},
					complete: () => {}
				});
			},
			backToTop() {
				console.log('----')
				uni.pageScrollTo({
					duration: 400,
					scrollTop: 0
				})
			},
			loadData: function(options) {
				uni.showLoading({
					title: 'Loading...',
				})
				// let id = options.id
				let id = Number(options.id)
				uni.request({
					url: this.baseUrl + 'data/detail/',
					method: 'GET',
					data: {
						id: id
					},
					success: res => {
						// console.log(res)
						this.article = res.data,
						this.id = String(res.data._id),
						this.fav_num = res.data.fav_num,
						this.approval_num = res.data.approve_num,
						this.browse_num = res.data.browse_num
						uni.hideLoading()
						this.addBrowseNum(id)

						// let keys = uni.getStorageInfoSync().keys
						// console.log("keys",keys)
						// if (keys.find(item => {
						// 		return item == id
						// 	}) && this.isLogin) {
						// 	this.isFav = true
						// }
						//判断是否已经收藏
						if(this.isLogin){
							uni.request({
								url: this.baseUrl + 'api/judgeisfav/',
								method: 'GET',
								data: {
									user_id : this.email,
									article_id : this.article._id
								},
								success: res => {
									// console.log(res)
									if(res.data.is_fav) this.isFav = true
								},
								fail: () => {},
								complete: () => {}
							});
						}
						
						setTimeout(() => {
							uni.stopPullDownRefresh()
						}, 1000)
					},
					fail: err => {
						console.log(err)
					},
					complete: () => {}
				})
			}
		},
		//正在加载
		onLoad(options) {
			this.loadData(options)
			this.options = options
		},
		onPullDownRefresh: function() {
			this.loadData(this.options)
		}
	}
</script>

<style>
	/* miniprogram/pages/detail/detail.wxss */
	.container {
		display: flex;
		flex-direction: column;
	}

	.figure {
		width: 100%;
	}

	.header {
		display: flex;
		flex-direction: column;
	}

	.article-info {
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		font-size: 30rpx;
	}

	.title {
		font-weight: bold;
		font-size: 50rpx;
		line-height: 65rpx;
		margin: 10rpx 5rpx;
	}

	.content {
		margin: 10rpx 5rpx;
	}

	.article-info .date {
		color: #888;
	}

	.article-info .author {
		color: rgb(13, 72, 221);
	}

	.seperate {
		margin: 0rpx 5rpx;
	}

	.hot-info {
		color: #777;
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		font-size: 30rpx;
	}

	.fav-image {
		width: 45rpx;
		height: 45rpx;
		position: relative;
		top: 5rpx;
	}

	.approval-wrapper {
		display: flex;
		flex-direction: column;
		justify-content: space-around;
		align-items: center;
	}

	.approval {
		background-color: chartreuse;
		width: 130rpx;
		height: 130rpx;
		border-radius: 50%;
	}

	.approval image {
		width: 80rpx;
		height: 80rpx;
		position: relative;
		top: 20rpx;
		left: 26rpx;
	}

	.approval text {
		align-self: center;
		position: relative;
		top: 20rpx;
	}

	.content {
		font-size: 40rpx;
	}
</style>
