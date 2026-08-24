# ArtNearby — відомі проблеми

## Актуальні

1. **Реєстрація падає з 500 при повторній реєстрації того ж username/email.**
   `auth_system/forms.py::CustomRegistrationForm` не перевіряє унікальність (`clean_username`/`clean_email`), а `auth_system/views.py::register` викликає `User.objects.create_user()` без обробки `IntegrityError`.

2. **Поля координат у `Location` названо `length`/`width`.**
   `find_it/models.py` — мається на увазі довгота/широта, назви незрозумілі й не відповідають прийнятим `latitude`/`longitude`. Працює коректно, потребує лише перейменування (і міграції).

3. **⚠️ Security: відсутня перевірка власності на Update/Delete у Store й на Update у Product.**
   `ProductUpdateView`, `StoreUpdateView`, `StoreDeleteView` (`find_it/views.py`) захищені лише декоратором `company_required` (`find_it/decorators.py`) — перевіряють роль (`user_type == 'company'`), але не власність. Будь-яка залогінена компанія може відредагувати чи видалити магазин або товар **іншої** компанії, підставивши чужий `pk` в URL (наприклад `/product/<pk>/update/`). Порівняй з `ProductDeleteView`, де `UserIsOverMixin` (`find_it/mixins.py`) застосований коректно й перевіряє `creator == request.user` — той самий підхід треба поширити на три інші view. Див. також [Access control](./about.md#access-control-acl) в `about.md`.

4. **⚠️ Security: компанія може створити товар у чужому магазині.**
   `ProductForm.Meta.fields` (`find_it/forms.py:18`) включає `"store"` як звичайний `ModelChoiceField` — queryset нічим не обмежений, тобто випадаючий список у формі "Add Product" (`templates/find_it/products/products_management.html:35`) показує **всі** магазини всіх компаній, а не тільки свої. `ProductsManagementView.post` (`find_it/views.py:68-74`) зберігає `product.creator = request.user`, але не перевіряє, що обраний `store.creator == request.user`. Показово, що `ProductForm.__init__` приймає `user`-параметр (`find_it/forms.py:20-21`), який ніде не використовується — схоже, фільтрацію почали робити й не довели до кінця. Наслідок: компанія A може додати товар у магазин компанії B.

5. **Модалка редагування товару (`products_management.html`) не працює для полів `fabricator` і `store`.**
   JS (рядки 166-189) підставляє в приховані поля модалки значення з `data-product-fabricator="{{ product.fabricator }}"` і `data-product-store="{{ product.store }}"` — але `{{ product.fabricator }}` рендерить рядкове представлення M2M-менеджера (не список ID), а `{{ product.store }}` рендерить `Store.__str__()`, тобто **назву** магазину, а не його `pk`. При збереженні `ProductForm` очікує на цих полях primary key(-и), тому валідація впаде. Поле `editCategory` (рядок 135) — вільний `<textarea>`, хоча `category` — `ChoiceField` з фіксованими варіантами (`fine_art`/`graphic_art`/...), тож будь-яке відхилення від точного значення теж провалить валідацію. Додатково `editImage` має `required` (рядок 127) — отже відредагувати товар без повторного завантаження зображення неможливо навіть через цю форму.

6. **На сторінці редагування товару (`product_update.html`) немає `enctype="multipart/form-data"`.**
   `<form method="post">` (рядок 7) без `enctype` — файлові поля (`image`) браузер просто не відправить, навіть якщо форма коректно провалідується. Те саме стосується будь-якого майбутнього ModelForm з файловим полем, відрендереного через цей шаблон.

7. **`Store.phone = models.IntegerField()`.**
   `find_it/models.py:10`. Телефонні номери з провідним нулем (`+380 50…`) або довші за ~10 цифр (стандартний міжнародний формат) або не влазять в 32-бітний `IntegerField`, або втрачають початковий `0`/`+`. Поле мало б бути `CharField`.

8. **`LOGIN_URL = "/admin/login/"` замість власної сторінки логіну.**
   `django_where/settings.py:131`. `LoginRequiredMixin` на `ProductsManagementView`, `ProductUpdateView`, `StoreManagementView`, `StoreUpdateView`, `StoreDeleteView` (`find_it/views.py`) редіректить незалогінених користувачів на Django admin-логін замість `auth_system`-івської сторінки `/login/` — плутає користувача сторонньою адмінкою замість власного UI.

## Відкриті питання дизайну (потребують рішення)

1. **`Product.fabricator` — `ManyToManyField`, а не `ForeignKey`?**
   `find_it/models.py:41`: `fabricator = models.ManyToManyField(Fabticator)`. Кожен `Product` уже прив'язаний до конкретного `Store` (`store = ForeignKey(Store)`) — тобто це конкретний товар у конкретному магазині, а не абстрактна позиція. Для конкретного товару зазвичай є один виробник (олівець Faber-Castell не буває водночас і Faber-Castell, і Koh-i-Noor).

   M2M має сенс, якщо `Product` іноді означає "набір" з кількох брендів (наприклад, стартовий набір художника: олівці одного бренду + папір іншого). Якщо ж кожен `Product` — завжди один виріб одного бренду, правильніша модель — `fabricator = models.ForeignKey(Fabticator)` (1—N: товар → один виробник).

   **Треба вирішити:** чи `Product` коли-небудь представляє мультибрендовий набір. Якщо ні — змінити на `ForeignKey` (потребує міграції даних, бо зараз це M2M-таблиця).

## Нещодавно виправлено

- ~~`requirements.txt` без Pillow~~ — `ImageField` вимагає Pillow, тепер вказано в `requirements.txt`.
- ~~Dockerfile: неправильний `ENTRYPOINT`~~ — було `manga.wsgi`, виправлено на `django_where.wsgi`.
- ~~`ProductDeleteView.success_url` посилався на неіснуючий роут `find_it:product-management`~~ (`find_it/views.py`) — правильна назва `find_it:products-management` (множина); падало з `NoReverseMatch` при успішному видаленні товару, виправлено. Знайдено при складанні [`routes.md`](./routes.md).
