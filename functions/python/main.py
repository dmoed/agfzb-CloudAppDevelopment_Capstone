from ibmcloudant.cloudant_v1 import Document, CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):

    databaseName = "reviews"

    try:

        authenticator = IAMAuthenticator(dict["IAM_API_KEY"])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(dict["COUCH_URL"])

        if "__ow_method" in dict and dict["__ow_method"] == "get":

            response = service.post_find(
                db=databaseName,
                selector={'dealership': {'$eq': int(dict['dealerId'])}},
                fields=["id", "name", "dealership", "review", "purchase", "purchase_date", "car_make", "car_model",
                        "car_year"],
            ).get_result()

            if len(response) and len(response['docs']):

                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": response['docs']
                }

            else:

                return {
                    "statusCode": 404,
                    "headers": {"Content-Type": "application/json"},
                    "body": {"message": "Not Found"}
                }

        elif "__ow_method" in dict and dict["__ow_method"] == "post":

            if "review" in dict and len(dict["review"]):

                newDocument = Document(
                    id=str(dict["review"]["id"]),
                    name=dict["review"]["name"],
                    dealership=dict["review"]["dealership"],
                    review=dict["review"]["review"],
                    purchase=dict["review"]["purchase"],
                    another=dict["review"]["another"],
                    purchase_date=dict["review"]["purchase_date"],
                    car_make=dict["review"]["car_make"],
                    car_model=dict["review"]["car_model"],
                    car_year=dict["review"]["car_year"]
                )

                response = service.post_document(db=databaseName, document=newDocument).get_result()

                return {
                    "statusCode": 201,
                    "headers": {"Content-Type": "application/json"},
                }

            else:

                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": {"message": "Bad Request", 'dict': dict}
                }

        else:

            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": {"message": "Bad Request"}
            }

    except Exception as e:

        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": {"message": "Internal Server Error", "error": str(e)}
        }
