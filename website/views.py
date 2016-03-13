# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core import serializers

from website.models import *

from PIL import Image

def index(request):
    return render(request, "website/index.html")

def physicalfolders_list(request):
    return HttpResponse(
        serializers.serialize("json", PhysicalFolder.objects.all()),
        content_type="application/json"
    )

def physicalfolders_photos(request, folder_id):
    folder = get_object_or_404(PhysicalFolder, pk=folder_id)
    return HttpResponse(
        serializers.serialize("json", folder.photos.all()),
        content_type="application/json"
    )

def virtualfolders_list(request):
    return HttpResponse(
        serializers.serialize("json", VirtualFolder.objects.all()),
        content_type="application/json"
    )

def virtualfolders_photos(request, folder_id):
    folder = get_object_or_404(VirtualFolder, pk=folder_id)
    return HttpResponse(
        serializers.serialize("json", folder.photos.all()),
        content_type="application/json"
    )

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
