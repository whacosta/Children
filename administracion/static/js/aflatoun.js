(function($) {
  "use strict";
  
  var mylat = -12.043333;
  var mylng = -77.028333;



  //MAP WITH MARKER
  var markerMap = new GMaps({
    div: '#map-marker',
    lat: mylat,
    lng: mylng
  });

  markerMap.addMarker({
    lat: mylat,
    lng: mylng,
    title: 'Lima'
  });
})(jQuery);