<template>
	<view class="container">
		<rich-editor ref="editor" placeholder="写点什么吧..." @contentChange="contentChange"></rich-editor>
		<button @click="submit" type="default">发布</button>
	</view>
</template>

<script>
	import richEditor from '../../components/rich-editor/rich-editor.vue'
	import {
		pathToBase64,
		base64ToPath
	} from '@/utils/image-tools/index.js'
	import {
		urlTobase64
	} from '@/utils/index.js'
	import {
		mapState
	} from 'vuex'
	export default {
		data() {
			return {
				html: '',
				text: '',
			}
		},
		components: {
			richEditor
		},
		computed: {
			...mapState(['email', 'username', 'avatarUrl', 'baseUrl', 'isLogin'])
		},
		methods: {
			contentChange: function(detail) {
				this.html = detail.html
				this.text = detail.text
			},
			submit: function() {
				if (this.isLogin) {
					if (this.html === '') {
						uni.showModal({
							title: '提示',
							content: '发布内容不能为空！',
							showCancel: false,
							confirmText: '好的',
							success: res => {
								if (res.confirm) {
									return;
								}
							}
						});
						return;
					}
					uni.showLoading({
						title: '正在发布...',
						mask: false
					});
					console.log('submit')
					let match_result = this.html.match(/src=".+?"/g)
					this.html = this.html.replace(/data-local=\".+?\"/, '')
					// 如果有图片的话-
					if (match_result) {
						let previous_list = []
						for (let result of match_result) {
							previous_list.push(result.substring(result.indexOf('"') + 1, result.lastIndexOf('"')))
						}
						let changed_list = []
						new Promise((resolve, reject) => {
							let new_html = this.html
							let count = 0
							let length = previous_list.length
							for (let value of previous_list) {
								uni.getImageInfo({
									src: value, //临时路径
									// responseType: 'blob', //设置返回的数据格式为arrraybuffer
									success: res => {
										console.log('res', res)
										let img = new Image()
										img.src = value
										let width = res.width
										let height = res.height
										// console.log(width, height)
										var canvas = document.createElement('canvas')
										canvas.width = width
										canvas.height = height
										var ctx = canvas.getContext('2d')
										ctx.drawImage(img, 0, 0)
										let base64 = ''
										if (width * height > 1e6) {
											if (length > 1) {
												base64 = canvas.toDataURL('image/jpeg', 0.1)
											} else {
												if (width > 3000 || height > 3000) {
													base64 = canvas.toDataURL('image/jpeg', 0.25)
												} else {
													base64 = canvas.toDataURL('image/jpeg', 0.5)
												}
											}
										} else {
											console.log(base64)
											base64 = canvas.toDataURL('image/jpeg', 1.0)
										}
										console.log(base64)
										let size = base64.length
										if (size > 1024 * 1024) reject(size)
										new_html = new_html.replace(value, base64)
										count++
										if (count == length) resolve(new_html)
									},
									fail: err => {
										console.log(err)
									}
								})
							}
						}).then(html => {
							// console.log('html',html)
							uni.request({
								url: this.baseUrl + 'api/addcomment/',
								method: 'POST',
								header: {
									"Content-type": "application/json"
								},
								data: {
									author_id: this.email,
									content: html,
									text_content: this.text,
									author_name: this.username
								},
								success: res => {
									console.log(res)
									setTimeout(() => {
										uni.hideLoading()
										uni.switchTab({
											url: '../community/community'
										})
									}, 500)
								},
							});
						}).catch(err => {
							console.log('err size', err)
							setTimeout(() => {
								uni.hideLoading()
								uni.showModal({
									title: '提示',
									content: '上传的图片压缩后暂时不能超过1M 您上传的图片中有一张大小为' + String((err / 1024.0 / 1024.0).toFixed(2)) + 'M 非常抱歉...',
									showCancel: false,
									confirmText: '好的',
									success: res => {
										uni.switchTab({
											url: '../community/community'
										})
									},
								});
							}, 500)

						})
					} else {
						console.log('no image')
						uni.request({
							url: this.baseUrl + 'api/addcomment/',
							method: 'POST',
							header: {
								"Content-type": "application/json"
							},
							data: {
								author_id: this.email,
								content: this.html,
								text_content: this.text,
								author_name: this.username
							},
							success: res => {
								setTimeout(() => {
									uni.hideLoading()
									uni.switchTab({
										url: '../community/community'
									})
								}, 500)
							}
						});
					}

				} else {
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
				}
			},

		},
		onLoad: function(options) {

		}
	}
</script>

<style>
	.container {
		display: flex;
		flex-direction: column;
		justify-content: space-around;
	}

	button {
		width: 95%;
	}
</style>
