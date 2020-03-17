$(document).ready(function(){

    $('.menu_toggle').click(function(){
		$(this).toggleClass('menuActive');
		//$('.admin-menu').toggleClass('opened');
		//$('.overlay_div').toggleClass('overlay_active');
		//$('body').toggleClass('overflow');
	});

 $(".menu_close").click(function(){
    $("#navbarNavDropdown").removeClass('show');
  });
 $(".menu-icon").click(function(){
  if($('#menu-btn').is(':checked')){
$('#menu-btn').prop('checked', false);
  }else{
  $('#menu-btn').prop('checked', true);
}
    $(".header .menu").toggleClass('active');
    $(".navBar").toggleClass('navbarNavDropdown');
     return false;
  });


$('input').focus(function(){
  $(this).parents('.form-group').addClass('focused');
});

$('input').blur(function(){
  var inputValue = $(this).val();
  if ( inputValue == "" ) {
    $(this).removeClass('filled');
    $(this).parents('.form-group').removeClass('focused');  
  } else {
    $(this).addClass('filled');
  }
})  

 $(".mbldisplay").click(function(){
 $(".mbldisplay").toggleClass('change');
 $('.css-jdgyoy-PrimaryItemsList').toggleClass('menuActive_n');

 }); 



 
 
 }); 


$(document).ready(function() {
  $('#example').DataTable();
} );