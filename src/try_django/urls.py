"""try_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from .views import (
    home_page,
    about_page,
    example_page,
    convention_page,
    hello_page,
    better_page,
    contact_page,
    login_page
)

from blog.views import (
    blog_post_detail_page_oldest,
    # blog_post_detail_page_older,
    # blog_post_detail_page,
    # blog_post_list_view,
    blog_post_create_view,
    # blog_post_retrieve_view,
    # blog_post_update_view,
    # blog_post_delete_view
)

from searches.views import search_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('about/', about_page),
    path('example/', example_page),
    path('convention/', convention_page),
    path('hello/', hello_page),
    path('better/', better_page),

    path('contact/', contact_page),
    path('login/', login_page),

    path('search/', search_view),

    # These 2 url patterns are conflicting with blog/<str:slug>
    path('blog-new/', blog_post_create_view),
    path('blogold/', blog_post_detail_page_oldest),

    # We created a new urls.py in blog dir, so we can move them
    # path('blog/<int:post_id>/', blog_post_detail_page_older), # This is older version
    # path('blog/<str:slug>/', blog_post_detail_page), # This is newer but same as below!

    # path('blog/', blog_post_list_view),
    # path('blog/<str:slug>/', blog_post_retrieve_view),
    # path('blog/<str:slug>/edit/', blog_post_update_view),
    # path('blog/<str:slug>/delete/', blog_post_delete_view),
    path('blog/', include('blog.urls')),
]


if settings.DEBUG:
    # test mode
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

