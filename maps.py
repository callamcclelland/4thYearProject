from __future__ import print_function

class Map(object):
    def __str__(self):
        
        """
        Creates the map
        
        Creates the map, with the javascript functions neccessary to pass data to and from the
        GUI
        
        Parameters
        ----------
        
        Returns
        String
            A String which is all text for the HTML file map.
        
        
        """
        return """
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=true"></script>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
            <div id="map-canvas" style="height: 100%; width: 100%"></div>
            <script type="text/javascript">
                var map;
                var pathComplete = 0;
                var markers = [];
                var currMarker = [];
                function show_map() {{
                    map = new google.maps.Map(document.getElementById("map-canvas"), {{
                        zoom: 18,
                        center: new google.maps.LatLng({centerLat}, {centerLon})
                    }});
                    map.addListener('click', function(e){{
                        if(!pathComplete){{
                            var latitude = e.latLng.lat();
                            var longitude = e.latLng.lng();
                            statLoc.addPath(latitude, longitude)
                            var marker = new google.maps.Marker({{
                                position: e.latLng,
                                map: map,
                                icon: 'http://maps.google.com/mapfiles/ms/icons/green.png'                       
                             }});
                            marker.addListener("dblclick", function() {{
                                if(!pathComplete){{
                                    marker.setMap(null);
                                    statLoc.removePoint(latitude, longitude)  
                                }}  
                            }});
                        }}
                    }});
                }}   
                function addMarker(lat, lng){{
                        var myLatLng = new google.maps.LatLng(lat,lng);
                        var beachMarker = new google.maps.Marker({{position: myLatLng,
                                                                    map: map,
                                                                    icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
                                                                    }});
                        markers.push(beachMarker);
                    }}
                function addCurrMarker(lat, lng){{
                        var j;
                        for(j=0;j<currMarker.length;j++){{
                            currMarker[j].setMap(null);
                        }}
                        var myLatLng = new google.maps.LatLng(lat,lng);
                        var beachMarker = new google.maps.Marker({{position: myLatLng,
                                                                    map: map,
                                                                    icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
                                                                    }});
                        currMarker.push(beachMarker);
                    }}
                function setPathComplete(){{
                        pathComplete = !pathComplete;
                }}
                function removeMarker(lat, lng){{
                        var removeLatLng = new google.maps.LatLng(lat,lng);
                        for(i=0;i<markers.length;i++){{
                            if(markers[i].getPosition().equals(removeLatLng)){{
                                markers[i].setMap(null);
                            }}
                        }}
                    }}
                function setCenter(lat, lng){{
                        if(lat<-90 || lat>90 || lng < -180 || lng >180){{
                            alert("Not valid Latitude and/or Longitude")
                        }}else{{
                            map.setCenter(new google.maps.LatLng(lat, lng));
                            map.setZoom(18);
                        }}
                }}
                google.maps.event.addDomListener(window, 'load', show_map);
            </script>
        """.format(centerLat=45.3852 , centerLon=-75.6969)
