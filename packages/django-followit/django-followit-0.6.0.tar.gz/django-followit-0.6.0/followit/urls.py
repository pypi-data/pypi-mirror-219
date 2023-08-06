try:
    from django.conf.urls import url as re_path # Django 1.11
except ImportError:
    from django.urls import re_path

from . import views as FollowitViews

urlpatterns = [
    re_path(
        r'^follow/(?P<model_name>\w+)/(?P<object_id>\d+)/$',
        FollowitViews.follow_object,
        name = 'follow_object'
    ),
    re_path(
        r'^unfollow/(?P<model_name>\w+)/(?P<object_id>\d+)/$',
        FollowitViews.unfollow_object,
        name = 'unfollow_object'
    ),
    re_path(
        r'^toggle-follow/(?P<model_name>\w+)/(?P<object_id>\d+)/$',
        FollowitViews.toggle_follow_object,
        name='toggle_follow_object'
    )
]
