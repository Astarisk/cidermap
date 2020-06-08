# cidermap
Automapping service for HnH built with python and Django.


The map itself is made using Leaflet + Leaflet.PixiOverlay. 

Leaflet.PixiOverlay helps provide better performance for a mass amount of markers providing a smoother experience and other fun features.

To get started run the following:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic
    
 Once these have been ran create a super user with django:
    python manage.py createsuperuser
    
From here you can add more members through the django admin panel (127.0.0.1:8000/admin)

The first client that connects and logs in sets the 0,0 location for the map.

