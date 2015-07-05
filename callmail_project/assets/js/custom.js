jQuery(document).ready(function($) {


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


	$("#avatarUpload").click(function(evt){
		evt.preventBubble=true;

    // do something

			console.log("Working!!!!");

    $("#FileUpload").click();

  });

	$("#mycamera").click(function(evt){

    // do something
		evt.preventBubble=true;

			console.log("Working!!!!");

    $("#FileUpload").click();

  });





});






