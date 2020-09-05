<template>
	<view class="container">
		<text class="welcome animation-fade animation-scale-down">欢迎加入<text>问吧</text></text>
		<form @submit="submit" ref="myForm">
			<view class="input-wrapper animation-slide-left">
				<text>用户名</text>
				<input type="text" name="username" placeholder="请输入您的用户名" />
			</view>
			<view class="input-wrapper animation-slide-right">
				<text>邮箱</text>
				<input type="text" ref="email_input" name="email" placeholder="请输入您的邮箱" />
			</view>
			<view class="input-wrapper animation-slide-left">
				<text>密码</text>
				<input type="password" name="password" placeholder="请输入密码" />
			</view>
			<view class="input-wrapper animation-slide-right">
				<text>确认密码</text>
				<input type="password" name="repassword" placeholder="请再次输入密码" />
			</view>
			<view class="input-wrapper">
				<button @click="reset" type="warn" class="animation-scale-down">重置</button>
				<button form-type="submit" type="primary" class="animation-scale-down">提交</button>
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
				popType:'top',
				duration:1500
			}
		},
		components:{
			uniPopup,
			uniPopupMessage,
			uniPopupDialog
		},
		methods: {
			submit: function(e) {
				console.log(e.detail.value)
				let values = e.detail.value
				//进行检查
				if (values.username == '') {
					this.popType = 'top'
					this.msgType = 'warn'
					this.message = '用户名不能为空！'
					this.$refs.popup.open()
				}else if(values.email==''){
					this.popType = 'top'
					this.msgType = 'error'
					this.message = '邮箱不能为空！'
					this.$refs.popup.open()
				}else if(values.password == ""){
					this.popType = 'top'
					this.msgType = 'error'
					this.message = '密码不能为空！'
					this.$refs.popup.open()
				}
				else if(values.repassword==""){
					this.popType = 'top'
					this.msgType = 'warn'
					this.message = '请重新输入密码！'
					this.$refs.popup.open()
				}else if(values.password != values.repassword){
					this.popType = 'top'
					this.msgType = 'error'
					this.message = '两次输入的密码不一致！'
					this.$refs.popup.open()
				}else if(!valideEmail(values.email)){
					this.popType = 'top'
					this.msgType = 'error'
					this.message = '邮箱不合法!'
					this.$refs.email_input.placeHolder = "请重新输入合法的邮箱地址！"
					this.$refs.email_input.valueSync = ''
					this.$refs.email_input.value = ''
					this.$refs.popup.open()
				}
				else{
					uni.request({
						url: this.$store.state.baseUrl + 'api/register/',
						method: 'GET',
						data: {
							username: values.username,
							password: values.password,
							email: values.email
						},
						success: res => {
							console.log(res)
							let user_count = res.data.user_count
							if (res.data.result == 1) {
								//注册成功
								uni.showModal({
									title: '通知',
									content: '注册成功！您是第'+user_count+'位注册问吧的用户。欢迎加入问吧！点击确认后即可跳转至登录界面...',
									showCancel: false,
									confirmText: '确认',
									success: res => {
										if(res.confirm){
											uni.navigateTo({
												url: '/pages/login/login',
											});
										}
									},
								});
							} else {
								//注册失败
								uni.showModal({
									title: '通知',
									content: '您的邮箱已被注册',
									showCancel: false,
									confirmText: '好的',
									success: res => {
										if (res.confirm) {
											this.$refs.email_input.valueSync = ""
											this.$refs.email_input.value = ""
											this.$refs.email_input.placeholder = "请输入未被注册的邮箱"
										}
									}
								});
							}
						},
						fail: () => {},
						complete: () => {}
					});
				}
			},

			reset: function() {
				console.log('reset')
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

			close: function(done) {
				done()
			},
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
		font-family: '华文行楷';
		font-size: 90rpx;
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
		height: 70rpx;
		border: solid #ccc 2rpx;
		margin-left: 10rpx;
	}

	button {
		width: 200rpx;
		margin: 60rpx 0rpx;
	}
</style>
