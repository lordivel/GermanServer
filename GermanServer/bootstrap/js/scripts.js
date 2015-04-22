
$(document).ready(function(){$('.carousel').carousel({interval:false});

/* affix the navbar after scroll below header */
$('#nav').affix({
      offset: {
        top: $('header').height()-$('#nav').height()
      }
});	

/* highlight the top nav as scrolling occurs */
$('body').scrollspy({ target: '#nav' })

/* smooth scrolling for scroll to top */
$('.scroll-top').click(function(){
  $('body,html').animate({scrollTop:0},1000);
})

/* smooth scrolling for nav sections */
$('#nav .navbar-nav li>a').click(function(){
  var link = $(this).attr('href');
  var posi = $(link).offset().top;
  $('body,html').animate({scrollTop:posi},700);
});


/* copy loaded thumbnails into carousel */
$('.panel .img-responsive').on('load', function() {
  
}).each(function(i) {
  if(this.complete) {
  	var item = $('<div class="item"></div>');
    var itemDiv = $(this).parent('a');
    var title = $(this).parent('a').attr("title");
    
    item.attr("title",title);
  	$(itemDiv.html()).appendTo(item);
  	item.appendTo('#modalCarousel .carousel-inner'); 
    if (i==0){ // set first item active
     item.addClass('active');
    }
  }
});

/* activate the carousel */
$('#modalCarousel').carousel({interval:false});

/* change modal title when slide changes */
$('#modalCarousel').on('slid.bs.carousel', function () {
  $('.modal-title').html($(this).find('.active').attr("title"));
})

/* when clicking a thumbnail */
$('.panel-thumbnail>a').click(function(e){
  
    e.preventDefault();
    var idx = $(this).parents('.panel').parent().index();
  	var id = parseInt(idx);
  	
  	$('#myModal').modal('show'); // show the modal
    $('#modalCarousel').carousel(id); // slide carousel to selected
  	return false;
});





/* google maps */
google.maps.visualRefresh = true;

var map;
	function initialize() {
        var latitude = 50.573087,
            longitude = 7.254032,
            center = new google.maps.LatLng(latitude,longitude),
            mapOptions = {
                center: center,
                zoom: 9,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };

        var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

        setMarkers(center, map);
        google.maps.event.addListener(map, "rightclick", function(event) {
		var lat = event.latLng.lat();
		var lng = event.latLng.lng();
		// populate yor box/field with lat, lng
		alert("Lat=" + lat + "; Lng=" + lng);
		});

    }

    function setMarkers(center, map) {
        var json = (function () { 
            var json = null; 
            $.ajax({ 
                'async': false, 
                'global': false, 
                'url': "http://localhost:5000/clipcultexperiences/api/v1.0/experiences", 
                'dataType': "json", 
                'success': function (data) {
                     json = data['experiences']; 
                 }
            });
            return json;
        })();


        //loop between each of the json elements
        for (var i = 0, length = json.length; i < length; i++) {
            var data = json[i],
            latLng = new google.maps.LatLng(data.lat, data.lng); 

            // Creating a marker and putting it on the map
            var marker = new google.maps.Marker({
				position: latLng,
                map: map,
                title: data.title
                });
                infoBox(map, marker, data);

        }

    }

    function infoBox(map, marker, data) {
        var infoWindow = new google.maps.InfoWindow();
        // Attaching a click event to the current marker
        google.maps.event.addListener(marker, "click", function(e) {
			
		var contentString = '<div id="content">'+
		'<div id="siteNotice">'+
		'</div>'+
		'<h1 id="firstHeading" class="firstHeading">' + data.title + '</h1>'+
		'<div id="bodyContent">'+
		'<p><b>ID:</b> ' + data.id +
		'<p><b>Description:</b> ' + data.desc +
		'<iframe id="ytplayer" type="text/html" width="640" height="390"' +
		'src="http://www.youtube.com/embed/M7lc1UVf-VE?autoplay=1&origin=http://example.com"' +
		'frameborder="0"/>' +
		'</div>'+
		'</div>';
		infoWindow.setContent(contentString);
        infoWindow.open(map, marker);
        });

        // Creating a closure to retain the correct data 
        // Note how I pass the current data in the loop into the closure (marker, data)
        (function(marker, data) {
          // Attaching a click event to the current marker
          google.maps.event.addListener(marker, "click", function(e) {
			
			var contentString = '<div id="content">'+
			'<div id="siteNotice">'+
			'</div>'+
			'<h1 id="firstHeading" class="firstHeading">' + data.title + '</h1>'+
			'<div id="bodyContent">'+
			'<p><b>ID:</b> ' + data.id +
			'<p><b>Description:</b> ' + data.desc +
			'<iframe id="ytplayer" type="text/html" width="640" height="390"' +
			'src="http://www.youtube.com/embed/' + data.link +'?autoplay=1&origin=http://example.com"' +
			'frameborder="0"/>'+
			'</div>'+
			'</div>';
			
            infoWindow.setContent(contentString);
            infoWindow.open(map, marker);
          });
        })(marker, data);
    }

   google.maps.event.addDomListener(window, 'load', initialize);

/* end google maps */


});
