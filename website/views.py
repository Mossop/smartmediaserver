# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core import serializers

from website.models import *

def index(request):
    return render(request, "website/index.html")

def physicalfolders(request):
    return HttpResponse(
        serializers.serialize("json", PhysicalFolder.objects.all()),
        content_type="text/json"
    )

def virtualfolders(request):
    return HttpResponse(
        serializers.serialize("json", VirtualFolder.objects.all()),
        content_type="text/json"
    )

def photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    return HttpResponse(serializers.serialize("json", photo))

