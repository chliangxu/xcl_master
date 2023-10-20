"""
URL configuration for http_xcl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from app_demo import views


# 在urlpatterns中加入path(‘hello/’, views.hello)，第一个元素是匹配的字符串，第二个元素为相对应的视图模块。
# 也就是告诉django所有url/hello/ 的请求都是指向了views.hello 这个视图。hello前不需要加’/‘,因为域名的末尾一定会有’/‘。其中’^‘为严格前匹配,’,浏览器输入http://localhost:8000/hello/a/b 也是可以访问view.hello视图

urlpatterns = [
    path('admin/', admin.site.urls),
    path("hello/", views.hello),
    path("book/", views.test)
    # path("publisher-polls/", include("polls.urls", namespace="publisher-polls")),
]
