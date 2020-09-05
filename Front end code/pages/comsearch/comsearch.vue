<template>
	<view class="container">
		<back-top v-show="is_show" @click.native="bakToTop"></back-top>
		<view class="header">
			<text class="first">以下是对"<text class="value">{{value}}</text>"的搜索结果:\n</text>
			<text class="result">共计<text class="result_num">{{count}}</text>条搜索结果</text>
		</view>
		<view class="body">
			<view class="comments-wrapper" v-if="!is_null">
				<view class="comment" v-for="(item,index) in comments" :key="index">
					<view class="comment-header">
						<image :src="item.author.avatarUrl" mode="" class="avatar"></image>
						<view class="username-and-time">
							<text class="username">{{item.author.username}}</text>
							<text class="date">{{item.created}}</text>
						</view>
					</view>
					<view class="comment-info">
						<jyf-parser class="content" :html="item.content" />
					</view>
					<view class="comment-footer">
						<text>浏览<text style="color: #00ffff;">{{item.browse_num}}</text>次</text>
						<image @click="approve(index,item._id)" :src="item.is_approved?approve_active_image:approve_base_image" mode=""></image>
					</view>
					<form @submit="addReply" :data-index="index" :data-comment_id="item._id">
						<view class="comment-bar">
							<input type="text" name="content" placeholder="说点什么吧..." @blur="blur" />
							<button type="default" form-type="submit">评论</button>
						</view>
					</form>

					<view class="approved_users">
						<text>当前已有<text style="color:#00FF22;+">{{item.approve_num}}</text>人点赞</text>
						<view class="approved_usernames">
							<view class="usernames">
								<text v-for="(username,index) in item.approved_users" :key="index" class="approved_name"> {{username}}</text>
								<text v-show="item.approve_num">觉得很赞</text>
							</view>
						</view>
					</view>
					<view class="replies">
						<view class="reply" v-for="(reply,index) in item.replies" :key="index">
							<text>{{reply.username}}:{{reply.content}}</text>
						</view>
					</view>
				</view>
			</view>
			<view class="sorry" v-else>
				<text>很抱歉，未查询到任何相关说说</text>
			</view>
		</view>
		<view class="bg">
			<image src="../../static/images/bgimage_1.jpg" mode=""></image>
		</view>
	</view>

</template>

<script>
	import backTop from '@/components/back-top/back-top.vue'
	import {mapState} from 'vuex'
	export default {
		data() {
			return {
				value: '中国',
				comments: [],
				is_null: true,
				is_show: false,
				count: 0,
				approve_base_image: '../../static/images/approve.png',
				approve_active_image: '../../static/images/approve_active.png',
			}
		},
		components: {
			backTop
		},
		computed:{
			...mapState(['email','username','isLogin','avatarUrl','baseUrl'])
		},
		methods: {
			bakToTop: function() {
				uni.pageScrollTo({
					scrollTop: 0,
					duration: 200
				})
			},
			approve: function(index, comment_id) {
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
						}
					});
				}
				if (this.comments[index]['is_approved']) {
					uni.request({
						url: this.baseUrl + 'api/cancelapprovecomment/',
						method: 'GET',
						data: {
							user_id: this.email,
							comment_id: comment_id
						},
						success: res => {
							console.log(res)
							if (res.data.result) {
								this.comments[index]['approve_num'] -= 1
								this.comments[index]['is_approved'] = false
								let users = this.comments[index]['approved_users']
								console.log(this.comments[index]['approved_users'])
								for(let index in users){
									if(users[index] == this.username){
										console.log('index',index)
										users.splice(index,1)
										console.log('splice')
										this.comments[index]['approved_users'] = users
										break
									}
								}
							}
						}
					});
				} else {
					uni.request({
						url: this.baseUrl + 'api/approvecomment/',
						method: 'GET',
						data: {
							user_id: this.email,
							comment_id: comment_id
						},
						success: res => {
							console.log(res)
							if (res.data.result) {
								this.comments[index]['approve_num'] += 1
								this.comments[index]['is_approved'] = true
								this.comments[index]['approved_users'].push(this.username)
							}
						}
					});
				}
			},
			addReply: function(e) {
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
						}
					});
					return
				}
				if (e.detail.value.content === '') {
					uni.showModal({
						title: '提示',
						content: '评论内容不能为空',
						showCancel: false,
						confirmText: '确认',
						success: res => {
							if (res.confirm) {
								return
							}
						}
					});
					return
				}
				uni.request({
					url: this.baseUrl + 'api/addreply/',
					method: 'POST',
					data: {
						author_id: this.email,
						content: e.detail.value.content,
						comment_id: e.currentTarget.dataset.comment_id
					},
					success: res => {
						uni.showToast({
							title: '评论成功',
							duration:750
						});
						let temp = {}
						temp.username = this.username
						temp.content = e.detail.value.content
						this.comments[e.currentTarget.dataset.index]['replies'].push(temp)
					}
				});
				console.log(e)
			},
			getSearchResult: function(value) {
				uni.showLoading({
					title: 'Loading...',
					mask: false
				});
				uni.request({
					url: this.baseUrl + 'api/comsearch/',
					method: 'GET',
					data: {
						value: value,
						user_id: this.email
					},
					success: res => {
						setTimeout(() => {
							uni.hideLoading()
							uni.showToast({
								title: '加载成功',
								duration: 750
							});
						}, 500)
						console.log(res)
						this.count = res.data.length
						if (this.count === 0) {
							this.is_null = true
						} else {
							this.is_null = false
							this.comments = res.data
						}
					},
				});
			}
		},
		onLoad: function(options) {
			console.log(options.value)
			this.value = options.value
			this.getSearchResult(this.value)
		},
		onPageScroll: function(e) {
			if (e.scrollTop >= 1000) this.is_show = true;
			else this.is_show = false
		}
	}
</script>

<style>
	.container {
		display: flex;
		flex-direction: column;
	}

	.header {
		box-shadow: #ccc 0 5rpx;
		margin: 20rpx 10rpx;
		padding: 10rpx 5rpx;
		border-top: #ccc solid 5rpx;
	}

	.header .first {
		font-weight: bold;
		font-size: 50rpx;
		color: #ccc;
	}

	.value {
		color: #184eff;
	}

	.result {
		font-size: 40rpx;
		font-weight: bold;
		color: #ccc;
	}

	.result_num {
		font-size: 50rpx;
		color: hotpink;
	}

	.sorry {
		margin-top: 100rpx;
		text-align: center;
		font-size: 50rpx;
		color: #ccc;
	}

	.bg {
		z-index: -99;
		position: fixed;
		top: 0;
		right: 0;
		left: 0;
	}

	.bg image {
		width: 100%;
		height: 100vh;
	}
</style>
