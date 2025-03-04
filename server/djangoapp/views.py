import logging
import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_state_from_cf, post_request
from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
# Create an `about` view to render a static about page
def home_request(request):
    context = {}
    return render(request, "djangoapp/index.html", context)

def about_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/about.html", context)

# Create a `contact` view to return a static contact page
def contact_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/contact.html", context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST["username"]
        password = request.POST["psw"]
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect("djangoapp:index")
        else:
            # If not
            return render(request, "djangoapp/index.html", context)
    else:
        return render(request, "djangoapp/index.html", context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)
    # If it is a POST request
    elif request.method == "POST":
    
        username = request.POST["username"]
        password = request.POST["password"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        user_exist = False
        
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, password=password)
            login(request, user)
            # redirect to course homepage
            return redirect("djangoapp:index")
        else:
            return render(request, "djangoapp/registration.html", context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/apptastic-nv_djangoserver-space/api/dealership"

        dealers_list = get_dealers_from_cf(url)
        context["dealers_list"] = dealers_list

        return render(request, "djangoapp/index.html", context)

def get_dealerships_by_state(request):
    context = {}
    if request.method == "GET" and len(request.GET["state"]):

        state = request.GET["state"]

        url = "https://us-east.functions.appdomain.cloud/api/v1/web/apptastic-nv_djangoserver-space/api/dealership"

        dealers_list = get_dealer_by_state_from_cf(url, state)
        context["dealers_list"] = dealers_list

        return render(request, "djangoapp/index.html", context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":

        url = "https://us-east.functions.appdomain.cloud/api/v1/web/apptastic-nv_djangoserver-space/api/review"

        reviews_list = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        reviews_list.reverse()

        context["reviews_list"] = reviews_list
        context['dealer_id'] = dealer_id

        return render(request, "djangoapp/dealer_details.html", context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):

    # fetch cars
    queryset = CarModel.objects.select_related('manufacturer')

    context = {}
    context['cars'] = queryset
    context['dealer_id'] = dealer_id

    if request.method == "POST" and request.user.is_authenticated:

        url = "https://us-east.functions.appdomain.cloud/api/v1/web/apptastic-nv_djangoserver-space/api/review"

        selected_car = queryset[int(request.POST["car"])-1]
        purchased = request.POST.get("purchase", False)
        purchased_date = request.POST.get("purchase_date", "")

        if purchased == "on":
            purchased = True

        if purchased_date:
            purchased_date = datetime.datetime.strptime(purchased_date, "%m/%d/%Y").strftime("%m/%d/%Y")

        json_payload = {
            "review": {
                "dealership": dealer_id,
                "name": request.POST.get("name", ""),
                "review": request.POST.get("review", ""),
                "purchase": purchased,
                "purchase_date": purchased_date,
                "car_make": selected_car.manufacturer.name,
                "car_model": selected_car.name,
                "car_year": selected_car.year.strftime("%Y"),
            }
        }

        response = post_request(url, json_payload, dealerId=dealer_id)

        if response:
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            context['error'] = 'Whoops, something went wrong!'
            return render(request, "djangoapp/add_review.html", context)

    else:

        return render(request, "djangoapp/add_review.html", context)

