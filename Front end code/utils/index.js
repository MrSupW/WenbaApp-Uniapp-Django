const valideEmail = function(string) {
	var re = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/
	if (re.test(string)) {
		return true
	} else {
		return false
	}
}

const blobToBase64 = function(blob) {
	return new Promise((resolve, reject) => {
		const fileReader = new FileReader();
		fileReader.onload = (e) => {
			resolve(e.target.result);
		};
		// readAsDataURL
		fileReader.readAsDataURL(blob);
		fileReader.onerror = () => {
			reject(new Error('文件流异常'));
		};
	});
}
const urlTobase64 = function(url) {
	var toBase64Url;
	uni.request({
		url: url,
		method: 'GET',
		responseType: 'arraybuffer',
		success: res => {
			let base64 = uni.arrayBufferToBase64(res.data); //把arraybuffer转成base64
			toBase64Url = 'data:image/jpeg;base64,' + base64; //不加上这串字符，在页面无法显示
			return toBase64Url
		}
	});
}
export {
	valideEmail,
	blobToBase64,
	urlTobase64
}
