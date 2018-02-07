# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.admin import PhotoAdmin as PhotoAdminDefault
from photologue.models import Gallery, Photo

from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError


MAX_LIMIT = 3


class GalleryAdminForm(forms.ModelForm):
    """Users never need to enter a description on a gallery."""

    class Meta:
        model = Gallery
        exclude = ['date_added', 'sites',]


class GalleryAdmin(GalleryAdminDefault):
    form = GalleryAdminForm

    def get_actions(self, request):
        actions = super(GalleryAdmin, self).get_actions(request)
        if not request.user.is_superuser and 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_queryset(self, request):
        qs = super(GalleryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs
        # TODO: add a m2m link between users and galleries and display
        # only those galleries that are linked to the user. 
        # qs.filter(users_allowed__in=[request.user])


class PhotoAdminForm(forms.ModelForm):
    """Users never need to enter a description on a gallery."""

    class Meta:
        model = Photo
        exclude = ['date_added', 'effect', 'sites', 'is_public']


class PhotoAdmin(PhotoAdminDefault):
    form = PhotoAdminForm


admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)
admin.site.unregister(Photo)
admin.site.register(Photo, PhotoAdmin)


def regions_changed(sender, **kwargs):
    if kwargs['instance'].photos.count() > MAX_LIMIT:
        raise ValidationError("You can't assign more than three regions")


m2m_changed.connect(regions_changed, sender=Gallery.photos.through)
