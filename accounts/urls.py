from django.urls import path
from accounts.views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('register/doctor', register_doctor, name= 'register_doctor'),
    path('register/patient', register_patient, name= 'register_patient'),
    path('register/nurse', register_nurse, name= 'register_nurse'),
    path('register/relative', register_relative, name= 'register_relative'),
    path('create_record', create_record, name= 'create_record'),
    path('records', allowed_records, name= 'records'),
    path('record/<int:pk>/', get_record, name='record_detail'),
    path('record/<int:pk>/authenticate', record_authenticate, name='record_authenticate'),
    path('logout/', logout, name= 'logout'),
    path('profile/', profile, name= 'profile'),
    path('', get_home, name = 'home'),
]