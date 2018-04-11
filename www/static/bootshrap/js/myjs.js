function getURL(data){
	$(".jumbotron").css('background-image','url(' + data.url + ')');
	$(".jumbotron").css('background-size','cover');
	
}
function setBgPic() {
	var
		js = document.createElement('script'),
		head =  $('head')[0];
	js.src = 'http://123.206.115.58/api/get_bing_photo?callback=getURL';
	head.appendChild(js);
}
function setJoke(data){
	$("#firstjoke").empty().append(data.items[1]);
	$("#secondjoke").empty().append(data.items[2]);
	$("#thirdjoke").empty().append(data.items[3])
}
function getJoke() {
	var
		js = document.createElement('script'),
		head =  $('head')[0];
	js.src = 'http://123.206.115.58/api/get_qiubai?callback=setJoke&page='+Math.floor(Math.random()*40);

	head.appendChild(js);
}
