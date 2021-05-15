from django.urls import path
from main import views


urlpatterns = [
    path('categories/', views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:pk>', views.CategoryViewSet.as_view({'get': 'retrieve', 'delete': 'destroy',
                                                               'put': 'update'})),
    path('categories/<int:pk>/product', views.ProductViewSet.as_view({'get': 'retrieve'})),
    path('product/', views.ProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('product/<int:pk>', views.ProductViewSet.as_view({'delete': 'destroy', 'get': 'select', 'put': 'update'})),
    path('cart/', views.CartAPIView.as_view()),
    path('cart/<int:pk>/update', views.CartAPIView.as_view()),
    path('cart/<int:pk>', views.cart_detail),
    path('orders/', views.orders),
    path('orders/<int:pk>', views.OrderAPIView.as_view()),
]
