from django.core.management.base import BaseCommand, CommandError

from gallery.utils import add_test_photos


class Command(BaseCommand):
    help = (
        "This command will add test photos from " "media/test_photos folder to database"
    )

    def handle(self, *args, **kwargs):
        try:
            add_test_photos()
        except Exception as ex:
            raise CommandError(ex)
