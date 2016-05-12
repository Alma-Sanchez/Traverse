$(document).ready(function(){
	$vcenter = $('#vcenter');
  $vcenter.css({
        'position': 'absolute',
        'top': '56%',
        'left': '50%',
        'margin-left': -$vcenter.width()/16,
        'margin-top': -$('#vcenter').outerHeight()/2
    });
  // $vcenter.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) + $(window).scrollTop()) + "px");	
	
});

// jQuery.fn.verticalAlignScreen = function (){
//   return this
//     .css("position", "absolute")
//     .css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) + $(window).scrollTop()) + "px");
// };