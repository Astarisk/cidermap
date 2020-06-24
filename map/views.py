import time
import os

from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from PIL import Image
from math import floor

from myapi.models import Grid, MarkerData
from .forms import CustomUserCreationForm

tile_cache = {}


def map_index(request):
    context = {}
    if request.user.is_authenticated:
        context['tokens'] = request.user.generatedtoken_set.all()
    return render(request, "map/index.html", context)


def map_page(request, token=""):
    if request.user.is_authenticated:
        # A Quick and dirty way to grab the URLS to the map icons
        context = {'marker_images': MarkerData.objects.all().values('image').distinct()}
        return render(request, "map/map.html", context)
    return HttpResponseRedirect(reverse('map_index'))


# I'm not quite sure how to strip the client/token out of url so I'm just using this here with a reverse.
# I'm sure there is some way in the urls.conf to do what I want but I don't know how yet.
def map_page2(request, token):
    return HttpResponseRedirect(reverse('map_page'))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("map_index"))


def user_register(request):
    context = {

    }
    registered = False

    if request.method == 'POST':
        print("trying to register....")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("form was valid")
            form.save()
            username = form.cleaned_data.get('username')
            print(f"username: {username}")
            raw_password = form.cleaned_data.get('password1')
            print(f"pw: {raw_password}")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('map_index'))
        else:
            print("invalied form")
    else:
        context["form"] = CustomUserCreationForm()
    return render(request, 'map/register.html', context)


def user_login(request):
    context = {

    }

    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('map_index'))
        else:
            context["alert_message"] = "Invalid Credentials."

    return render(request, 'map/login.html', context)


@login_required
@csrf_exempt
def get_tile(request, zoom, x_coord, y_coord):
    try:
        tmp_img = tile_cache.get(f"{zoom}/{x_coord}/{y_coord}")
        if tmp_img:
            return HttpResponse(status=200, content=tmp_img, content_type='image/png')
        else:
            tmp_img = open(f"./map_grids/{zoom}/{x_coord}_{y_coord}.png", "rb", buffering=0).read()
            tile_cache[f"{zoom}/{x_coord}/{y_coord}"] = tmp_img
        return HttpResponse(status=200, content=tmp_img, content_type='image/png')
    except FileNotFoundError:
        return HttpResponse(status=404)


def generate_zoom_mapping():
    grids = Grid.objects.all()

    mapping = set()

    for grid in grids:
        mapping.add((floor(grid.x_coord / 2), floor(grid.y_coord / 2)))

    return mapping


@login_required
def generate_zoom_layers(request):
    print(time.time())
    # Goes from 3 to 9 (uploaded tiles)
    initial_mapping = generate_zoom(generate_zoom_mapping(), 9)
    initial_mapping = generate_zoom(initial_mapping, 8)
    initial_mapping = generate_zoom(initial_mapping, 7)
    initial_mapping = generate_zoom(initial_mapping, 6)
    initial_mapping = generate_zoom(initial_mapping, 5)
    print(time.time())

    return HttpResponseRedirect(reverse('map_index'))


def generate_zoom(initial_mapping, in_layer):
    start = time.time()
    new_mapping = set()
    out_layer = in_layer - 1

    if not os.path.exists(f"./map_grids/{out_layer}"):
        os.mkdir(f"./map_grids/{out_layer}")

    for map in initial_mapping:
        zoom_image = Image.new('RGBA', (100, 100))

        draw_x = 0
        for x_coord in range(map[0] * 2, (map[0] * 2) + 2):
            draw_y = 0
            for y_coord in range(map[1] * 2, (map[1] * 2) + 2):

                # Open the previous zoom's image
                try:
                    tmp_img = Image.open(f"./map_grids/{in_layer}/{x_coord}_{y_coord}.png")
                    tmp_img = tmp_img.resize((50, 50), resample=Image.LANCZOS)
                    zoom_image.paste(tmp_img, (draw_x, draw_y))
                except FileNotFoundError:
                    pass
                draw_y += 50
            draw_x += 50

        zoom_image.save(f"./map_grids/{out_layer}/{map[0]}_{map[1]}.png")

        new_mapping.add((floor(map[0] / 2), floor(map[1] / 2)))

    print(f"finished layer: {out_layer} - " + str(start - time.time()))
    return new_mapping
