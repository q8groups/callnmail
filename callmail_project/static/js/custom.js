jQuery(document).ready(function($) {

if ( $( "#login" ).length ) {
	$('.fuzzOptionsList.login').fuzzyDropdown({
		mainContainer: '.county_search_login',
		arrowUpClass: 'fuzzArrowUp',
		selectedClass: 'selected',
		enableBrowserDefaultScroll: true
	});

	$('.fuzzOptionsList.signup').fuzzyDropdown({
		mainContainer: '.county_search_signup',
		arrowUpClass: 'fuzzArrowUp',
		selectedClass: 'selected',
		enableBrowserDefaultScroll: true
	});
}

	$("#avatarUpload").click(function(evt){
		evt.s;

    // do something

			console.log("Working!!!!");

    $("#FileUpload").click();

  });

//	$('#id_age').datetimepicker({
// timepicker:false,
//});
	$('#id_age').datepicker();



});






