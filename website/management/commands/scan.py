# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
import pytz

from website.models import *
from website.management.command import UICommand

from optparse import make_option

from PIL import Image
import exifread
from libxmp import XMPFiles, consts


class Command(UICommand):
    help = "Update an existing repository."

    def apply_exif(self, photo):
        def parse_date(datestr):
            return pytz.utc.localize(datetime.strptime(str(datestr), "%Y:%m:%d %H:%M:%S"))

        def parse_location(location, direction):
            location = str(location).replace("[", "").replace("]", "").replace(" ", "")
            parts = location.split(",")

            degrees = 0
            mult = 1
            for part in parts:
                check = part.split("/")
                value = float(check[0])
                if len(check) == 2:
                    value = value / float(check[1])
                degrees = degrees + value / mult
                mult = mult * 60

            if str(direction) == "S" or str(direction) == "W":
                return -degrees
            return degrees

        try:
            f = open(photo.path, 'rb')
            tags = exifread.process_file(f)
            self.info("Found EXIF data")
        except Exception as err:
            self.info("Failed to load EXIF data: %s" % err)
            return

        if "EXIF DateTimeOriginal" in tags:
            photo.captured = parse_date(tags["EXIF DateTimeOriginal"])
        elif "EXIF DateTimeDigitized" in tags:
            photo.captured = parse_date(tags["EXIF DateTimeDigitized"])

        if "Image Artist" in tags:
            photo.author = str(tags["Image Artist"])

        if "GPS GPSLatitude" in tags and "GPS GPSLatitudeRef" in tags and "GPS GPSLongitude" in tags and "GPS GPSLongitudeRef" in tags:
            photo.latitude = parse_location(tags["GPS GPSLatitude"], tags["GPS GPSLatitudeRef"])
            photo.longitude = parse_location(tags["GPS GPSLongitude"], tags["GPS GPSLongitudeRef"])

    def apply_xmp(self, photo):
        try:
            xmpfile = XMPFiles(file_path=photo.path)
            xmp = xmpfile.get_xmp()
            self.info("Found XMP data")
        except Exception as err:
            self.info("Failed to load XMP data: %s" % err)
            return

        def has_property(ns, prop):
            try:
                xmp.get_property(ns, prop)
                return True
            except:
                return False

        def read_array(ns, prop):
            results = []
            index = 0
            while True:
                index = index + 1
                try:
                    results.append(xmp.get_array_item(ns, prop, index))
                except:
                    return results

        if has_property(consts.XMP_NS_Lightroom, "hierarchicalSubject"):
            tags = read_array(consts.XMP_NS_Lightroom, "hierarchicalSubject")
            for tagname in tags:
                tagparts = tagname.split("|")
                parent = None
                for tagname in tagparts:
                    tag, created = Tag.objects.get_or_create(parent=parent, name=tagname)
                    photo.tags.add(tag)
                    parent = tag
        elif has_property(consts.XMP_NS_DC, "subject"):
            tags = read_array(consts.XMP_NS_DC, "subject")
            for tagname in tags:
                tag, created = Tag.objects.get_or_create(parent=None, name=tagname)
                photo.tags.add(tag)

        if has_property("http://iptc.org/std/Iptc4xmpExt/2008-02-29/", "PersonInImage"):
            people = read_array("http://iptc.org/std/Iptc4xmpExt/2008-02-29/", "PersonInImage")
            for name in people:
                person, created = Person.objects.get_or_create(name=name)
                photo.people.add(person)

        if has_property(consts.XMP_NS_XMP, "Rating"):
            photo.rating = xmp.get_property_int("http://ns.adobe.com/xap/1.0/", "Rating")

        if has_property(consts.XMP_NS_XMP, "CreateDate"):
            photo.captured = xmp.get_property_datetime("http://ns.adobe.com/xap/1.0/", "CreateDate")

        if has_property(consts.XMP_NS_Photoshop, "DateCreated"):
            photo.captured = xmp.get_property_datetime("http://ns.adobe.com/photoshop/1.0/", "DateCreated")

        if has_property(consts.XMP_NS_IPTCCore, "Location"):
            photo.location = xmp.get_property(consts.XMP_NS_IPTCCore, "Location")

        if has_property(consts.XMP_NS_Photoshop, "City"):
            photo.city = xmp.get_property("http://ns.adobe.com/photoshop/1.0/", "City")

        if has_property(consts.XMP_NS_Photoshop, "State"):
            photo.state = xmp.get_property("http://ns.adobe.com/photoshop/1.0/", "State")

        if has_property(consts.XMP_NS_Photoshop, "Country"):
            photo.country = xmp.get_property("http://ns.adobe.com/photoshop/1.0/", "Country")

        if has_property(consts.XMP_NS_DC, "creator"):
            creators = read_array(consts.XMP_NS_DC, "creator")
            photo.author = ", ".join(creators)

    def scan_photo(self, folder, path):
        try:
            im = Image.open(path)
        except Exception as err:
            return

        stats = os.stat(path)

        try:
            photo = Photo.objects.get(path=path)
            mtime = pytz.utc.localize(datetime.utcfromtimestamp(stats.st_mtime))
            if mtime == photo.mtime:
                return

            photo.delete()
            self.status("Updating photo %s." % path)
        except ObjectDoesNotExist:
            self.status("Adding photo %s." % path)

        photo = Photo(folder=folder, path=path, name=os.path.basename(path))
        photo.mtime = pytz.utc.localize(datetime.utcfromtimestamp(stats.st_mtime))
        (photo.width, photo.height) = im.size
        photo.save()

        try:
            self.apply_exif(photo)
        except:
            self.error("Failed to read EXIF data")
            self.traceback()

        try:
            self.apply_xmp(photo)
        except:
            self.error("Failed to read XMP data")
            self.traceback()

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
