//自动生成标签切换
$(document).ready(function () {
$(".tabcon-main > div").addClass("tabcon");
$('.tab-menu li').click(function(){
	$(this).addClass("active").siblings().removeClass();
	$(".tabcon-main > div").hide().eq($('.tab-menu li').index(this)).addClass( "tabcon" + $('.tab-menu li').index(this)).show();
});

}); 
 