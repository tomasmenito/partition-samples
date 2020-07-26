from architect.commands import partition
from django.apps import AppConfig
from django.db import ProgrammingError
from django.db.models.signals import post_migrate

def create_partitions(sender, **kwargs):
    """
    After running migrations, go through each of the models
    in the app and ensure the partitions have been setup
    """
    paths = {model.__module__ for model in sender.get_models()}
    for path in paths:
        try:
            print(partition.run(dict(module=path)))
        except ProgrammingError as e:
            # Possibly because models were just un-migrated or
            # fields have been changed that effect Architect
            print(f"Unable to apply partitions for module '{path}'", e)
        else:
            print(f"Applied partitions for module '{path}'")


class BookstoreConfig(AppConfig):
    name = 'bookstore'

    def ready(self):
        super(BookstoreConfig, self).ready()
        # Hook up Architect to the post migrations signal
        post_migrate.connect(create_partitions, sender=self)