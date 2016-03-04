from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^register/$',views.registerCustomer),
    url(r'^pbtest/$',views.pbtest),
]