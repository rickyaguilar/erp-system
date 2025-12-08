from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.request_list_view, name='request_list'),  # Main inventory page
    path('request-form/', views.request_form_view, name='request_form'),
    path('approve-request/<int:request_id>/', views.approve_request_view, name='approve_request'),
    path('request/<int:request_id>/details/', views.request_details_api, name='request_details_api'),
    path('purchase/', views.purchase_view, name='purchase'),
    path('purchase/approve/<int:request_id>/', views.approve_purchase_view, name='approve_purchase'),
    path('purchase/reject/<int:request_id>/', views.reject_purchase_view, name='reject_purchase'),
    path('delivery/', views.delivery_view, name='delivery'),
    path('masterlist/', views.masterlist_view, name='masterlist'),
]