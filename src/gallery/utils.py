from pathlib import Path

from django.conf import settings

from gallery.models import Photo


def add_test_photos():
    test_photos_dir = Path(settings.MEDIA_ROOT) / 'test_photos'
    file_paths = []
    for file_path in test_photos_dir.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(settings.MEDIA_ROOT)
            file_paths.append(str(relative_path))

    for count, path in enumerate(file_paths):
        Photo.objects.create(
            title=f'photo{count}',
            image=path,
            created_by_id=1
        )
