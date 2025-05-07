import requests
import json
from django.conf import settings


class ZarinPalSandbox:
    _payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    _callback_url = "YOUR CALL_BACK_URL"


    def __init__(self ,merchant_id = "7f60de98-a5ce-487a-8bb8-5db1c8d8b970"):
        self.merchant_id = merchant_id


    def payment_request(self, amount, description="پرداختی کاربر"):
        payload = json.dumps({
            "merchant_id": self.merchant_id,
            "amount": str(amount),
            "currency": "IRT",
            "callback_url": self._callback_url,
            "description": description,
            "metadata": {
                "mobile": "09192819212",
                "email": "info@davari@gmail.com"
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(self._payment_request_url, headers=headers, data=payload)
        try:
            response_json = response.json()
            if response.status_code == 200 and response_json.get('data', {}).get('code') == 100:
                return response_json['data']
            else:
                error_msg = response_json.get('errors', {}).get('message', 'Unknown error')
                raise ValueError(f"Zarinpal payment request failed: {error_msg}")
        except json.JSONDecodeError:
            raise ValueError("Invalid response from Zarinpal")
        

    def payment_verify(self,amount,authority):
        payload = json.dumps({
        "merchant_id": self.merchant_id,
        "amount": amount,
        "authority": authority
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.post(self._payment_verify_url, headers=headers, data=payload)
        return response.json()

    def generate_payment_url(self,authority):
        return f"{self._payment_page_url}{authority}"
    
if __name__ == '__main__':
    zaripal = ZarinPalSandbox(merchant_id="7f60de98-a5ce-487a-8bb8-5db1c8d8b970")
    response = zaripal.payment_request(20000)

    print(response)
    input("generate payment_url :")
    print(zaripal.generate_payment_url(response["authority"]))

    input("check the payment :")

    response = zaripal.payment_verify(20000,response["authority"])
    print(response)