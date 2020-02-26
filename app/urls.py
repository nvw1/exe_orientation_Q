from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
               path('', views.index, name='index'),
               path('health', views.health, name='health'),
               path('404', views.handler404, name='404'),
               path('500', views.handler500, name='500'),
               path('redirect', views.redirect, name='redirect'),
                path('admin/', admin.site.urls),
             path('gamemaster',views.gamemaster,name='gamemaster'),
                path('studentview',views.studentview,name='studentview'),
                path('hint',views.hint,name="hint")
               ]
urlpatterns += staticfiles_urlpatterns()