from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings

from django.conf.urls.static import static

from gallery_app.views import my_profile, add_user, add_photo, home, photo_detail, \
    search_photo, photo_edit, photo_delete, photo_text


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name="home"),
    url(r'^rejestracja/$', add_user, name="add-user"),
    url(r'^dodaj/$', add_photo, name="add-photo"),
    url(r'^profil/$', my_profile, name="my-profile"),
    url(r'^zaloguj/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^wyloguj/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^zdjecie/(?P<id>(\d)+)$', photo_detail, name='photo-detail'),
    url(r'^szukaj/$', search_photo, name='search'),
    url(r'^edytuj/(?P<id>(\d)+)$', photo_edit, name='edit'),
    url(r'^usun/(?P<id>(\d)+)$', photo_delete, name='delete'),
    url(r'^napis/(?P<id>(\d)+)$', photo_text, name='text'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
