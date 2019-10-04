"""

Management command to reload the db

"""
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.management import call_command

from config.settings.base import DB_PATH, BACKEND_DIR


class Command(BaseCommand):
    """ Implements a Django management command to reload the db """
    help = 'Deletes your local db and reconstructs it from backend/data/db.json'

    def handle(self, *args, **options):
        db_json_path = Path(BACKEND_DIR) / 'data' / 'db.json'

        if os.path.exists(DB_PATH):
            print('\nDeleting existing db...')
            os.remove(DB_PATH)
            print('Done!')

        print('\nRebuilding db from migrations...')
        call_command('migrate')
        print('Done!')

        print('\nLoading data from db.json...')
        call_command('loaddata', db_json_path)
        print('Done!')

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully reloaded the database from {DB_PATH}')
        )
