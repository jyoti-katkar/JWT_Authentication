from django.urls import path
from .views import homepage, login, employeeList, employeeDetail

urlpatterns = [
    path('', homepage),
    path('api/login', login),
    #path('api/sampleapi', sample_api)
    path('api/emplist', employeeList.as_view()),
    path('api/employeeDetail/<int:pk>', employeeDetail.as_view())

]