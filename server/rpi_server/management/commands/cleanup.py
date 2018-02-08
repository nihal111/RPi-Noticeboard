from django.core.management.base import BaseCommand
from rpi_server.models import PhotoExtended as Photos
import datetime


class Command(BaseCommand):
    help = 'Deletes photos which have expired.'

    def handle(self, *args, **options):
        print("Running on " + str(datetime.date.today()))
        photos = Photos.objects.all().filter(
            expiry_date__lt=datetime.date.today())
        for photo in photos:
            self.stdout.write(self.style.WARNING(
                'Successfully deleted {} with expiry date {}'
                .format(photo, photo.expiry_date)))
            Photos.objects.filter(id=photo.id).delete()
        self.stdout.write(self.style.SUCCESS('Deleted all old photos'))
        print
