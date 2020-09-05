<template>
	<view class="container">
		<image class="back" src="/static/images/backtop.png" mode=""></image>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				
			};
		}
	}
</script>

<style>
	.container{
		position: fixed;
		z-index: 8;
		width: 80rpx;
		height: 80rpx;
		bottom: 160rpx;
		right: 40rpx;
		border-radius: 50%;
		border: solid 5rpx #00eeee;
		background-color: #00EEEE;
		align-items: center;
	}
	.back{
		z-index: 9;
		width: 60rpx;
		height: 60rpx;
	}

</style>
