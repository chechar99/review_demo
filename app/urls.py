from django.conf.urls import url
import views

urlpatterns = [
    url(r'^set_review$', views.set_review),
    url(r'^get_review_list$', views.get_review_list),
]
