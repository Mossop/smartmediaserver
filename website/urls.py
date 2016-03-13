# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^physicalfolder/list$", views.physicalfolders, name="physicalfolders"),
    url(r"^virtualfolder/list$", views.virtualfolders, name="virtualfolders"),
    url(r"^photo/get/(?P<photo_id>[0-9]+)$", views.photo, name="photo")
]
