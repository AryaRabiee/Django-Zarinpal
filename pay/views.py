from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import View
from .models import Payment , PaymentStatusType
from django.urls import reverse_lazy
from django.shortcuts import redirect,get_object_or_404
from .zarinpal_client import ZarinPalSandbox
from .models import Order , OrderStatusType


class PaymentVerify (View):

    def get(self,request,*args,**kwargs):
        authority_id = request.GET.get("Authority")
        status = request.GET.get("status")

        payment_obj = get_object_or_404(Payment , authority_id = authority_id)
        zarinpal = ZarinPalSandbox()
        response = zarinpal.payment_verify(int(payment_obj.amount) , payment_obj.authority_id)

        status = response.get("data", {}).get("code")
        
        if status == 100 or status == 101:
            payment_obj.ref_id = response.get("data", {}).get("ref_id")
            payment_obj.response_code = response.get("data", {}).get("code")
            payment_obj.status = PaymentStatusType.success.value
            payment_obj.response_json = response
            payment_obj.save()
            order = Order.objects.get(payment = payment_obj)
            order.status = OrderStatusType.success.value
            order.save()
            return redirect(reverse_lazy("SUCCESS PAGE"))
        
        else:
            payment_obj.ref_id = response.get("data", {}).get("ref_id")
            payment_obj.response_code = response.get("data", {}).get("code")
            payment_obj.status = PaymentStatusType.failed.value
            payment_obj.response_json = response
            payment_obj.save()
            order = Order.objects.get(payment = payment_obj)
            order.status = OrderStatusType.canceled.value
            order.save()
            return redirect(reverse_lazy("FAILED PAGE"))       
