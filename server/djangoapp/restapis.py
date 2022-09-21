from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from .models import CarModel, CarMake, CarDealer, DealerReview
import requests
import json
import datetime


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={"Content-Type": "application/json"},
#                                     auth=HTTPBasicAuth("apikey", api_key))
def get_request(url, **kwargs):
    print("GET from {} ".format(url))
    print(kwargs)
    try:
        # Call get method of requests library with URL and parameters
        # no authentication GET
        response = requests.get(url,
                                headers={"Content-Type": "application/json"},
                                params=kwargs)

        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data

    except:
        # If any error occurs
        print("Network exception occurred")


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print("POST from {} ".format(url))
    print(kwargs)
    try:
        # Call get method of requests library with URL and parameters
        # no authentication GET
        response = response = requests.post(url, params=kwargs, json=payload)

        status_code = response.status_code
        print("With status {} ".format(status_code))
        # json_data = json.loads(response.text)

        if status_code == 201:
            return True
        else:
            return False

    except Exception as e:
        # If any error occurs
        print("Network exception occurred")
        print(e)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        print(json_result)
        # # Get the row list in JSON as dealers
        # # For each dealer object
        for dealer in json_result:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"],
                                   city=dealer["city"],
                                   id=dealer["id"],
                                   lat=dealer["lat"],
                                   long=dealer["long"],
                                   st=dealer["st"],
                                   state=dealer["state"],
                                   zip=dealer["zip"],
                                   short_name=dealer["short_name"],
                                   full_name=dealer["full_name"]
                                   )
            results.append(dealer_obj)

    return results


def get_dealer_by_state_from_cf(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    if json_result:
        print(json_result)
        # # Get the row list in JSON as dealers
        # # For each dealer object
        for dealer in json_result:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"],
                                   city=dealer["city"],
                                   id=dealer["id"],
                                   lat=dealer["lat"],
                                   long=dealer["long"],
                                   st=dealer["st"],
                                   state=dealer["state"],
                                   zip=dealer["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # # Get the row list in JSON as dealers
        # # For each dealer object
        for review in json_result:
            #
            sentiment = analyze_review_sentiments(review["review"])

            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review["dealership"],
                                      review=review["review"],
                                      name=review["name"],
                                      purchase=review["purchase"],
                                      purchase_date=review["purchase_date"],
                                      car_make=review["car_make"],
                                      car_model=review["car_model"],
                                      car_year=review["car_year"],
                                      sentiment=sentiment)

            results.append(review_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(review):
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/ece43bb5-024f-4a93-9a64-efa42d33b0df"
    api_key = "0LOnxFgQLYZjw867YV4Bu3sG6vkQWEgpmqtNFyoLaQrV"

    authenticator = IAMAuthenticator(api_key)

    natural_language_understanding = NaturalLanguageUnderstandingV1(version="2021-08-01", authenticator=authenticator)

    natural_language_understanding.set_service_url(url)

    response = natural_language_understanding.analyze(
        text=review,
        language="en",
        features=Features(
            sentiment=SentimentOptions(
                targets=[review])
        )
    ).get_result()

    # print(response)
    # label = json.dumps(response, indent=2)
    label = response["sentiment"]["document"]["label"]

    return label
