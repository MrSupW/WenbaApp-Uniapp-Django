<template>
	<view>
		<view class="container">
			<view class="title">
				<text>{{left_words}}</text>
			</view>
			<view class="searchBar-wrapper">
				<uni-search-bar :placeholder="placeholder" :radius="150" class="searchBar" @confirm="confirm"></uni-search-bar>
			</view>
		</view>
	</view>
</template>

<script>
	import uniSearchBar from '../uni-search-bar/uni-search-bar.vue'
	export default {
		data() {
			return {

			};
		},
		props: {
			left_words: {
				type: String,
				default: '问吧精选'
			},
			placeholder:{
				type:String,
				default:'搜索文章作者或标题'
			}
		},
		components: {
			uniSearchBar
		},
		methods: {
			confirm: function(e) {
				if (e.value === '') return;
				uni.navigateTo({
					url: '/pages/search/search?value=' + e.value,
				});
			}
		}
	}
</script>

<style>
	.container {
		display: flex;
		flex-direction: row;
		align-items: center;
		height: 75rpx;
		width: 100%;
		justify-content: space-around;
	}

	.title {
		line-height: 75rpx;
		font-size: 43.5rpx;
		color: #052AFC;
		font-family: '幼圆';
		font-weight: bold;
		border-radius: 5rpx;
		width: 175rpx;
		text-align: center;
	}

	.searchBar {
		width: 565rpx;
		height: 65rpx;
		position: relative;
		bottom: 20rpx;
	}

	.button {}
</style>
