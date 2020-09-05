<template>
	<view class="container">
		<back-top v-show="is_show" @click.native="bakToTop"></back-top>
		<view class="header">
			<text class="first">以下是对"<text class="value">{{value}}</text>"的搜索结果:\n</text>
			<text class="result">共计<text class="result_num">{{count}}</text>条搜索结果</text>
		</view>
		<view class="body">
			<view class="article-warper" v-if="!is_null">
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
			<view class="sorry" v-else>
				<text>很抱歉，未查询到任何相关文章</text>
			</view>
		</view>
		<view class="bg">
			<image src="../../static/images/bgimage_1.jpg" mode=""></image>
		</view>
	</view>

</template>

<script>
	import backTop from '@/components/back-top/back-top.vue'
	export default {
		data() {
			return {
				value: '中国',
				articles: [],
				is_null: false,
				is_show: false,
				count: 0
			}
		},
		components: {
			backTop
		},
		methods: {
			bakToTop: function() {
				uni.pageScrollTo({
					scrollTop: 0,
					duration: 200
				})
			},
			getSearchResult: function(value) {
				uni.showLoading({
					title: 'Loading...',
					mask: false
				});
				uni.request({
					url: this.$store.state.baseUrl + 'api/search/',
					method: 'GET',
					data: {
						value: value
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
							this.articles = res.data
						}
					},
				});
			},
			gotoDeatil(id) {
				// console.log(id)
				wx.navigateTo({
					url: '../detail/detail?id=' + id,
				})
			},
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

	.article text {
		color: #F1F1F1;
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
