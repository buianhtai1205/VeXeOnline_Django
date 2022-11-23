/*	var ws = new WebSocket("ws://localhost:8080/BanVeXe/checkGhe");
	ws.onmessage = function process(message) {
		var json = JSON.parse(message.data);
		if (json.check != null)
			if (json.check.indexOf("true") != -1)
				choose("#" + json.ghe);
			else
				unchoose("#" + json.ghe);
				
		if (json.set != null)
			setSeatOdered("#" +json.set);
		if (json.unset != null)
			unsetSeatOdered("#" +json.unset);
	};
	function sendMessage(el) {
		ws.send(el.attr("id"));
	}*/

function scroll(el,time) {
		$('body,html').animate({
			scrollTop: 0
		}, 100);
		$('body,html').animate({
			scrollTop: $(el).offset().top
		}, time);
		return false;
	}
function setDefaut(chuyen) {
	$("."+chuyen).slideUp(0);
	$("."+chuyen).html("");
}