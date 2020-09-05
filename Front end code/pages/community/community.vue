<template>
	<view>
		<view class="container animation-slide-left">
			<community-searchbar placeholder="搜索用户名或文本内容" left_words="问吧社区" class="searchbar"></community-searchbar>
			<view class="comments-wrapper">
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
		</view>
		<view class="bg">
			<image src="../../static/images/bgimage_1.jpg" mode=""></image>
		</view>
		<view class="add_comment" @click="addComment">
			<image src="../../static/images/plus.png" mode=""></image>
		</view>
	</view>
</template>

<script>
	import {
		mapState
	} from 'vuex'
	import parser from "@/components/jyf-parser/jyf-parser"
	import communitySearchbar from '@/components/community_searchbar/community_searchbar.vue'
	let enable_reach_bottom = true
	const row = 5
	var page = 0
	export default {
		data() {
			return {
				comments: [],
				approve_base_image: '../../static/images/approve.png',
				approve_active_image: '../../static/images/approve_active.png',
			}
		},
		components: {
			"jyf-parser": parser,
			communitySearchbar
		},
		computed: {
			...mapState(['email', 'username', 'avatarUrl', 'baseUrl', 'isLogin'])
		},
		methods: {
			blur:function(e){
				console.log(e)
			},
			addComment: function() {
				if (this.isLogin) {
					uni.navigateTo({
						url: '../addcomment/addcomment',
						success: res => {},
						fail: () => {},
						complete: () => {}
					});
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
						}
					});
				}
			},
			loadData: function() {
				uni.showLoading({
					title: 'Loading'
				})
				page++
				uni.request({
					url: this.$store.state.baseUrl + 'api/getcomments/',
					method: 'GET',
					data: {
						page: page,
						row: row,
						user_id: this.email
					},
					success: res => {
						// console.log(res)
						this.comments.push(...res.data)
						setTimeout(() => {
							uni.stopPullDownRefresh()
							uni.hideLoading()
							uni.showToast({
								title: '加载成功',
								duration: 500
							});
						})

					}
				});
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
			}
		},
		onLoad:function() {
			this.loadData()
		},
		onPullDownRefresh:function() {
			this.comments = []
			page = 0
			this.loadData()
		},
		onReachBottom:function(){
			if(!enable_reach_bottom) return
			page++
			uni.showLoading({
				title: 'Loading'
			})
			page++
			uni.request({
				url: this.$store.state.baseUrl + 'api/getcomments/',
				method: 'GET',
				data: {
					page: page,
					row: row,
					user_id: this.email
				},
				success: res => {
					// console.log(res)
					if(res.data.length===0){
						enable_reach_bottom = false
						uni.hideLoading()
						return
					}
					this.comments.push(...res.data)
					setTimeout(() => {
						uni.stopPullDownRefresh()
						uni.hideLoading()
						uni.showToast({
							title: '加载成功',
							duration: 500
						});
					})
			
				}
			});
		}
	}
</script>

<style>
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

	.container {
		display: flex;
		flex-direction: column;
	}


	
	
	.add_comment {
		position: fixed;
		z-index: 99;
		right: 30rpx;
		bottom: 200rpx;
		background-color: #00ff22;
		width: 80rpx;
		height: 80rpx;
		border-radius: 50%;
	}
	
	.add_comment image {
		width: 80rpx;
		height: 80rpx;
		border-radius: 50%;
	}
</style>
