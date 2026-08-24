import os

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    help = (
        "Delete the SQLite database file entirely and recreate the schema by "
        "running migrations from scratch. SQLite only."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            action="store_true",
            help="Skip the confirmation prompt.",
        )

    def handle(self, *args, **options):
        db_settings = connections.databases["default"]
        if db_settings["ENGINE"] != "django.db.backends.sqlite3":
            raise CommandError(
                "drop_data only supports the sqlite3 backend this project uses."
            )

        db_path = db_settings["NAME"]

        if not options["noinput"]:
            confirm = input(
                f"This will delete '{db_path}' and rebuild an empty schema. Continue? [y/N] "
            )
            if confirm.lower() != "y":
                self.stdout.write("Cancelled.")
                return

        connections["default"].close()

        if os.path.exists(db_path):
            os.remove(db_path)
            self.stdout.write(f"Removed {db_path}")
        else:
            self.stdout.write(f"{db_path} did not exist, nothing to remove.")

        call_command("migrate")

        self.stdout.write(self.style.SUCCESS("Database dropped and schema recreated."))
