function set(item, idchuyen, chitietve) {
	$(item).mouseleave(function() {
		unselected($(this));
	});
	$(item).mouseenter(function() {
		selected($(this));
	});
	$(item).click(function() {
		choose($(this), idchuyen, chitietve);
	});
}

function selected(el) {
	var newSrc = "../assets/user/images/ghe2.png";
	$(el).attr("src", newSrc);
}
function unselected(el) {
	var newSrc = "../assets/user/images/ghe1.png";
	$(el).attr("src", newSrc);
}
function choose(el, id, chitietve) {
	var idGhe = $(el).attr("id");
	var idChuyen = $(id).val(); 
	$
			.get(
					'/themghe',
					{
						idChuyen : idChuyen,
						idGhe : idGhe
					},
					function(responseText) {
						if (responseText.indexOf("ok") != -1) {
							$(chitietve )
									.load("/views/chitietvexe.jsp?chuyen=" + idChuyen);
							$(el).unbind("mouseenter");
							$(el).unbind("mouseleave");
							$(el).off("click");
							$(el).click(function() {
								unchoose($(el), id, chitietve);
							});
							selected($(el));
							return;
						} else {
							if (responseText.indexOf("limited-notlogin") != -1) {
								alert("Quý khách chưa đăng nhập nên chỉ được chọn tối đa 2 vé! Vui lòng đăng nhập để được chon nhiều hơn!");
							} else {
								alert("Quý khách chỉ được chọn tối đa 5 ghế!");
							}
						}
						unselected($(el));
					});

}



function unchoose(el, id, chitietve) {
	var idChuyen = $(id).val();
	var idGhe = $(el).attr("id");
	$.get('/huyghe', {
		idChuyen : idChuyen,
		idGhe : idGhe
	}, function(responseText) {
		if (responseText.indexOf("ok") != -1) {
			$(chitietve ).load("/views/chitietvexe.jsp?chuyen=" + idChuyen);
			//
			$(el).off("click");
			$(el).click(function() {
				choose($(this), id, chitietve);
			});
			unselected($(el));
			$(el).mouseenter(function() {
				selected($(el));
			});
			$(el).mouseleave(function() {
				unselected($(el));
			});
		} else {
			selected($(el));
		}
	});

}

function setSeatOdered(el) {
	var newSrc = "../assets/user/images/ghe3.png";
	$(el).attr("src", newSrc);
	$(el).unbind("mouseenter");
	$(el).unbind("mouseleave");
	$(el).unbind("click");
}
function unsetSeatOdered(el) {
	var newSrc = "../assets/user/images/ghe1.png";
	$(el).attr("src", newSrc);
	$(el).mouseleave(function() {
		unselected($(this));
	});
	$(el).mouseenter(function() {
		selected($(this));
	});
	$(el).click(function() {
	});
}

