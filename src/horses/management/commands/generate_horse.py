from django.core.management.base import BaseCommand, CommandError

from horses.utils import FakeHorsesGenerator


class Command(BaseCommand):
    help = "This command will generate fake horses for developing"

    def handle(self, *args, **kwargs):
        try:
            generator = FakeHorsesGenerator()
            for _ in range(int(kwargs["count"])):
                generator.generate()
                generator.add_to_db()
                print(generator.name)
        except Exception as ex:
            raise CommandError(ex)

    def add_arguments(self, parser):
        parser.add_argument(
            "-c", "--count", action="store", default=1, help="Количество лошадей"
        )
