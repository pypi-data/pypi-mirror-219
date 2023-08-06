try:
    from django.conf.urls.defaults import *
except ImportError:
    from django.conf.urls import *

from blended.djangolint.views import validate

urlpatterns = [
   url(r'^validate/$', validate),    
]
