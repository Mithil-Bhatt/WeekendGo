"""
URL configuration for PGproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from WeekendApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Login),
    path('login/', views.Login),
    path('signup/', views.signup),
    path('home/',views.home),
    path('logout/', views.Logout),
    path('about/',views.about),
    path('pgs/',views.pgs),
    path('feedback/',views.feedback_view),
    path('thank_you/',views.feedback_thank_you),
    path('paymentdone/',views.paymentdone),
    path('pgbooked/',views.pgbooked),
    path('bookmarks/',views.user_bookmarks),
    path('owners/',views.owners),
    path('pg/<int:pg_id>/',views.singlepg, name='singlepg'),
    path('add_to_bookmarks/<int:pg_id>/', views.add_to_bookmarks, name='add_to_bookmarks'),
    path('bookmark/<int:bookmark_id>/remove_pg/',views.remove_from_bookmark, name='remove_pg'),
] + static(settings.STATIC_URL)