# ArtNearby (where_is_it)

Сайт для пошуку матеріалів для малювання поруч з тобою: магазини художніх товарів додають свої точки продажу та товари, а користувачі шукають і фільтрують їх за категоріями.

Детальніше про продукт, ролі користувачів і user flow — [`docs/about.md`](docs/about.md); поточний статус фіч — [`docs/roadmap.md`](docs/roadmap.md).

## Запуск через Docker (рекомендовано)

Потрібно встановити тільки [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Compose йде разом з ним).

Запустити проєкт:

```bash
docker compose up --build
```

Сайт буде доступний на http://localhost:8000

Зупинити:

```bash
docker compose down
```

`--build` потрібен лише при першому запуску або після зміни `Dockerfile`/`requirements.txt` — для звичайного старту достатньо `docker compose up`.

Створити адміна (для доступу до `/admin/`):

```bash
docker compose exec web python manage.py createsuperuser
```

## Запуск без Docker

Потрібно: Python 3.12+.

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
