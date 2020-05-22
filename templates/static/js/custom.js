
var block_show = false;
 
function scrollTracking(){
	if (block_show) {
		return false;
	}
 
	var wt = $(window).scrollTop();
	var wh = $(window).height();
	var et = $('.count').offset().top;
	var eh = $('.count').outerHeight();
	var dh = $(document).height();   
 
	if (wt + wh >= et || wh + wt == dh || eh + et < wh){
		block_show = true;
		
		// Код анимации
    $('.count').css('opacity', '1');
    $('.count').spincrement({
        thousandSeparator: "",
        duration: 6000
    });
} else {
    // если не виден
    $('.count').css({ 'opacity': '0' });
}
}

$(window).scroll(function(){
	scrollTracking();
});
	
$(document).ready(function(){ 
	scrollTracking();
});