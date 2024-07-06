# from django.urls import path
# from . import views
# urlpatterns = [
#     path('register',views.RegisterView)
# ]
from django.urls import path
from.views import RegisterView, LoginView, UserView, OrganisationView, OrganisationDetailView, AddUserToOrganisationView

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('api/users/<pk>/', UserView.as_view()),
    path('api/organisations/', OrganisationView.as_view()),
    path('api/organisations/<pk>/', OrganisationDetailView.as_view()),
    path('api/organisations/<pk>/users/', AddUserToOrganisationView.as_view()),
]