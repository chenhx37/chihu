from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^register/$',views.registerCustomer),
    url(r'^login/$',views.loginUser),
    url(r'^viewCanteens/$',views.viewCanteens),
    url(r'^viewMeals/$',views.viewMeals),
    url(r'^pbtest/$',views.pbtest),
]