# CiderMap

A collaborative automapping project for **Haven & Hearth**, built with Python and Django. Game clients upload map tiles, landmarks, and character positions; a browser map brings them together with Leaflet and PixiJS.

This is an older personal project. The repository contains the mapping service and browser UI, with some rough edges that need attention before bringing up a new shared instance.

## What's in the code

- Client endpoints for grid images and coordinates, character positions, markers, and a grid index.
- Django user accounts and generated tokens for client uploads.
- A Leaflet map with Leaflet.PixiOverlay for landmark and player sprites, including periodic player-position refreshes.
- PNG map tiles on disk, with Pillow routines that combine tiles into lower zoom levels.
- Django admin for managing users and stored map data.

## How it fits together

`myapi/` handles client uploads, tokens, and map metadata. `map/` contains the browser views, custom user model, and tile/zoom handling. Routes and application settings live in `config/`.

The checked-in settings use **SQLite** (`db.sqlite3`). Uploaded tiles are stored under `map_grids/9/`; generated zoom layers live alongside them. Back up both the database and tile directory to preserve a map.

## Historical local setup

The Dockerfile targets Python 3.8, and `requirements.txt` pins the original dependency stack, including Django 3.1.14. Treat this as a starting point for reproducing the project, not a tested setup on current Python releases.

From the repository root, in an isolated Python environment:

```sh
python -m pip install -r requirements.txt
python manage.py makemigrations map myapi
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
python manage.py runserver
```

Initial migrations are not checked in, so generate them for both local apps before migrating. The settings also reference a root `static/` directory that is absent from the checkout; create it or remove that unused entry from `STATICFILES_DIRS` if Django reports it.

Open <http://127.0.0.1:8000/> to log in, and <http://127.0.0.1:8000/admin/> to manage accounts. Once logged in, generate a token on the index page and configure a compatible game client's mapping URL as:

```text
http://127.0.0.1:8000/client/<your-token>/
```

The browser map is at `/map/`. The intended initial mapping flow uses the first located grid as `(0, 0)`; see the locate limitation below before trying that flow.

## Known limitations

- The client `locate` route supplies a `token` argument, but `locate_character` does not accept it. Its initial-grid path also sets a non-null timestamp field to `None`. That path needs repair before relying on initial map alignment.
- The browser template references a player-marker image that is not included in the checkout.
- The Compose file includes PostgreSQL, but Django remains configured for SQLite. It maps host port `8420` to Gunicorn on port `8000` and does not run migrations or configure static-file serving automatically.
- The checked-in settings enable debug mode and include a development secret key. A shared deployment needs updated dependencies, deployment-specific settings, and a review of authentication and upload handling.

## Main pieces

| Path | Purpose |
| --- | --- |
| [myapi/views.py](myapi/views.py) | Upload and map-data endpoints |
| [myapi/models.py](myapi/models.py) | Grids, markers, character positions, and tokens |
| [map/views.py](map/views.py) | Browser views, tile serving, and zoom generation |
| [map/templates/map/map.html](map/templates/map/map.html) | Leaflet/PixiJS map UI |
| [config/settings.py](config/settings.py) | Database and Django configuration |
| [config/urls.py](config/urls.py) | Browser and client routes |
