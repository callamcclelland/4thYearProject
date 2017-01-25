from __future__ import print_function

class Map(object):
    def __str__(self):
        return """
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=true"></script>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
            <div id="map-canvas" style="height: 100%; width: 100%"></div>
            <script type="text/javascript">
                var map;
                var initialized = 0;
                function show_map() {{
                    map = new google.maps.Map(document.getElementById("map-canvas"), {{
                        zoom: 18,
                        center: new google.maps.LatLng({centerLat}, {centerLon})
                    }});
                    map.addListener('click', function(e){{
                        if(!initialized){{
                            var latitude = e.latLng.lat();
                            var longitude = e.latLng.lng();
                            if(confirm("Add Point to path: " +latitude+", " +longitude)){{
                                statLoc.addPath(latitude, longitude)
                                if(confirm("Finished Path?")){{
                                    initialized = 1;
                                }}
                                var marker = new google.maps.Marker({{
                                    position: e.latLng,
                                    map: map,
                                    icon: 'http://maps.google.com/mapfiles/ms/icons/green.png'
                                    
                                }});
                            }}
                        }}
                    }});
                }}   
                function addMarker(lat, lng){{
                        var myLatLng = new google.maps.LatLng(lat,lng);
                        var beachMarker = new google.maps.Marker({{position: myLatLng,
                                                                    map: map
                                                                    }});
                    }}
                google.maps.event.addDomListener(window, 'load', show_map);
            </script>
        """.format(centerLat=45.3852 , centerLon=-75.6969)
