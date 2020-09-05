<template>
	<view class="container">
		<view class="header animation-slide-left">
			<block v-if="this.$store.state.isLogin">
				<view class="user-info-wrapper">
					<image @click="chooseAvatar" class="avatar" :src="this.avatarUrl"></image>
					<view class="info-text-wrapper">
						<text class="info-text">用户名:{{username}}</text>
						<text class="info-text">邮箱:{{email}}</text>
					</view>
				</view>
			</block>
			<block v-else>
				<text class="tip-text">您当前未登录</text>
				<view class="button-wrapper">
					<button type="primary" class="login-button" @click="gotoLogin">登录</button>
					<button type="default" class="reg-button" @click="gotoRegister">注册</button>
				</view>
			</block>
		</view>
		<view class="middle" v-show="this.isLogin">
			<view class="comment_wrapper" @click="gotoMyComment">
				<text class="comment-text">我的说说</text>
				<image src="../../static/images/right_row.png" mode=""></image>
			</view>
			<text class="fav-text">我的收藏(<text class="fav-num">{{fav_count}}</text>)</text>
		</view>
		<view class="footer" v-show="this.isLogin">
			<view class="article-warper">
				<view class="article" :class="{'animation-slide-left':(index%2==0),'animation-slide-right':(index%2==1)}" v-for="(item,index) in articles"
				 :key="index">
					<view>
						<image mode="center" class="preview" :src="item.preview"></image>
					</view>
					<view class="container">
						<view class="article-info" @click="gotoDeatil(item._id)">
							<text class="title">{{item.title}}</text>
							<text class="desc">{{item.desc}}</text>
						</view>
						<view class="bottom-container">
							<text class="author">作者 {{item.author}}</text>
							<text class="browse">阅读 {{item.browse_num}}</text>
						</view>
					</view>
				</view>
			</view>
		</view>
		<view class="bg">
			<image src="../../static/images/bgimage_1.jpg" mode=""></image>
		</view>
	</view>
</template>

<script>
	import {
		mapState
	} from 'vuex'
	export default {
		data() {
			return {
				articles: [],
				fav_count: 0
			}
		},
		computed: {
			...mapState(['username', 'avatarUrl', 'isLogin', 'email', 'baseUrl'])
		},
		methods: {
			gotoDeatil: function(id) {
				uni.navigateTo({
					url: '/pages/detail/detail?id=' + id,
				});
			},
			gotoLogin: function() {
				uni.navigateTo({
					url: '/pages/login/login',
				});
			},
			gotoRegister: function() {
				uni.navigateTo({
					url: '/pages/register/register'
				})
			},
			chooseAvatar: function() {
				uni.chooseImage({
					count: 1,
					sourceType: ['album', 'camera'],
					success: res => {
						var imgFile = res.tempFilePaths[0]
						uni.getImageInfo({
							src: imgFile,
							success: res => {
								let avatar = new Image()
								avatar.src = imgFile
								let width = res.width
								let height = res.height
								// console.log(width,height)
								var canvas = document.createElement('canvas')
								canvas.width = width
								canvas.height = height
								var ctx = canvas.getContext('2d')
								ctx.drawImage(avatar, 0, 0)
								let base64 = canvas.toDataURL('image/jpeg', 0.1)
								// console.log(base64)
								uni.request({
									url: this.baseUrl + 'api/changeavatar/',
									method: 'POST',
									data: {
										avatarUrl: base64,
										user_id: this.email
									},
									success: res => {
										console.log(res)
										if (res.data.result == 1) {
											this.$store.state.avatarUrl = base64
											uni.showModal({
												title: '提示',
												content: '头像更换成功',
												showCancel: false,
												confirmText: '好的'
											});
										}
									}
								});
							}
						})
					}
				})
			},
			gotoMyComment:function(){
				uni.navigateTo({
					url: '/pages/mycomments/mycomments'
				});
			}
		},
		onLoad: function() {

		},
		onShow: function() {
			if (this.isLogin) {
				uni.request({
					url: this.$store.state.baseUrl + 'api/getfavs/',
					method: 'GET',
					data: {
						user_id: this.email
					},
					success: res => {
						this.articles = res.data.articles
						this.fav_count = res.data.articles.length
					},
					fail: () => {},
					complete: () => {}
				});
			}
		}
	}
</script>

<style>
	.container {
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: space-around;
	}

	.header {
		width: 100%;
		margin: 20rpx 0;
		display: flex;
		flex-direction: column;
		text-align: center;
		box-shadow: #ddd 0 5rpx;
		border-top: #ddd solid 5rpx;
		padding: 15rpx 0rpx;
	}

	.tip-text {
		font-size: 60rpx;
		font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
		font-weight: 600;
		margin: 50rpx;
		color: #ccc;
	}

	.button-wrapper {
		display: flex;
		flex-direction: row;
		margin-bottom: 10rpx;
	}

	.login-button {
		width: 200rpx;
		position: relative;
		left: 40rpx;
	}

	.reg-button {
		width: 200rpx;
		position: relative;
		right: 40rpx;
	}

	.middle {
		margin: 20rpx 0rpx;
		display: flex;
		flex-direction: column;
	}

	.fav-text,.comment-text{
		margin: 10rpx 10rpx;
		font-size: 45rpx;
		font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
		font-weight: 545;
		color: #eee;
	}

	.fav-num {
		color: hotpink;
		font-size: 55rpx;
		font-weight: 560;
	}

	.footer {
		box-shadow: #ddd 0 -5rpx;
	}

	.avatar {
		width: 150rpx;
		height: 150rpx;
		border-radius: 50%;
	}

	.user-info-wrapper {
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		font-size: 36rpx;
	}

	.info-text-wrapper {
		display: flex;
		flex-direction: column;
		text-align: center;
		justify-content: space-around;
	}

	.change-avatar-tip {
		position: fixed;
		font-size: 22rpx;
		top: 160rpx;
		left: 90rpx;
		z-index: 99;
		font-weight: bold;
		color: #000000;
	}

	.info-text {
		width: 550rpx;
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 1;
		overflow: hidden;
		text-overflow: ellipsis;
		word-break: break-all;
		color: #eee;
	}

	.article-info {
		color: #eee;
	}
	
	.comment_wrapper{
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		border-top:solid #aaa 4rpx;
		border-bottom: solid #aaa 4rpx;
	}
	.comment_wrapper image{
		width: 60rpx;
		height: 60rpx;
		margin-right: 450rpx;
	}
</style>