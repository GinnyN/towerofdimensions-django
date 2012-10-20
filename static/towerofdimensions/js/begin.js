$(document).on("ready", ready);

function ready(){
	margin = parseInt($("#header-background").css("margin-top").split("px")[0]);
	padding = parseInt($("#header-background").css("padding-top").split("px")[0]);
	marginFooter = parseInt($("footer").css("margin-top").split("px")[0]);
	marginAside = parseInt($("#content").css("margin-top").split("px")[0]);
	$("#content").height($(document).height() - $("#header-background").height() - (2 * margin) - (2 * padding) - $("footer").height() - (2 * marginFooter) - (marginAside));

	$("nav ul li a").hover(function(){
			$(this).addClass("hover");
		}, 
		function(){
			$(this).removeClass("hover")
		});
	$("nav ul li a").on("click", clickMenu);

	$("#menu-mercenaries").on("click", mercenariesSetup)
}

function clickMenu(){
	$("nav ul li a").removeClass("active");
	$(this).addClass("active");
}