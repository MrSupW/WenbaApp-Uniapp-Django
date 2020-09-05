import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
	state:{
		isLogin:false,
		email: '',
		username:'',
		avatarUrl:'/static/images/base_avatar.png',
		// baseUrl:'http://47.93.219.145:8888/wenba_back/'
		baseUrl:'http://127.0.0.1:8000/wenba_back/'
	}
})
export default store