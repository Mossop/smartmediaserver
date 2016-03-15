# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
import json

from django.http import HttpResponse, Http404
from django.views.decorators.http import last_modified
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.core.files import File

from website.models import *

from PIL import Image

def JsonResponse(objects):
    return HttpResponse(
        serializers.serialize("json", objects),
        content_type="application/json"
    )

def get_model(model):
    if model == "physicalfolder":
        return PhysicalFolder
    if model == "virtualfolder":
        return VirtualFolder
    if model == "tag":
        return Tag
    if model == "person":
        return Person
    raise Http404("Model %s does not exist" % model)

def index(request):
    return render(request, "website/index.html")

def root_list(request):
    roots = [
        { "model": "physicalfolder", "name": "All Photos" },
        { "model": "tag", "name": "Tags" },
        { "model": "person", "name": "People" }
    ]
    return HttpResponse(json.dumps(roots), content_type="application/json")

def root_contents(request, model):
    model = get_model(model)
    subfolders = model.objects.filter(parent__isnull=True)
    return JsonResponse(subfolders)

def folder_contents(request, model, folder_id):
    model = get_model(model)
    folder = get_object_or_404(model, pk=folder_id)

    subfolders = list(model.objects.filter(parent=folder).order_by("name"))
    photos = list(folder.photos.all().order_by("captured"))

    return JsonResponse(subfolders + photos)

def photo_modified(request, photo_id, **kwargs):
    photo = get_object_or_404(Photo, pk=photo_id)
    return photo.mtime

@last_modified(photo_modified)
def photo_thumbnail(request, photo_id, size):
    size = int(size)
    photo = get_object_or_404(Photo, pk=photo_id)
    response = HttpResponse(content_type="image/jpeg")
    im = Image.open(photo.path)
    im.thumbnail((size, size))
    im.save(response, "JPEG", optimize=True, quality=95, icc_profile=im.info.get('icc_profile'))
    return response

@last_modified(photo_modified)
def photo_shrink_to_fit(request, photo_id, width, height):
    width = int(width)
    height = int(height)
    photo = get_object_or_404(Photo, pk=photo_id)
    response = HttpResponse(content_type="image/jpeg")
    im = Image.open(photo.path)
    im.thumbnail((width, height))
    im.save(response, "JPEG", optimize=True, quality=95, icc_profile=im.info.get('icc_profile'))
    return response

@last_modified(photo_modified)
def photo_download(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    filename = photo.path
    wrapper = File(file(filename))
    response = HttpResponse(wrapper, content_type="image/jpeg")
    response['Content-Length'] = os.path.getsize(photo.path)
    return response
