from django.urls import path
from mvt.views import index
from mvt.views import CareSeekerList
from mvt.views import CareSeekerDetail
from mvt.views import CareSeekersRequestStatus
from mvt.views import CareTakersRequests
from mvt.views import CareTakerDetail
from mvt.views import AproveRequest
from mvt.views import UpdateFund
from mvt.views import StartService
from mvt.views import StopService
from mvt.views import RejectService
from mvt.views import ReviewView

urlpatterns = [
    path('index',index,name='index'),
    path('care_seeker_list',CareSeekerList.as_view(),name="care_seeker_list"),
    path('care_seeker/<int:pk>',CareSeekerDetail.as_view(),name = 'care_seeker'),
    path('care_seeker/<int:pk>/<slug:slug>',CareSeekerDetail.as_view(),name = 'care_seeker'),
    path('request_status',CareSeekersRequestStatus.as_view()),
    path('care_taker_list',CareTakersRequests.as_view()),
    path('care_taker/<int:pk>',CareTakerDetail.as_view(),name='caretaker'),
    path('approve_request/<int:pk>',AproveRequest.as_view(),name='approve_request'),
    path('update_fund/<int:pk>',UpdateFund.as_view(),name='update_fund'),
    path('start_service',StartService.as_view()),
    path('start_service/<int:pk>',StartService.as_view(),name = "start_service"),
    path('end_service',StopService.as_view()),
    path('end_service/<int:pk>',StopService.as_view(),name='end_service'),
    path('reject_service',RejectService.as_view()),
    path('reject_service/<int:pk>',RejectService.as_view(),name='reject_service'),
    path('review/<int:pk>/<slug:slug>',ReviewView.as_view(),name='review')

]