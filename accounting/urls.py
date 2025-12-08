from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('overview/', views.overview_view, name='overview'),
    path('liquidation-form/', views.liquidation_form_view, name='liquidation_form'),
    path('debit-memo/', views.debit_memo_view, name='debit_memo'),
    path('check-voucher/', views.check_voucher_view, name='check_voucher'),
    path('disbursement/', views.disbursement_view, name='disbursement'),
]