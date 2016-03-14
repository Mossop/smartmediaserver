# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models

class PhysicalFolder(models.Model):
    parent = models.ForeignKey("self",
                               null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name="children",
                               related_query_name="child")
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=1000, unique=True)

    class Meta:
        unique_together = ("parent", "name")

    def __unicode__(self):
        return self.name

class VirtualFolder(models.Model):
    parent = models.ForeignKey("self",
                               null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name="children",
                               related_query_name="child")
    photos = models.ManyToManyField("Photo",
                                    related_name="virtual_folders",
                                    through="VirtualFolderPhotos")
    name = models.CharField(max_length=200)
    index = models.IntegerField()

    class Meta:
        unique_together = (("parent", "name"), ("parent", "index"))

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    parent = models.ForeignKey("self",
                               null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name="children",
                               related_query_name="child")
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ("parent", "name")

class Person(models.Model):
    name = models.CharField(max_length=200, unique=True)

class Photo(models.Model):
    folder = models.ForeignKey(PhysicalFolder,
                               on_delete=models.CASCADE,
                               related_name="photos")
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=1000, unique=True)
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

class VirtualFolderPhotos(models.Model):
    folder = models.ForeignKey(VirtualFolder,
                               on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo,
                              on_delete=models.CASCADE)
    locked = models.BooleanField()

    class Meta:
        unique_together = ("folder", "photo")
