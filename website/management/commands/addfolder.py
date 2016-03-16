# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

from django.core.management.base import BaseCommand, CommandError

from website.models import *
from website.management.command import UICommand

class Command(UICommand):
    help = "Update an existing repository."

    def add_arguments(self, parser):
        parser.add_argument("--name", help="")
        parser.add_argument("--url", help="A URL that this folder can be reached at directly.")
        parser.add_argument("path")

    def handle(self, *args, **kwargs):
        path = kwargs["path"]

        if not os.path.isdir(path):
            raise CommandError("\"%s\" is not a directory." % path)

        if kwargs["name"]:
            name = kwargs["name"]
        else:
            name = os.path.basename(path)

        url = None
        if kwargs["url"]:
            url = kwargs["url"]
            if url[-1:] != "/":
                url = url + "/"

        self.info("Adding \"%s\" as %s." % (path, name))
        folder = PhysicalFolderRoot(name=name, physicalpath=path, directurl=url)
        folder.save()
