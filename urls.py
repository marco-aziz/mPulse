
from django.contrib import admin
from django.urls import path, include
from mpulseapp.views import MemberView, MemberCreate, FileUploadView

urlpatterns = [
	#Path for admin page, mainly to check on model instamces instead of using SQLite DB browser
    path('admin/', admin.site.urls),
    #Path for REST Framework authentication, required
    path('api-auth/', include('rest_framework.urls')),
    #Path for member list view, support detail view with param id, ph, cmid, aid
    path('api/members/', MemberView.as_view(), name='post-list'),
    #Path for creating a new member over POST with form-data populated
    path('api/members/create/', MemberCreate.as_view(), name='post-list'),
    #path for uploading .csv file and batch creating members
    path('api/members/batch/', FileUploadView.as_view(), name='post-list'),

]
