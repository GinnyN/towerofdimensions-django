function mercenariesSetup(){
	$("#loading").show();
	$.ajax({
		type : 'POST',
		data: {csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()},
		dataType: 'html',
		url : $("#menu-mercenaries-url").attr("value"),
		success: function(response){
			$("#main").html(response).show();
			$("#loading").hide();
			$(".mercenary-resume").on("click",openFullView)
		}
	});
}

function openFullView(){
	$(".mercenary-list").addClass("mercenary-list-aside");
	$(".mercenary-full-view").remove();

	id = $(this).attr("class").split("mercenary-resume ")[1];
	$("#loading").show();
	$.ajax({
		type : 'POST',
		data: {csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()},
		dataType: 'html',
		url : $("#menu-mercenaries-url").attr("value")+id+"/",
		success: function(response){
			$("#main").append(response);
			$("#loading").hide();
		}
	});
}