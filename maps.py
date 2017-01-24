from __future__ import print_function

class Map(object):
    def __init__(self):
        self._points = []
        self._main_point = []
    def add_point(self, coordinates):
        self._points.append(coordinates)
    def add_main_point(self, coordinates):
        self._main_point.append(coordinates)
    def __str__(self):
        markersCode = "\n".join(
            [ """new google.maps.Marker({{
                position: new google.maps.LatLng({lat}, {lon}),
                map: map
                }});""".format(lat=x[0], lon=x[1]) for x in self._points
            ])
        markerMain = "\n".join(
            [ """new google.maps.Marker({{
                position: new google.maps.LatLng({lat}, {lon}),
                map: map,
                icon: 'http://maps.google.com/mapfiles/ms/icons/green.png'
                }});""".format(lat=x[0], lon=x[1]) for x in self._main_point
            ])
        return """
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=true"></script>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
            <div id="map-canvas" style="height: 100%; width: 100%"></div>
            <script type="text/javascript">
                var map;
                function show_map() {{
                    map = new google.maps.Map(document.getElementById("map-canvas"), {{
                        zoom: 18,
                        center: new google.maps.LatLng({centerLat}, {centerLon})
                    }});
                    map.addListener('click', function(e){{
                        var latitude = e.latLng.lat();
                        var longitude = e.latLng.lng();
                        if(confirm("Add Point to path: " +latitude+", " +longitude)){{
                            statLoc.updateLoc(latitude, longitude)
                        }}
                    }});
                    {markersCode}{markerMain} 
                }}   
                google.maps.event.addDomListener(window, 'load', show_map);
            </script>
        """.format(centerLat=45.3852 , centerLon=-75.6969,
                   markersCode=markersCode, markerMain=markerMain)
