from django.conf.urls import url
from .import views
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
"""router.register('hello-viewset',views.HelloViewSet,base_name='hello-viewset')"""
router.register('profile',views.UserProfileViewSet)
urlpatterns=[
url(r'^SampleApi/',views.SampleApi.as_view()),
url(r'^TimeData/',views.TimeData.as_view()),
url(r'^PowerPlantData/',views.PowerPlantData.as_view()),
url(r'^GetDesisionAspectCumBlock_New/',views.GetDesisionAspectCumBlock_New.as_view()),
url(r'^GetInstanceDataRABT/',views.GetInstanceDataRABT.as_view()),
url(r'^GetNextFourBlocks_Final/',views.GetNextFourBlocks_Final.as_view()),
url(r'^GetDCSGLastBlockData_New/',views.GetDCSGLastBlockData_New.as_view()),
url(r'^GetInstanceDataRABT_CurrentBlockNX4_Final/',views.GetInstanceDataRABT_CurrentBlockNX4_Final.as_view()),
url(r'',include(router.urls))
]
