from django.core.management.base import BaseCommand, CommandError

from horses.models import Horse
from horses.utils import set_fake_horse_parents


class Command(BaseCommand):
    help = "This command will set fake horses pedigree for developing"

    def handle(self, *args, **kwargs):
        try:
            all_horses = Horse.objects.all()
            for horse in all_horses:
                set_fake_horse_parents(horse)
        except Exception as ex:
            raise CommandError(ex)
