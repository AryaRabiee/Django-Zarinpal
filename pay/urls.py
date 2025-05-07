from django.urls import path
from . import views
urlpatterns = [
path('verify/', views.PaymentVerify.as_view(), name='verify'),
# path('success/', TemplateView.as_view(template_name="success.html"), name='success'),
# path('failed/', TemplateView.as_view(template_name="failed.html"), name='failed'),
 ]