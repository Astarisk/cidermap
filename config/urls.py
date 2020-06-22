"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from config import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, register_converter

from myapi import views as api_views
from map import views as map_views


# Tile coordinates can come in negatives -- which Django doesn't support in their <int>.
class NegativeIntConverter:
    regex = '-?\d+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%d' % value


register_converter(NegativeIntConverter, 'negint')

urlpatterns = [
    path('admin/', admin.site.urls),

    # API calls for the Client
    path('client/<slug:token>/api/v2/updateGrid', api_views.update_grid),
    path('client/<slug:token>/api/v1/locate', api_views.locate_character),
    path('client/<slug:token>/api/v2/updateCharacter', api_views.update_character),
    path('client/<slug:token>/api/v1/uploadMarkers', api_views.upload_marker),
    path("client/<slug:token>/grids/mapdata_index", api_views.mapdata_index),

    # The endpoints the client calls that make no sense.
    path('client/<slug:token>/', map_views.map_page2),
    #path('client/<slug:token>/api/tile/<int:zoom>/<negint:x_coord>/<negint:y_coord>', map_views.get_tile),

    # API calls for the Map
    path('map/api/getPlayers', api_views.get_players, name="get_player_markers"),
    path('map/api/tile/<int:zoom>/<negint:x_coord>/<negint:y_coord>', map_views.get_tile),
    path('map/api/getMarkers', api_views.get_markers, name="get_markers"),
    path('map/api/generateToken', api_views.generate_token, name="generate_token"),

    # Map url
    path('', map_views.map_index, name="map_index"),
    path('map/', map_views.map_page, name="map_page"),
    path('login/', map_views.user_login, name="map_login"),
    path('generateZoom/', map_views.generate_zoom_layers, name="map_logout"),

    path('logout/', map_views.user_logout, name="generate_zoom")
]

