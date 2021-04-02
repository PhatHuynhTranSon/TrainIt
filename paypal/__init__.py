from paypalcheckoutsdk.core import PayPalHttpClient
from paypalcheckoutsdk.core.environment import SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest

class CreatePaymentException(Exception):
    pass

class CapturePaymentException(Exception):
    pass

class PayPalHandler:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.create_environment()
        self.create_client()

    def create_environment(self):
        '''
        Create sandbox environment for PayPal
        '''
        self.env = SandboxEnvironment(
            client_id=self.client_id,
            client_secret=self.client_secret
        )

    def create_client(self):
        '''
        Create the client
        '''
        self.client = PayPalHttpClient(self.env)

    def capture_order(self, order_id, debug=True):
        request = OrdersCaptureRequest(order_id)
        response = self.client.execute(request)

        if debug:
            print("Status Code: ", response.status_code)
            print("Status: ", response.result.status)
            print("Order ID: ", response.result.id)
            print("Links: ")

            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))

            print("Capture Ids:")
            for purchase_unit in response.result.purchase_units:
                for capture in purchase_unit.payments.captures:
                    print("\t", capture.id)
        
        return self.parse_response(response)

    def parse_response(self, response):
        return {
            "status_code": response.status_code,
            "status": response.result.status,
            "order_id": response.result.id,
            "links": [ { "rel": link.rel, "href": link.href, "method": link.method } for link in response.result.links ],
            "reference_id": response.result.purchase_units[0].reference_id,

            "buyer": {
                "email": response.result.payer.email_address,
            }
        }

    def is_completed(self, response):
        return response["status"] == "COMPLETED"


def create_paypal_handler():
    client_id = "AT1hwSRViFlyWiFet1Hv73JCbilrC0jRnqL_07UUQJ-KAJTaadEULNvb3bHziVd6MroAv0SEE7DJGcvP"
    client_secret = "EB7bpq1n4itWiywSx7Y2xHIuMHv7M1sCI6bDYzD3LhtboB8FrUMir1fMWz0d0d0HzDcLRu0BIo98I6wh"
    paypal_handler = PayPalHandler(client_id, client_secret)
    return paypal_handler  
