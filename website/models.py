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

class Photo(models.Model):
    folder = models.ForeignKey(PhysicalFolder,
                               on_delete=models.CASCADE,
                               related_name="photos")
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=1000)

class VirtualFolderPhotos(models.Model):
    folder = models.ForeignKey(VirtualFolder,
                               on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo,
                              on_delete=models.CASCADE)
    locked = models.BooleanField()

    class Meta:
        unique_together = ("folder", "photo")
