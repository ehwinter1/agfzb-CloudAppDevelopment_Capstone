from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake, CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
# def about(request):
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            error_msg = 'Invalid credentials.'
            return render(request, 'djangoapp/index.html', {'error': error_msg})
    else:
        return render(request, 'djangoapp/index.html')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        user.save()
        message = "User successfully created."
        return render(request, 'djangoapp/registration.html', {"message": message})
    else:
        return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/5ef53005-e473-41bd-bb70-ba9c37cc30a2/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context = {'dealership_list' : dealerships}
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/5ef53005-e473-41bd-bb70-ba9c37cc30a2/review-package/get-reviews"
        dealer_url =  "https://us-south.functions.appdomain.cloud/api/v1/web/5ef53005-e473-41bd-bb70-ba9c37cc30a2/dealership-package/get-dealership"
        reviews = get_dealer_reviews_from_cf(review_url, dealer_id)
        context["reviews"] = reviews
        dealer = get_dealer_by_id(dealer_url, dealer_id)
        context["dealer"] = dealer
        return render(request, 'djangoapp/dealer_details.html', context)



# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    dealer_url =  "https://us-south.functions.appdomain.cloud/api/v1/web/5ef53005-e473-41bd-bb70-ba9c37cc30a2/dealership-package/get-dealership"
    dealer = get_dealer_by_id(dealer_url, dealer_id)
    if request.method == 'GET':
        cars = CarModel.objects.all().filter(dealer_id=dealer_id)
        context['cars'] = cars
        context['dealer'] = dealer
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
            form = request.POST
            review = dict()
            review["name"] = "{request.user.first_name} {request.user.last_name}"
            review["dealership"] = dealer_id
            review["review"] = form["content"]
            review["purchase"] = form.get("purchasecheck")
            if review["purchase"]:
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%Y-%m-%d").isoformat()
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.make.name
            review["car_model"] = car.name
            review["car_year"] = car.year
            review["id"] = 1
            
            # If the user bought the car, get the purchase date
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%Y-%m-%d").isoformat()
            else: 
                review["purchase_date"] = None
            
            post_url = "https://us-south.functions.appdomain.cloud/api/v1/web/5ef53005-e473-41bd-bb70-ba9c37cc30a2/review-package/post-review"
            json_payload = {"review" : review}
            post_request(post_url,json_payload)

            # After posting the review the user is redirected back to the dealer details page
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)