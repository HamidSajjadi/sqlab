"""shimons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from shimons.Views import user_views, general_views, dashbord_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', user_views.signup, name='signup'),
    path('logout/', user_views.logout_user, name='logout'),
    path('login/', user_views.login_user, name='login'),
    path('dashbord/', dashbord_views.dashbord, name='dashbord'),
    path('dashbord/upload/algorithm/', dashbord_views.upload_algorithm, name='algorithm upload'),
    path('dashbord/upload/patterns/', dashbord_views.upload_patterns, name='pattern upload'),
    path('index/', general_views.index, name='index'),
    path(r'', RedirectView.as_view(url='index/')),

]
