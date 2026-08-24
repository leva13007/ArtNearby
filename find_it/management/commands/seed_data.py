from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from auth_system.models import Profile
from find_it.models import Fabticator, Location, Product, Store

FABRICATORS = ["Faber-Castell", "Koh-i-Noor", "Winsor & Newton", "Staedtler", "Copic"]

COMPANIES = [
    {
        "username": "atelier_paris",
        "company_name": "Atelier Couleur",
        "city": "Paris",
        "address": "15 Rue de Rivoli",
        "phone": "+33142345678",
        "tax_id": "FR10000001",
        "longitude": 2.3522,
        "latitude": 48.8566,
        "store_name": "Atelier Couleur Paris",
        "website": "https://atelier-couleur.example.com",
    },
    {
        "username": "kunstwerk_berlin",
        "company_name": "Kunstwerk",
        "city": "Berlin",
        "address": "22 Unter den Linden",
        "phone": "+493023456789",
        "tax_id": "DE10000002",
        "longitude": 13.4050,
        "latitude": 52.5200,
        "store_name": "Kunstwerk Berlin",
        "website": "https://kunstwerk.example.com",
    },
    {
        "username": "estudio_madrid",
        "company_name": "Estudio de Arte",
        "city": "Madrid",
        "address": "9 Gran Via",
        "phone": "+34915234567",
        "tax_id": "ES10000003",
        "longitude": -3.7038,
        "latitude": 40.4168,
        "store_name": "Estudio de Arte Madrid",
        "website": "https://estudiodearte.example.com",
    },
    {
        "username": "bottega_roma",
        "company_name": "Bottega d'Arte",
        "city": "Rome",
        "address": "4 Via del Corso",
        "phone": "+390645678901",
        "tax_id": "IT10000004",
        "longitude": 12.4964,
        "latitude": 41.9028,
        "store_name": "Bottega d'Arte Roma",
        "website": "https://bottegadarte.example.com",
    },
    {
        "username": "amsterdam_art",
        "company_name": "Amsterdam Art Supplies",
        "city": "Amsterdam",
        "address": "31 Damrak",
        "phone": "+31205678901",
        "tax_id": "NL10000005",
        "longitude": 4.9041,
        "latitude": 52.3676,
        "store_name": "Amsterdam Art Supplies",
        "website": "https://amsterdam-art.example.com",
    },
]

INDIVIDUALS = ["sophie_shopper", "lukas_artlover", "elena_paints"]

PRODUCTS_BY_CATEGORY = {
    "fine_art": [("Oil Paint Set 24 colors", 45.0), ("Canvas Panel 30x40", 12.5)],
    "graphic_art": [("Graphite Pencil Set", 9.0), ("Sketch Marker Set", 38.0)],
    "papeterie": [("Watercolor Paper Pad A4", 14.0), ("Kraft Sketchbook", 7.5)],
    "art_craft": [("Acrylic Paint Pens", 11.0), ("Modeling Clay Set", 16.0)],
}


class Command(BaseCommand):
    help = "Populate the database with sample stores, locations, products and users."

    @transaction.atomic
    def handle(self, *args, **options):
        fabricators = [
            Fabticator.objects.get_or_create(name=name)[0] for name in FABRICATORS
        ]

        store_count = 0
        product_count = 0

        for company in COMPANIES:
            user, created = User.objects.get_or_create(
                username=company["username"],
                defaults={"email": f"{company['username']}@example.com"},
            )
            if created:
                user.set_password("changeme123")
                user.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    "user_type": "company",
                    "company_name": company["company_name"],
                    "address": company["address"],
                    "phone": company["phone"],
                    "tax_id": company["tax_id"],
                },
            )

            store, store_created = Store.objects.get_or_create(
                name=company["store_name"],
                defaults={
                    "description": f"{company['company_name']} — art supplies in {company['city']}.",
                    "phone": company["phone"],
                    "website": company["website"],
                    "creator": user,
                },
            )
            if store_created:
                store_count += 1

            Location.objects.update_or_create(
                store=store,
                defaults={
                    "address": company["address"],
                    "city": company["city"],
                    # length = longitude, width = latitude (see docs/known-issues.md #2)
                    "length": company["longitude"],
                    "width": company["latitude"],
                },
            )

            for category, items in PRODUCTS_BY_CATEGORY.items():
                for name, price in items:
                    product, product_created = Product.objects.get_or_create(
                        store=store,
                        name=name,
                        defaults={
                            "category": category,
                            "price": price,
                            "description": f"{name} available at {store.name}.",
                            "creator": user,
                        },
                    )
                    if product_created:
                        product.fabricator.set(fabricators[:2])
                        product_count += 1

        individual_count = 0
        for username in INDIVIDUALS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": f"{username}@example.com"},
            )
            if created:
                user.set_password("changeme123")
                user.save()
                individual_count += 1
            Profile.objects.update_or_create(user=user, defaults={"user_type": "individual"})

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(fabricators)} fabricators, {store_count} new stores, "
            f"{product_count} new products, {individual_count} new individual users."
        ))
