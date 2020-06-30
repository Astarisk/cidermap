import json
import os
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Grid, MarkerData, LostMarkerData, CharacterLocation, GeneratedToken
from .decorators import check_token


# Create your views here.

# Let's make sure the directory for saving map tiles exists
if not os.path.exists('./map_grids/9'):
    os.makedirs('./map_grids/9')


def handle_minimap_upload(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@check_token
@csrf_exempt
def update_grid(request):
    if request.method == "POST":

        grid_id = request.POST["id"]
        x_coord = request.POST["x"]
        y_coord = request.POST["y"]

        obj, created = Grid.objects.get_or_create(
            grid_id=grid_id,
            x_coord=x_coord,
            y_coord=y_coord
        )

        if created:
            # First time being made so save the grid.
            handle_minimap_upload(request.FILES['file'], f"./map_grids/9/{x_coord}_{y_coord}.png")
        else:
            # Update the saved minimap file.
            updated_time = timezone.now()
            threshhold = timedelta(minutes=20)

            if updated_time - obj.update_timestamp > threshhold:
                obj.update_timestamp = updated_time
                obj.save()

                # Refresh the saved minimap file.
                handle_minimap_upload(request.FILES['file'], f"./map_grids/9/{x_coord}_{y_coord}.png")

    return HttpResponse(status=200)


@check_token
@csrf_exempt
def upload_marker(request):
    if request.method == "POST":
        markers = json.loads(request.body)

        for marker in markers:
            image = "gfx/terobjs/mm/custom"
            try:
                if marker["image"]:
                    image = marker["image"]
            except KeyError:
                pass

            data = MarkerData.objects.all().values().filter(grid_id=marker['gridId'], x_coord=marker['x'],
                                                            y_coord=marker['y'])

            lost_data = LostMarkerData.objects.all().values().filter(grid_id=marker['gridId'], x_coord=marker['x'],
                                                                     y_coord=marker['y'])

            if data.exists() or lost_data.exists():
                continue
            else:
                if 'BORDER_CAIRN:OURS' in marker['name']:
                    image = "gfx/terobjs/mm/frendcairn"
                if 'BORDER_CAIRN:THEIRS' in marker['name']:
                    image = "gfx/terobjs/mm/enemycairn"

                if 'SEA_MARK:OURS' in marker['name']:
                    image = "gfx/terobjs/mm/seamark"
                if 'SEA_MARK:THEIRS,' in marker['name']:
                    image = "gfx/terobjs/mm/enemyseamark"

                grid = Grid.objects.filter(grid_id=marker['gridId'])

                # Markers that have a known grid id
                if grid.exists():
                    data = MarkerData(grid_id=marker['gridId'], x_coord=marker['x'], y_coord=marker['y'],
                                      image=image, name=marker['name'], hidden=False)
                    data.save()
                else:
                    # Markers with no grid id (thus no way to place it on a map)
                    data = LostMarkerData(grid_id=marker['gridId'], x_coord=marker['x'], y_coord=marker['y'],
                                          image=image, name=marker['name'])
                    data.save()
    return HttpResponse(status=200)



@csrf_exempt
def locate_character(request):
    if request.method == "GET":
        grids = Grid.objects.all()

        # If no entries exist in the database, set the received gridID as the 0,0 location
        if not grids.exists():
            grid = Grid(grid_id=request.GET["gridId"], x_coord=0, y_coord=0, update_timestamp=None)
            grid.save()
            return HttpResponse(status=200, content=f"0;0")

        entry = grids.filter(pk=request.GET["gridId"])

        if entry.exists():
            return HttpResponse(status=200, content=f"{entry.get().x_coord};{entry.get().y_coord}")
    return HttpResponse(status=404)


@check_token
@csrf_exempt
def update_character(request):
    if request.method == "POST":
        char_pos = json.loads(request.body)
        if char_pos["type"] == 'located':
            char_loc = CharacterLocation(gob_id=char_pos["id"], name=char_pos["name"], x_coord=char_pos["x"],
                                         y_coord=char_pos["y"])
            char_loc.save()

    return HttpResponse(status=200)


@login_required
def get_players(request):
    if request.user.is_authenticated:
        markers = []

        # Grab the entries within the last 10 seconds
        q = CharacterLocation.objects.filter(time_added__gt=timezone.now() - timedelta(seconds=10))

        # Grab the unique gob_id
        characters = q.values('gob_id').distinct()

        # Loop through the latest and entries and return only the latest of each unique gob
        for char in characters:
            latest_entry = q.filter(gob_id=char["gob_id"]).latest('time_added')

            # Hard coding in the image name for now. Just so I don't need to change the HTML/JS TODO:
            marker = {'name': latest_entry.name, 'image': "gfx/terobjs/mm/player",
                      'x': latest_entry.x_coord, 'y': latest_entry.y_coord}
            markers.append(marker)
        return JsonResponse(markers, safe=False)
    return HttpResponseRedirect(reverse('map_index'))


def get_markers(request):
    if request.user.is_authenticated:
        data = MarkerData.objects.all().filter(hidden=False)

        markers = []

        for d in data:
            grid = Grid.objects.filter(pk=d.grid_id).get()

            x = d.x_coord + grid.x_coord * 100
            y = d.y_coord + grid.y_coord * 100

            marker = {'name': d.name, 'image': d.image, 'x': x, 'y': y}
            markers.append(marker)

        return JsonResponse(markers, safe=False)
    return HttpResponseRedirect(reverse('map_index'))


def generate_token(request):
    if request.user.is_authenticated:
        user = get_user_model().objects.filter(pk=request.user.id).get()
        token = GeneratedToken(owner=user)
        token.save()
    return HttpResponseRedirect(reverse('map_index'))


@check_token
@csrf_exempt
def mapdata_index(request):
    grids = Grid.objects.all()

    s = ""
    for grid in grids:
        s += f"{grid.grid_id},{grid.x_coord},{grid.y_coord}\n"

    return HttpResponse(status=200, content=s)
