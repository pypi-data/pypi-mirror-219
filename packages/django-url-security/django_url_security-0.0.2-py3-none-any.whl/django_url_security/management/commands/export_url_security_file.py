from django.core.management.base import BaseCommand

from django_url_security.core import get_spec_file_path
from django_url_security.generate_permission_spec_file import (
    print_permission_spec_file,
)


class Command(BaseCommand):
    help = f'Writes the current permission specifications to {get_spec_file_path()}'

    def handle(self, *args, **options):
        print_permission_spec_file()
        return f'Successfully wrote permission spec file to {get_spec_file_path()}'
