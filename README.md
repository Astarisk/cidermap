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

When an account is made the first task that needs to be done to have the client interact with the map is to generate a token. This token can be found and generated at the Login / Index page. Copy the token and paste it into the mapping option section of the client.

ex: 127.0.0.1:8000/client/z3jfhe9X9ezu - This is what should be copied into the settings in the options window of labeled Map Settings..
