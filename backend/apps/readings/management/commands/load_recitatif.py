"""

Management command to reload the db

"""
from pathlib import Path
import re

from django.core.management.base import BaseCommand


from config.settings.base import PROJECT_ROOT
from apps.readings.models import Document, Segment


class Command(BaseCommand):
    """ Initial loader to get a rough copy of Recitatif into the database,
        split more-or-less by paragraph (will need some manual intervention).
        Might be useful to generalize this and make it into a generic loader
        for the system at some point...
    """

    def handle(self, *args, **options):
        recit_path = Path(PROJECT_ROOT) / 'analysis' / 'data' / 'recitatif.txt'

        with open(recit_path, encoding='utf-8') as recit_file:
            recit_text = recit_file.readlines()

        recit_doc = Document(
            title='Recitatif',
            author='Toni Morrison',
        )
        recit_doc.save()

        i = 0
        for line in recit_text:
            # Skip lines that are empty newlines
            stripped_line = re.sub(r'\s+', '', line)
            if not stripped_line:
                continue

            seg = Segment(
                text=line,
                sequence=i,
                document=recit_doc,
            )
            seg.save()
            i += 1
