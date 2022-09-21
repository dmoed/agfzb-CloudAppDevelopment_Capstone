from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    # path for about view
    path(route='about', view=views.about_request, name='about'),

    # path for contact us view
    path(route='contact', view=views.contact_request, name='contact'),

    # path for registration

    # path for login
    path(route='login', view=views.login_request, name='login'),

    # path for logout
    path(route='logout', view=views.logout_request, name='logout'),

    # path registration
    path(route='registration', view=views.registration_request, name='registration'),

    # path for dealer reviews view
    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer by state
    path(route='dealer', view=views.get_dealerships_by_state, name='index'),

    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path(route='dealer/<int:dealer_id>/add-review', view=views.add_review, name='dealer_add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
