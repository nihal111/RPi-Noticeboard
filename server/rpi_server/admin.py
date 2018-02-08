# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.admin import PhotoAdmin as PhotoAdminDefault
from photologue.models import Gallery, Photo

from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError

from .models import PhotoExtended

MAX_LIMIT = 15


class GalleryAdminForm(forms.ModelForm):
    """Users never need to enter a description on a gallery."""

    def __init__(self, *args, **kwargs):
        super(GalleryAdminForm, self).__init__(*args, **kwargs)
        self.fields['photos'].help_text = \
            'IMPORTANT: Select a maximum of {} photos.'.format(str(MAX_LIMIT))

    class Meta:
        model = Gallery
        exclude = ['date_added', 'sites', ]


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
        else:
            return qs.filter(title__iexact=request.user)
        # TODO: add a m2m link between users and galleries and display
        # only those galleries that are linked to the user.
        # qs.filter(users_allowed__in=[request.user])


class PhotoAdminForm(forms.ModelForm):
    """Users never need to enter a description on a gallery."""

    class Meta:
        model = PhotoExtended
        exclude = ['date_added', 'effect', 'sites', 'is_public']


class PhotoExtendedInline(admin.StackedInline):
    model = PhotoExtended
    can_delete = False


class PhotoAdmin(PhotoAdminDefault):
    form = PhotoAdminForm
    inlines = [PhotoExtendedInline, ]


admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)


admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)
admin.site.unregister(Photo)
admin.site.register(Photo, PhotoAdmin)


def regions_changed(sender, **kwargs):
    if kwargs['instance'].photos.count() > MAX_LIMIT:
        raise ValidationError("You can't assign more than three regions")


# Uncomment this line to put a cap of photos every gallery can contain
# This cap is defined by MAX_LIMIT
m2m_changed.connect(regions_changed, sender=Gallery.photos.through)
