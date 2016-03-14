# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core import serializers

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

def hierarchy_list(request, model):
    return JsonResponse(get_model(model).objects.all())

def folder_photos(request, model, folder_id):
    folder = get_object_or_404(get_model(model), pk=folder_id)
    return JsonResponse(folder.photos.all())

def photo_thumbnail(request, photo_id, size):
    size = int(size)
    photo = get_object_or_404(Photo, pk=photo_id)
    response = HttpResponse(content_type="image/jpeg")
    im = Image.open(photo.path)
    im.thumbnail((size, size))
    im.save(response, "JPEG")
    return response

def photo_download(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    response = HttpResponse(content_type="image/jpeg")
    im = Image.open(photo.path)
    im.save(response, "JPEG")
    return response
