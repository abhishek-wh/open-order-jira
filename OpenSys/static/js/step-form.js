//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches
// form1 start
$("#msform .next").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs = $(this).parent();
	next_fs = $(this).parent().next();
	
	//activate next step on progressbar using the index of next_fs
	$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("inProgress");
	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("inProgress").addClass("checked");
	// .removeClass('pull-right').addClass('yournewClass')
	
	//show the next fieldset
	next_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			// scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			//left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
        // 'transform': 'scale('+scale+')',
        'position': 'relative'
      });
			next_fs.css({'left': left, 'opacity': opacity});
		}, 
		duration: 200, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$("#msform .previous").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs = $(this).parent();
	previous_fs = $(this).parent().prev();
	
	//de-activate current step on progressbar
	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("inProgress");
	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("inProgress").removeClass("checked");
	
	//show the previous fieldset
	previous_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale previous_fs from 80% to 100%
			//scale = 0.8 + (1 - now) * 0.2;
			//2. take current_fs to the right(50%) - from 0%
			//left = ((1-now) * 50)+"%";
			//3. increase opacity of previous_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({'left': left});
			//previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
			previous_fs.css({ 'opacity': opacity});
		}, 
		duration: 200, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".submit").click(function(){
	return false;
})

// form1 end


// form2 start
var current_fs2, next_fs2, previous_fs2; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches
$("#msform2 .previous").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs2 = $(this).parent();
	previous_fs2 = $(this).parent().prev();
	
	//de-activate current step on progressbar
	$("#progressbar1 li").eq($("fieldset").index(current_fs2)).removeClass("inProgress");
	$("#progressbar1 li").eq($("fieldset").index(current_fs2)).removeClass("inProgress").removeClass("checked");
	
	//show the previous fieldset
	previous_fs2.show(); 
	//hide the current fieldset with style
	current_fs2.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale previous_fs from 80% to 100%
			//scale = 0.8 + (1 - now) * 0.2;
			//2. take current_fs to the right(50%) - from 0%
			//left = ((1-now) * 50)+"%";
			//3. increase opacity of previous_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs2.css({'left': left});
			//previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
			previous_fs2.css({ 'opacity': opacity});
		}, 
		duration: 200, 
		complete: function(){
			current_fs2.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
})
$("#msform2 .next").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs2 = $(this).parent();
	next_fs2 = $(this).parent().next();
	
	//activate next step on progressbar using the index of next_fs
	$("#progressbar1 li").eq($("fieldset").index(next_fs2)).addClass("inProgress");
	$("#progressbar1 li").eq($("fieldset").index(current_fs2)).removeClass("inProgress").addClass("checked");
	// .removeClass('pull-right').addClass('yournewClass')
	
	//show the next fieldset
	next_fs2.show(); 
	//hide the current fieldset with style
	current_fs2.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			// scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			//left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs2.css({
        // 'transform': 'scale('+scale+')',
        'position': 'relative'
      });
			next_fs2.css({'left': left, 'opacity': opacity});
		}, 
		duration: 200, 
		complete: function(){
			current_fs2.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".submit").click(function(){
	return false;
})

// form2 end




// nextstep form

//jQuery time
var current_fs1, next_fs1, previous_fs1; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches
// form3 start
$("#msform1 .next").click(function(){
	//debugger;
	if(animating) return false;
	animating = true;
	
	current_fs1 = $(this).parent();
	next_fs1 = $(this).parent().next();
	
	//activate next step on progressbar using the index of next_fs
	$("#progressbar1 li").eq($("fieldset").index(next_fs1)).addClass("inProgress");
	$("#progressbar1 li").eq($("fieldset").index(current_fs1)).removeClass("inProgress").addClass("checked");
	// .removeClass('pull-right').addClass('yournewClass')
	
	//show the next fieldset
	next_fs1.show(); 
	//hide the current fieldset with style
	current_fs1.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			// scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			//left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs1.css({
        //'transform': 'scale('+scale+')',
        'position': 'relative'
      });
			next_fs1.css({'left': left, 'opacity': opacity});
		}, 
		duration: 200, 
		complete: function(){
			current_fs1.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$("#msform1 .previous").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs1 = $(this).parent();
	previous_fs1 = $(this).parent().prev();
	
	//de-activate current step on progressbar
	$("#progressbar1 li").eq($("fieldset").index(current_fs1)).removeClass("inProgress");
	$("#progressbar1 li").eq($("fieldset").index(current_fs1)).removeClass("inProgress").removeClass("checked");
	
	//show the previous fieldset
	previous_fs1.show(); 
	//hide the current fieldset with style
	current_fs1.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale previous_fs from 80% to 100%
			//scale = 0.8 + (1 - now) * 0.2;
			//2. take current_fs to the right(50%) - from 0%
			//left = ((1-now) * 50)+"%";
			//3. increase opacity of previous_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs1.css({'left': left});
			previous_fs1.css({ 'opacity': opacity});
		}, 
		duration: 200, 
		complete: function(){
			current_fs1.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".submit").click(function(){
	return false;
})

// form3 end