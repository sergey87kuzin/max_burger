import datetime
import hashlib
import hmac
import json
import uuid
from http import HTTPStatus
from itertools import chain
from typing import List, Optional, Dict
from urllib.parse import quote_plus

from fastapi.responses import RedirectResponse
import requests
from sqlalchemy.ext.asyncio import AsyncSession

from api_models.orders import OrderToShow
from global_constants import PaymentStatus
from handlers.orders import get_order_by_id, update_order
from settings import SITE_DOMAIN, SBER_USERNAME, SBER_PASSWORD, ENVIRONMENT, CALLBACK_TOKEN, OPERATOR_PHONE, PHONE, INN, \
    MERCHANT_LOGIN, LETTER_FOR_SBER_ORDER


class SberPaymentsService:
    """
    https://securepayments.sberbank.ru/wiki/doku.php/integration:api:rest:requests:register
    https://securepayments.sberbank.ru/wiki/doku.php/integration:api:rest:requests:register_cart
    https://securepayments.sberbank.ru/wiki/doku.php/integration:api:callback:start

    При интеграции уточнить налоговые коды
    """

    SITE_HOST = SITE_DOMAIN

    PAYMENT_HOST_PROD = "https://securepayments.sberbank.ru/"
    PAYMENT_HOST_DEV = "https://3dsec.sberbank.ru/"

    ORDER_REGISTRATION_LINK = "payment/rest/register.do"
    ORDER_STATUS_LINK = "payment/rest/getOrderStatusExtended.do"

    HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

    DEFAULT_CURRENCY_CODE = 643

    DEFAULT_TAX_SYSTEM = 2
    """
    0 - общая;
    1 - упрощённая, доход;
    2 - упрощённая, доход минус расход;
    3 - единый налог на вменённый доход;
    4 - единый сельскохозяйственный налог;
    5 - патентная система налогообложения.
    """

    DEFAULT_MEASURE = 0  # Для штучных товаров 0

    DEFAULT_COUNTRY_CODE = 810

    DEFAULT_TAX_TYPE = 0
    """
    Ставка НДС, доступны следующие значения:
    0 – без НДС;
    1 – НДС по ставке 0%;
    2 – НДС чека по ставке 10%;
    4 – НДС чека по расчетной ставке 10/110;
    6 - НДС чека по ставке 20%;
    7 - НДС чека по расчётной ставке 20/120.
    """

    DEFAULT_PAYMENT_METHOD = 4
    """
    Тип оплаты возможны следующие значения:
    1 - полная предварительная оплата до момента передачи предмета расчёта;
    2 - частичная предварительная оплата до момента передачи предмета расчёта;
    3 - аванс;
    4 - полная оплата в момент передачи предмета расчёта;
    5 - частичная оплата предмета расчёта в момент его передачи с последующей оплатой в кредит;
    6 - передача предмета расчёта без его оплаты в момент его передачи с последующей оплатой в кредит;
    7 - оплата предмета расчёта после его передачи с оплатой в кредит.
    """

    DEFAULT_PAYMENT_OBJECT = 1
    """
    Тип оплачиваемой позиции, возможны следующие значения:
    1 - товар;
    4 - услуга;
    Остальные позиции не перечислены за ненадобностью
    """

    def __init__(self, order: OrderToShow):
        self.USERNAME = SBER_USERNAME
        self.API_USERNAME = self.USERNAME + "-api"
        self.PASSWORD = SBER_PASSWORD
        self.CALLBACK_TOKEN = CALLBACK_TOKEN
        self.CALLBACK_URL = SITE_DOMAIN + "/api/payments/callback/"
        self.OPERATOR_PHONE = OPERATOR_PHONE
        self.PHONE = PHONE
        self.INN = INN
        self.SUCCESS_URL = SITE_DOMAIN + "payment_result/?success=true"
        self.FAIL_URL = SITE_DOMAIN + "payment_result/?success=false"
        self.PAYMENT_FAILED_NOTIFICATION_URL = SITE_DOMAIN + "/api/payments/callback/"
        self.MERCHANT_LOGIN = MERCHANT_LOGIN
        self.order = order
        self.response = {}
        self.cart_items = []

        if ENVIRONMENT in ["local", "dev"]:
            self.__ORDER_STATUS_LINK = self.PAYMENT_HOST_DEV + self.ORDER_STATUS_LINK
            self.__ORDER_REGISTRATION_LINK = self.PAYMENT_HOST_DEV + self.ORDER_REGISTRATION_LINK
        else:
            self.__ORDER_STATUS_LINK = self.PAYMENT_HOST_PROD + self.ORDER_STATUS_LINK
            self.__ORDER_REGISTRATION_LINK = self.PAYMENT_HOST_PROD + self.ORDER_REGISTRATION_LINK

    def __create_cart_items(self) -> List[dict]:
        for position, product_in_order in enumerate(self.order.products, start=1):
            cart_item = {
                "positionId": position,
                "name": product_in_order.product.name[:120],
                "quantity": {
                    "value": product_in_order.quantity,
                    "measure": self.DEFAULT_MEASURE,
                },
                "itemCurrency": self.DEFAULT_CURRENCY_CODE,
                "itemCode": str(product_in_order.product.id),
                "tax": {"taxType": self.DEFAULT_TAX_TYPE},
                "itemPrice": int(product_in_order.price_with_sale or product_in_order.price) * 100,
                "itemAttributes": {"attributes": self.__get_items_attributes()},
            }
            self.cart_items.append(cart_item)
        self.__add_delivery_item()
        return self.cart_items

    def __get_items_attributes(self) -> List[dict]:
        return [
            {"name": "paymentMethod", "value": self.DEFAULT_PAYMENT_METHOD},
            {"name": "paymentObject", "value": self.DEFAULT_PAYMENT_OBJECT},
        ]

    def __get_post_address(self) -> str:
        street = self.order.street
        house = self.order.house_number
        apartment = self.order.apartment
        full_address = (
                f"{street if street else ''} {house if house else ''}"
                + f"{(' кв. ' + str(apartment)) if apartment else ''}"
        )
        return full_address

    def __get_return_url(self):
        return self.SITE_HOST + self.SUCCESS_URL + f"?order_id={self.order.id or self.order.id}"

    def get_payment_url(self) -> Optional[str]:
        if self.order is None:
            raise AttributeError("Этот метод ")
        payload = {
            "userName": self.API_USERNAME,
            "password": self.PASSWORD,
            "orderNumber": f"{self.order.id}{LETTER_FOR_SBER_ORDER}",
            "amount": int(self.order.total_price) * 100,  # в копейках
            "currency": self.DEFAULT_CURRENCY_CODE,
            "returnUrl": self.SITE_HOST + f"/orders/{self.order.id}/?newOrder=true&statusPay=success",
            "failUrl": self.SITE_HOST + f"/orders/{self.order.id}/?newOrder=true&statusPay=fail",
            "dynamicCallbackUrl": self.CALLBACK_URL,
            "pageView": "MOBILE",
            "merchantLogin": self.MERCHANT_LOGIN,
            "delivery_info": json.dumps(
                {
                    "delivery_city": self.order.city,
                    "delivery_country": self.DEFAULT_COUNTRY_CODE,
                    "delivery_type": self.order.delivery_type,
                    "post_address": self.__get_post_address(),
                }
            ),
            "sessionTimeoutSecs": 60 * 60,  # час время жизни ссылки на оплату
            "orderBundle": json.dumps(
                {
                    "orderCreationDate": self.order.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                    "customerDetails": {
                        "email": self.order.user.username,
                        "phone": self.order.user.phone,  # ^((+7|7|8)?([0-9]){10})$
                    },
                    "cartItems": {"items": self.__create_cart_items()},
                }
            ),
            "taxSystem": self.DEFAULT_TAX_SYSTEM,
        }

        response = requests.post(
            url=self.__ORDER_REGISTRATION_LINK,
            data=payload,
            headers=self.HEADERS,
            verify="Cert_CA.pem"
        )
        if response.status_code == HTTPStatus.OK:
            self.response = response.json().get("formUrl", None)
            return self.response
        return None

    def __add_delivery_item(self) -> None:
        delivery_item = {
            "positionId": len(self.cart_items) + 1,
            "name": "Доставка",
            "quantity": {
                "value": 1,
                "measure": self.DEFAULT_MEASURE,
            },
            "itemAmount": self.order.delivery_price * 100,
            "itemCurrency": self.DEFAULT_CURRENCY_CODE,
            "itemCode": uuid.uuid4().hex,
            "tax": {"taxType": self.DEFAULT_TAX_TYPE},
            "itemPrice": self.order.delivery_price * 100,
            "itemAttributes": {"attributes": self.__get_items_attributes()},
        }
        self.cart_items.append(delivery_item)

    def calculate_hashsum(self, data: Dict) -> bool:
        checksum = data.pop("checksum", None)

        hexadecimal_string = (
            hmac.new(
                key=bytes(self.CALLBACK_TOKEN, "utf-8"),
                msg=bytes(";".join(chain.from_iterable(list(sorted(data.items())))) + ";", "utf-8"),
                digestmod=hashlib.sha256,
            )
            .hexdigest()
            .upper()
        )

        return hmac.compare_digest(checksum, hexadecimal_string)

    async def get_order_from_callback_request(self, data: Dict, session: AsyncSession):
        if not self.calculate_hashsum(data):
            return False
        order_id = data["orderNumber"][:-1]
        order = await get_order_by_id(order_id, session)
        if order is None:
            return False
        return order

    async def handle_success_callback_data(self, data: dict, session: AsyncSession) -> bool:
        if data:
            # if self.calculate_hashsum(request.data):
            order_id = data.get("orderNumber")[:-1]
            order = await get_order_by_id(order_id, session)
            payment_status = PaymentStatus.NOT_PAID
            if order is None:
                return False
            else:
                payment_state = data.get("paymentState")  # состояние транзакции
                operation = data.get("operation")
                operation_status = data.get("status")

                format_string = "%d.%m.%Y %H:%M:%S"
                if operation == "deposited":
                    # deposited - операция завершения;
                    if operation_status == "1":
                        # 1 - операция прошла успешно;
                        payment_status = PaymentStatus.PAID
                        payment_date = data.get("paymentDate")

                        order.paid_amount = data.get("depositedAmount")
                    else:
                        # 0 - операция прошла неуспешно;
                        payment_status = PaymentStatus.NOT_PAID

                elif operation == "declinedByTimeout":
                    if operation_status == "1":
                        payment_status = PaymentStatus.NOT_PAID

                elif operation == "reversed":
                    if operation_status == "1":
                        payment_status = PaymentStatus.NOT_PAID

                elif operation == "refunded":
                    if operation_status == "1":
                        payment_status = PaymentStatus.NOT_PAID

                if payment_state == "started":
                    #  Заказ создан
                    pass
                elif payment_state == "payment_void":
                    # Заказ отменён
                    pass
                elif payment_state == "payment_declined":
                    # Средства по заказу возвращены
                    pass
            # order.save(update_fields=("payment_status", "status", "payment_date", "paid_amount"))
            update_data = {
                "payment_status": payment_status
            }
            await update_order(order_id, update_data, session)
            return True

        return False

    async def handle_failed_callback(self, request_data: dict, session: AsyncSession):
        """request_data - request.GET"""
        fail_url = self.FAIL_URL
        order_id = None if not request_data.get("InvoiceId", None) else request_data.get("InvoiceId")
        if order_id:
            await update_order(order_id, {"payment_status": PaymentStatus.NOT_PAID}, session)

            return RedirectResponse(fail_url + "?order_id={}".format(order_id))

        order_id = request_data.get("order_id")
        if order_id:
            order = await get_order_by_id(order_id, session)
            if not bool(order):
                return RedirectResponse(fail_url + "?order_id={}".format(order_id))

            payment_url = SberPaymentsService(order).get_payment_url()
            if payment_url:
                update_data = {
                    "payment_url": payment_url,
                    "created_at": datetime.datetime.now()
                }
                await update_order(order_id, update_data, session)
                return RedirectResponse(fail_url + "?payment_url={}&order_id={}".format(payment_url, order_id))

            return RedirectResponse(fail_url + "?order_id={}".format(order_id))

        return RedirectResponse(fail_url + "?order_id={}".format(order_id))
