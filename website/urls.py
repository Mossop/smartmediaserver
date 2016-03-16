# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^list/roots$", views.root_list),
    url(r"^(?P<model>physicalfolder|virtualfolder|tag|person)/contents$", views.root_contents),
    url(r"^(?P<model>physicalfolder|virtualfolder|tag|person)/(?P<folder_id>[0-9]+)/contents$", views.folder_contents),
    url(r"^photo/(?P<photo_id>[0-9]+)/thumbnail/(?P<size>[0-9]+)$", views.photo_thumbnail),
    url(r"^photo/(?P<photo_id>[0-9]+)/shrink/to/fit/(?P<width>[0-9]+)x(?P<height>[0-9]+)$", views.photo_shrink_to_fit),
    url(r"^photo/(?P<photo_id>[0-9]+)/download$", views.photo_download, name="download-photo")
]
