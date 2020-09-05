<template>
	<view class="container">
		<index-searchbar class="searchbar"></index-searchbar>
		<back-top v-show="is_backtop_show" @click.native="backToTop"></back-top>
		<view class="header animation-fade animation-slide-top">
		</view>
		<view class="body">
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
	</view>
</template>

<script>
	import {
		mapState
	} from 'vuex'
	import backTop from '../../components/back-top/back-top.vue'
	import indexSearchbar from '../../components/index-searchbar/index-searchbar.vue'
	var page = 0
	const row = 10
	export default {
		data() {
			return {
				articles: [],
				is_backtop_show: false
			}
		},
		components: {
			backTop,
			indexSearchbar
		},
		methods: {
			//收藏与点赞数据变化
			getChangedNumber(number) {
				if (number >= 10000) {
					return (parseFloat(number) / 1000).toFixed(1) + 'K'
				}
				return number + ''
			},
			gotoDeatil(id) {
				// console.log(id)
				wx.navigateTo({
					url: '../detail/detail?id=' + id,
				})
			},
			backToTop() {
				console.log('----')
				uni.pageScrollTo({
					duration: 500,
					scrollTop: 0
				})
			},
			loadData:function(){
				page++
				uni.showLoading({
					title: 'Loading...',
				})
				uni.request({
					url: this.baseUrl + 'data/index/',
					method: 'GET',
					data: {
						page: page
					},
					success: res => {
						// console.log(res)
						for (let item of res.data) {
							item.browse_num = this.getChangedNumber(item.browse_num)
						}
						this.articles = res.data
						setTimeout(() => {
							uni.hideLoading({
								success: res => {
									uni.showToast({
										title: '加载成功',
										duration: 300
									})
								}
							})
							uni.stopPullDownRefresh()
						},750)
						
					},
					fail: err => {
						console.log(err)
					},
					complete: () => {}
				});
			}
		},
		computed: {
			...mapState(['baseUrl'])
		},
		//加载中函数
		onLoad() {
			this.loadData()
		},
		onReachBottom: function() {
			page++
			uni.showLoading({
				title: 'Loading...',
			})
			uni.request({
				url: this.baseUrl + 'data/index/',
				method: 'GET',
				data: {
					page: page
				},
				success: res => {
					let old_article = this.articles
					let new_article = res.data
					for (let item of new_article) {
						item.browse_num = this.getChangedNumber(item.browse_num)
					}
					let temp_article = old_article.concat(new_article)
					this.articles = temp_article
					setTimeout(() => {
						uni.hideLoading({
							success: (res) => {
								uni.showToast({
									title: '加载成功',
									duration: 300
								})
							},
						})
					}, 200)
				},
				fail: () => {},
				complete: () => {}
			})
		},
		onPageScroll:function(e) {
			if (e.scrollTop >= 1500) {
				this.is_backtop_show = true
			} else {
				this.is_backtop_show = false
			}
		},
		onPullDownRefresh: function() {
			this.loadData()
		}
	}
</script>

<style>
	.container {
		display: flex;
		flex-direction: column;
	}

/* 	.header {
		text-align: center;
		color: #0000ff;
		font-size: 75rpx;
		font-weight: bold;
		font-family: '华文楷体';
	} */

	.body {
		display: flex;
		flex-direction: column;
		margin-top: 75rpx;
	}

	.author {
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 1;
		word-break: break-all;
		overflow: hidden;
		width: 300rpx;
		text-overflow: ellipsis;
	}
	.searchbar{
		position: fixed;
		right: 0;
		left: 0;
		z-index: 999;
		background-color: #f1f1f2;
	}
</style>
