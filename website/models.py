# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

from django.db import models
from django.core.urlresolvers import reverse

class Folder(models.Model):
    parent = models.ForeignKey("self",
                               null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name="children",
                               related_query_name="child")
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ("parent", "name")
        abstract = True

    def __unicode__(self):
        return self.name

class PhysicalFolder(Folder):
    @property
    def path(self):
        if self.parent:
            return os.path.join(self.parent.path, self.name)
        else:
            return self.physicalfolderroot.path

    @property
    def url(self):
        if self.parent:
            if self.parent.url:
                return "%s%s/" % (self.parent.url, self.name)
            return None
        else:
            return self.physicalfolderroot.url

class PhysicalFolderRoot(PhysicalFolder):
    physicalpath = models.CharField(max_length=255, unique=True)
    directurl = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        pass

    @property
    def path(self):
        return self.physicalpath

    @property
    def url(self):
        return self.directurl

class VirtualFolder(Folder):
    photos = models.ManyToManyField("Photo",
                                    related_name="virtual_folders",
                                    through="VirtualFolderPhotos")
    index = models.IntegerField()

    class Meta:
        unique_together = (("parent", "name"), ("parent", "index"))

    def __unicode__(self):
        return self.name

class Tag(Folder):
    pass

class Person(Folder):
    pass

class Photo(models.Model):
    folder = models.ForeignKey(PhysicalFolder,
                               on_delete=models.CASCADE,
                               related_name="photos")
    filename = models.CharField(max_length=200)
    mtime = models.DateTimeField()

    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    captured = models.DateTimeField(null=True, blank=True)
    author = models.CharField(null=True, blank=True, max_length=200)
    raiting = models.IntegerField(null=True, blank=True)

    tags = models.ManyToManyField(Tag, related_name="photos")
    people = models.ManyToManyField(Person, related_name="photos")

    class Meta:
        unique_together = ("folder", "filename")

    @property
    def path(self):
        return os.path.join(self.folder.path, self.filename)

    @property
    def url(self):
        if self.folder.url:
            return "%s%s" % (self.folder.url, self.filename)
        return reverse("download-photo", kwargs={ "photo_id": self.pk })

class VirtualFolderPhotos(models.Model):
    folder = models.ForeignKey(VirtualFolder,
                               on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo,
                              on_delete=models.CASCADE)
    locked = models.BooleanField()

    class Meta:
        unique_together = ("folder", "photo")
