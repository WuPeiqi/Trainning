"""chouti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web.views import home
from web.views import account

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^index/$', home.index),
    url(r'^fetch_comment/$', home.fetch_comment),
    # url(r'^comment/$', home.comment),
    url(r'^favor/$', home.favor),
    url(r'^upload_image/$', home.upload_image),
    url(r'^check_code/$', account.check_code),
    url(r'^send_msg/$', account.send_msg),
    url(r'^register/$', account.register),
    url(r'^login/$', account.login),
    url(r'^logout/$', account.logout),

    url(r'^add_comment/$', home.add_comment),
    url(r'^show/$', home.show),
    url(r'^', home.index),
]
