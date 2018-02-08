from django.db import models

import datetime

from photologue.models import Photo
from django.dispatch import receiver
from django.db.models.signals import post_delete


class PhotoExtended(models.Model):

    # Link back to Photologue's Gallery model.
    photo = models.OneToOneField(Photo, related_name='extended')

    # This is the important bit - where we add in the tags.
    expiry_date = models.DateField(default=datetime.date.today)

    # Boilerplate code to make a prettier display in the admin interface.
    class Meta:
        verbose_name = u'Extra fields'
        verbose_name_plural = u'Extra fields'

    def __str__(self):
        return self.photo.title

    def admin_thumbnail(self):
        func = getattr(self, 'get_admin_thumbnail_url', None)


@receiver(post_delete, sender=PhotoExtended)
def post_delete_photo_extended(sender, instance, *args, **kwargs):
    if instance.photo:  # just in case photo is not specified
        instance.photo.delete()
