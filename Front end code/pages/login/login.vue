<template>
	<view class="container">
		<text class="welcome animation-scale-down">欢迎登录<text>问吧</text></text>
		<text class="change-tip animation-slide-bottom" @click="changeLoginMode">{{change_to_mode}}</text>
		<form @submit="submit" ref="myForm">
			<view class="input-wrapper animation-slide-left" v-if="is_username">
				<text>用户名</text>
				<input type="text" name="username" placeholder="请输入您的用户名" />
			</view>
			<view class="input-wrapper animation-slide-left" v-else>
				<text>邮箱</text>
				<input type="text" name="email" placeholder="请输入您的邮箱" />
			</view>
			<view class="input-wrapper animation-slide-right">
				<text>密码</text>
				<input type="password" name="password" placeholder="请输入密码" />
			</view>
			<view class="input-wrapper">
				<button type="warn" @click="reset" class="animation-fade animation-scale-down">重置</button>
				<button form-type="submit" type="primary" class="animation-fade animation-scale-down">登录</button>
			</view>
		</form>
		<uni-popup ref="popup" :type="popType">
			<uni-popup-message :type="msgType" :message="message" :duration="duration"></uni-popup-message>
		</uni-popup>
		<view class="bg">
			<image src="../../static/images/bgimage_3.jpg" mode=""></image>
		</view>
	</view>
</template>

<script>
	import uniPopup from '@/components/uni-popup/uni-popup.vue'
	import uniPopupMessage from '@/components/uni-popup/uni-popup-message.vue'
	import uniPopupDialog from '@/components/uni-popup/uni-popup-dialog.vue'
	import {valideEmail} from '@/utils/index.js'
	export default {
		data() {
			return {
				msgType: 'error',
				message: '注册成功',
				popType: 'top',
				duration: 1500,
				is_username: true,
				change_to_mode: '切换至邮箱登录'
			}
		},
		components: {
			uniPopup,
			uniPopupMessage,
			uniPopupDialog
		},
		methods: {
			submit: function(e) {
				// console.log(e.detail.value)
				let values = e.detail.value
				//进行检查
				if (this.is_username && values.username == '') {
					this.popType = 'top'
					this.msgType = 'warn'
					this.message = '用户名不能为空！'
					this.$refs.popup.open()
				} else if (!this.is_username && values.email == '') {
					this.popType = 'top'
					this.msgType = 'error'
					this.message = '邮箱不能为空！'
					this.$refs.popup.open()
				} else if (!this.is_username && !valideEmail(values.email)) {
					this.popType = 'top'
					this.msgType = 'error'
					this.message = '邮箱不合法!'
					this.$refs.email_input.placeHolder = "请重新输入合法的邮箱地址！"
					this.$refs.email_input.valueSync = ''
					this.$refs.email_input.value = ''
					this.$refs.popup.open()
				} else if (values.password == "") {
					this.popType = 'top'
					this.msgType = 'error'
					this.message = '密码不能为空！'
					this.$refs.popup.open()
				} else {
					uni.request({
						url: this.$store.state.baseUrl + 'api/login/',
						method: 'GET',
						data: {
							username: values.username,
							password: values.password,
							email: values.email
						},
						success: res => {
							// console.log(res)
							if (res.data.result == 1) {
								//登录成功
								// console.log(res)
								this.$store.state.isLogin = true
								this.$store.state.username = res.data.userInfo.username
								this.$store.state.avatarUrl = res.data.userInfo.avatarUrl
								this.$store.state.email = res.data.userInfo.email
								uni.showModal({
									title: '通知',
									content: '登录成功 欢迎回来 点击确认后即可跳转至个人中心',
									showCancel: false,
									confirmText: '确认',
									success: res => {
										if (res.confirm) {
											console.log('navigateTo')
											uni.switchTab({
												url:'/pages/home/home'
											})
										}
									},
								});
							} else {
								//登录失败
								uni.showModal({
									title: '通知',
									content: '用户名或密码有误',
									showCancel: false,
									confirmText: '好的'
								});
							}
						}
					});
				}
			},
			reset: function() {
				uni.showModal({
					title: '提示',
					content: '您确定要重置表单内容吗？',
					showCancel: true,
					cancelText: '取消',
					confirmText: '确认',
					success: res => {
						if (res.confirm) {
							this.$refs.myForm._onReset()
						} else if (res.cancel) {
							uni.showToast({
								title: '已取消重置操作',
								icon: 'none',
								duration: 500
							});
						}
					},
					fail: () => {},
					complete: () => {}
				});
			},
			changeLoginMode: function() {
				if (this.is_username) {
					uni.redirectTo({
						url: '/pages/login/login?mode=email',
					});
				} else {
					uni.redirectTo({
						url: '/pages/login/login?mode=username',
					});
				}
			}
		},
		onLoad(options) {
			let mode = options.mode || 'username'
			if (mode === 'username') {
				this.is_username = true
				this.change_to_mode = "切换至邮箱登录"
			} else {
				this.is_username = false
				this.change_to_mode = "切换至用户名登录"
			}
		}
	}
</script>

<style>
	.welcome {
		font-size: 85rpx;
		font-family: '华文楷体';
		font-weight: bold;
		color: hotpink;
	}

	.welcome text {
		color: #007AFF;
		font-size: 90rpx;
		font-family: '华文行楷';
	}

	.container {
		height: calc(85vh - 200rpx);
		display: flex;
		flex-direction: column;
		justify-content: space-around;
		align-items: center;
	}

	.input-wrapper {
		display: flex;
		flex-direction: row;
		margin: 20rpx 0;
		justify-content: space-between;
		align-items: center;
	}

	.input-wrapper text {
		font-size: 38rpx;
		line-height: 60rpx;
		font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
	}

	input {
		height: 90rpx;
		border: solid #ccc 2rpx;
		margin-left: 10rpx;
	}

	button {
		width: 180rpx;
		margin: 60rpx 0rpx;
	}

	.change-tip {
		color: #9000FF;
		text-decoration: underline;
	}
</style>
