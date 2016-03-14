# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from website.models import *
from website.management.command import UICommand

from optparse import make_option

from PIL import Image

class Command(UICommand):
    help = "Update an existing repository."

    def scan_photo(self, folder, path):
        try:
            im = Image.open(path)
        except:
            return

        try:
            photo = Photo.objects.get(path=path)
        except ObjectDoesNotExist:
            self.info("Adding photo %s." % path)
            photo = Photo(folder=folder, name=os.path.basename(path), path=path)
            photo.save()

    def scan_folder(self, folder):
        self.info("Scanning %s..." % folder.path)

        names = os.listdir(folder.path)
        for name in names:
            path = os.path.join(folder.path, name)
            if os.path.isdir(path):
                try:
                    nextfolder = PhysicalFolder.objects.get(path=path)
                except ObjectDoesNotExist:
                    self.info("Adding folder %s." % path)
                    nextfolder = PhysicalFolder(parent=folder, name=name, path=path)
                    nextfolder.save()
                self.scan_folder(nextfolder)
            elif os.path.isfile(path):
                self.scan_photo(folder, path)

        oldphotos = list(Photo.objects.filter(folder=folder).exclude(name__in=names))
        for photo in oldphotos:
            photo.delete()

        oldfolders = list(PhysicalFolder.objects.filter(parent=folder).exclude(name__in=names))
        for oldfolder in oldfolders:
            oldfolder.delete()

    def handle(self, *args, **kwargs):
        roots = PhysicalFolder.objects.filter(parent__isnull=True)
        for root in roots:
            self.scan_folder(root)
