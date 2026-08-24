# ArtNearby — карта роутів

Повний список URL-адрес сайту: хто може заходити, який view і темплейт відповідають, куди редіректить у разі відмови. Для загального контексту (ролі, user flow) — [`about.md`](./about.md); для деталей доступу — розділ [Access control](./about.md#access-control-acl).

Обидва urlconf (`find_it.urls`, `auth_system.urls`) підключені в корені (`django_where/urls.py`), тому шлях у браузері — без префіксу. `find_it.urls` має `app_name = "find_it"` (в шаблонах/redirect викликається як `find_it:route-name`), `auth_system.urls` — без namespace (`route-name` напряму).

## Публічні (без логіну)

| Шлях | Name | View | Темплейт | Примітка |
|---|---|---|---|---|
| `/` | `index` / `find_it:index` | `find_it.views.index` | `find_it/index.html` | Головна: 3 картки + 6 випадкових товарів. Роут визначений в **обох** urlconf-ах (однаковий view) — не давайте їм розійтись. |
| `/products_list/` | `find_it:list-product` | `ProductListView` | `find_it/products/product_list.html` | Повний список товарів, `?category=` фільтрує. |
| `/<pk>/` | `find_it:product-detail` | `ProductDetailView` | `find_it/products/product_detail.html` | Картка товару за id. |
| `/register/` | `register` | `auth_system.views.register` | `find_it/auth_system/registrate.html` | Реєстрація (individual/company). |
| `/login/` | `login` | `auth_system.views.login_view` | `find_it/auth_system/login.html` | Логін. |
| `/logout/` | `logout` | `auth_system.views.logout_view` | — (redirect) | Логаут, редірект на `index`. |
| `/profile/` | `profile` | `auth_system.views.profile_view` | `find_it/profile_show.html` | ⚠️ Не захищений — рендериться навіть для анонімного користувача (шаблон покладається на `{{ user }}` з контекст-процесора). |
| `/admin/` | — | Django admin | — | Логін через `/admin/login/` — це ж значення `LOGIN_URL` (див. нижче). |

## Тільки для компаній (`Profile.user_type == 'company'`)

Захищені `LoginRequiredMixin` + `@company_required` (`find_it/decorators.py`): неавторизованих редіректить на `login`, авторизованих individual-користувачів — на `index`.

| Шлях | Name | View | Темплейт | Перевірка власності |
|---|---|---|---|---|
| `/products/manage/` | `find_it:products-management` | `ProductsManagementView` | `find_it/products/products_management.html` | Список фільтрується по `creator=request.user` — свій список видно, чужі товари через цей роут недосяжні. |
| `/products/<pk>/update/` | `find_it:product-update` | `ProductUpdateView` | `find_it/products/product_update.html` | ⚠️ **Немає** — будь-яка компанія може відредагувати чужий товар, підставивши `pk`. Див. [`known-issues.md`](./known-issues.md) #3. |
| `/products/<pk>/delete/` | `find_it:product-delete` | `ProductDeleteView` | `find_it/products/product_delete_confirmation.html` | Є — `UserIsOverMixin` перевіряє `creator == request.user`, інакше `403`. |
| `/stores/manage/` | `find_it:store-management` | `StoreManagementView` | `find_it/store/store_management.html` | Список фільтрується по `creator=request.user`. |
| `/stores/<pk>/update/` | `find_it:store-update` | `StoreUpdateView` | `find_it/store/store_update_form.html` | ⚠️ **Немає** — те саме, що й product-update. Див. [`known-issues.md`](./known-issues.md) #3. |
| `/stores/<pk>/delete/` | `find_it:store-delete` | `StoreDeleteView` | `find_it/store/store_delete_confirmation.html` | ⚠️ **Немає** — те саме. Див. [`known-issues.md`](./known-issues.md) #3. |

## Гейтинг незалогінених — нюанс `LOGIN_URL`

`LOGIN_URL = "/admin/login/"` (`django_where/settings.py`) — тому `LoginRequiredMixin` на всіх п'яти management-view вище кидає незалогіненого користувача на **сторінку логіну Django admin**, а не на власну `/login/`. `@company_required` (для залогінених, але не-компаній) редіректить коректно, на `login`. Див. [`known-issues.md`](./known-issues.md) #8.

## Медіа

`MEDIA_URL = /media/` віддає `MEDIA_ROOT/product_images/*` напряму через `static()`-хелпер у `django_where/urls.py` — лише в dev-режимі (`DEBUG=True`), у продакшені так само не буде працювати без окремого serving.
