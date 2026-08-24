from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from auth_system.models import Profile
from find_it.models import Fabticator, Location, Product, Store


class Command(BaseCommand):
    help = (
        "Delete all Store/Location/Product/Fabticator/Profile rows and non-superuser "
        "users, leaving the database schema and superuser accounts intact."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            action="store_true",
            help="Skip the confirmation prompt.",
        )

    def handle(self, *args, **options):
        if not options["noinput"]:
            confirm = input(
                "This will delete all products, stores, locations, fabricators and "
                "non-superuser users. Continue? [y/N] "
            )
            if confirm.lower() != "y":
                self.stdout.write("Cancelled.")
                return

        with transaction.atomic():
            product_count = Product.objects.count()
            Product.objects.all().delete()

            location_count = Location.objects.count()
            Location.objects.all().delete()

            store_count = Store.objects.count()
            Store.objects.all().delete()

            fabricator_count = Fabticator.objects.count()
            Fabticator.objects.all().delete()

            non_superusers = User.objects.filter(is_superuser=False)
            profile_count = Profile.objects.filter(user__in=non_superusers).count()
            user_count = non_superusers.count()
            non_superusers.delete()

        self.stdout.write(self.style.SUCCESS(
            f"Deleted {product_count} products, {location_count} locations, "
            f"{store_count} stores, {fabricator_count} fabricators, "
            f"{profile_count} profiles, {user_count} non-superuser users."
        ))
