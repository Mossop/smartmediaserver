# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

from django.core.management.base import BaseCommand, CommandError

from website.models import *
from website.management.command import UICommand

from optparse import make_option

class Command(UICommand):
    help = "Update an existing repository."

    def add_arguments(self, parser):
        parser.add_argument("name")
        parser.add_argument("path")

    def handle(self, *args, **kwargs):
        name = kwargs["name"]
        path = kwargs["path"]

        if not os.path.isdir(path):
            raise CommandError("\"%s\" is not a directory." % path)

        self.info("Adding \"%s\" as %s." % (path, name))
        folder = PhysicalFolder(parent=None, name=name, path=path)
        folder.save()
