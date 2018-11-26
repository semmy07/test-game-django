"""
I usually use the "include" from conf.urls, and include url from other apps, but for this project its not useful
"""

from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from game.views import GameView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', GameView.as_view())
]
