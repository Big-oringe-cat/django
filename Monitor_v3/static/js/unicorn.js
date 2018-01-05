/**
**/
function resetHeight(){
	var height = $("body").height();
	$("#content").height(height-53);
}

$(window).resize(function(){
	resetHeight();
})

$(document).ready(function(){	
	
	// === Sidebar navigation === //
	
	$('.submenu > a').click(function(e)
	{
		e.preventDefault();
		var submenu = $(this).siblings('ul');
		var li = $(this).parents('li');
		var submenus = $('#sidebar li.submenu ul');
		var submenus_parents = $('#sidebar li.submenu');
		if(li.hasClass('open'))
		{
			if( ( ($(window).width() < 768) && ($(window).width() > 479) ) || $("#sidebar > ul").hasClass("toggler") ) {
				submenu.fadeOut(250);				
			} else {
				submenu.slideUp();
			}
			
			li.removeClass('open');
		} else 
		{
			if( ( ($(window).width() < 768) && ($(window).width() > 479) ) || $("#sidebar > ul").hasClass("toggler") ) {
				submenus.fadeOut(250);			
				submenu.fadeIn(250);				
			} else {
				submenus.slideUp();	
				submenu.slideDown();
			}
			submenus_parents.removeClass('open');		
			li.addClass('open');	
		}
	});
	
	var ul = $('#sidebar > ul');
	
	$('#sidebar > a').click(function(e)
	{
		e.preventDefault();
		var sidebar = $('#sidebar');
		if(sidebar.hasClass('open'))
		{
			sidebar.removeClass('open');
			ul.slideUp(250);
		} else 
		{
			sidebar.addClass('open');
			ul.slideDown(250);
		}
	});
	
	// === Resize window related === //
	$(window).resize(function()
	{
		if($(window).width() > 479)
		{
			ul.css({'display':'block'});	
			$('#content-header .btn-group').css({width:'auto'});		
		}
		if($(window).width() < 479)
		{
			ul.css({'display':'none'});
			fix_position();
		}
		if($(window).width() > 768)
		{
			$('#user-nav > ul').css({width:'auto',margin:'0'});
            $('#content-header .btn-group').css({width:'auto'});
		}
	});
	
	if($(window).width() < 468)
	{
		ul.css({'display':'none'});
		fix_position();
	}
	if($(window).width() > 479)
	{
	   $('#content-header .btn-group').css({width:'auto'});
		ul.css({'display':'block'});
	}
	
	// === Tooltips === //
	$('.tip').tooltip();	
	$('.tip-left').tooltip({ placement: 'left' });	
	$('.tip-right').tooltip({ placement: 'right' });	
	$('.tip-top').tooltip({ placement: 'top' });	
	$('.tip-bottom').tooltip({ placement: 'bottom' });
	
	// === Fixes the position of buttons group in content header and top user navigation === //
	function fix_position()
	{
		var uwidth = $('#user-nav > ul').width();
		$('#user-nav > ul').css({width:uwidth,'margin-left':'-' + uwidth / 2 + 'px'});        
        
	}
	
	//toggler sidebar
	resetHeight();
	$(".sidebar-toggler").click(function(){
		if ($("#sidebar > ul").hasClass("toggler"))
		{
			$("#sidebar, #sidebar > ul").width(220);
			$("#sidebar > ul").removeClass("toggler");
			$("#sidebar > ul > li > a > span").show();
			$("#content").removeAttr("style");
			$(".sidebar-toggler").removeAttr("style");
		} else {
			$("#sidebar, #sidebar > ul").width(43);
			$("#sidebar > ul").addClass("toggler");
			$("#sidebar > ul > li > a > span").hide();
			$("#content").css("margin-left","43px");
			$(".sidebar-toggler").css("margin","3px");	
		}
	});

	// === Sidebar === //
	$("#sidebar > ul > li").each(function(){
		$(this).click(function() {
			$(this).siblings("li").removeClass("active");
			$(this).addClass("active");
		});
	});
});