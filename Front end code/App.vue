<script>
export default {
	onLaunch: function() {
		console.log('App Launch');
	},
	onShow: function() {
		console.log('App Show');
	},
	onHide: function() {
		console.log('App Hide');
	}
};
</script>

<style>
	@import url("static/css/main.css");
	@import url("static/css/animation.css");
/* 解决头条小程序组件内引入字体不生效的问题 */
/* #ifdef MP-TOUTIAO */
@font-face {
	font-family: uniicons;
	src: url('/static/uni.ttf');
}
/* #endif */

	.article-warper{
		display: flex;
		flex-direction: column;
	}
	.article{
		display: flex;
		flex-direction: row;
		margin: 2.5rpx 5rpx;
		min-height: 100rpx;
		justify-content: space-between;
		align-items: center;
	}
	.preview{
		height: 180rpx;
		width: 250rpx;
		margin: 10rpx 10rpx;
	}

	.preview image{
		width: 100%;
	}
	
	.article-info{
		display: flex;
		flex-direction: column;
		justify-content: space-around;
	}
	.article-info .title{
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 2;
		overflow: hidden;
		text-overflow: ellipsis;
		font-size: 36rpx;
		line-height: 38rpx;
		font-weight: bold;
		font-family: monospace;
	}

	.article-info .desc{
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp:2;
		overflow: hidden;
		text-overflow: ellipsis;
		line-height: 32rpx;
		font-size: 30rpx;
		font-weight: 300;
	}
	.bottom-container{
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		margin-right: 10rpx;
		color: #999;
		font-size: 28rpx;
	}
	
	.bg{
		z-index: -99;
		position: fixed;
		top: 0;
		right: 0;
		left: 0;
	}
	.bg image{
		width: 100%;
		height: 100vh;
	}
	
	
	.comments-wrapper {
		display: flex;
		flex-direction: column;
		color: #eee;
	}
	
	.comment {
		margin: 10rpx 0;
		margin-bottom: 20rpx;
	}
	
	.comment-header {
		display: flex;
		flex-direction: row;
		padding: 12rpx 10rpx;
		box-shadow: #ccc 0 5rpx;
	}
	
	.username-and-time {
		display: flex;
		flex-direction: column;
		margin-left: 20rpx;
	}
	
	.username {
		font-size: 40rpx;
		margin-bottom: 4rpx;
	}
	
	.date {
		font-size: 26rpx;
	}
	
	.avatar {
		width: 80rpx;
		height: 80rpx;
		border-radius: 50%;
	}
	
	
	.comment-info {
		display: flex;
		flex-direction: column;
		padding: 12rpx 10rpx;
	}
	
	.content{
		font-size: 35rpx;
	}
	
	.comment-footer {
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
		padding: 12rpx 10rpx;
	}
	
	.comment-footer image {
		height: 35rpx;
		width: 35rpx;
		margin-right: 20rpx;
	}
	
	.comment-bar {
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-around;
	}
	
	.comment-bar input {
		background-color: #333;
		height: 40rpx;
		border-radius: 20rpx;
		margin: 12rpx 0rpx;
		width: 85%;
		font-size: 28rpx;
		line-height: 30rpx;
	}
	
	.comment-bar button {
		height: 40rpx;
		border-radius: 0rpx;
		font-size: 25rpx;
		line-height: 40rpx;
		font-weight: bold;
		background-color: #007AFF;
		color: #eee;
	}
	
	
	
	.approved_users {
		display: flex;
		flex-direction: column;
	}
	
	.approved_usernames {
		display: flex;
		flex-direction: row;
		color: #fff;
	}
	
	.reply image {
		height: 30rpx;
		width: 30rpx;
		margin-right: 20rpx;
	}
	
	.replies{
		display: flex;
		flex-direction: column;
	}
	
	.reply{
		display: flex;
		flex-direction: row;
		justify-content: space-between;
	}
	
	.approved_name{
		margin: 0rpx 10rpx;
		color: #ffff00;
	}
	
	.usernames{
		word-break: break-all;
	}


</style>
