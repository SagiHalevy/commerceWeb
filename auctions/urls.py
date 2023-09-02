from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("createListing", views.createListing, name="createListing"),
    path("productPage/<int:product_id>", views.productPage, name="productPage"),
    path("productPage/<int:product_id>/submitBid", views.submitBid, name="submitBid"),
    path("productPage/<int:product_id>/toggleWatchlist", views.toggleWatchlist, name="toggleWatchlist"),
]

if settings.DEBUG: #routing for media (BASE_DIR/media)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  
