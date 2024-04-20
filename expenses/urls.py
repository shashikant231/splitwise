from .views import *
from rest_framework import routers
from django.urls import path,include

router = routers.DefaultRouter()
router.register("user_api",CustomUserViewset,basename='user_api')
router.register("expenses",ExpenseViewset,basename='expenses')
router.register("share",ShareViewset,basename='share')
router.register(r'total-balance', TotalBalanceViewSet, basename='total_balance')
router.register(r'total-you-owe', TotalYouOweViewSet, basename='total-you-owe')
router.register(r'total-due-to-you', TotalDueToYouViewSet, basename='total-due-to-you')
# router.register(r'expense-with-shares', ExpenseWithSharesViewSet, basename='expense-with-shares')
router.register(r'expense-with-shares/(?P<username>\w+)', ExpenseWithSharesViewSet, basename='expense-with-shares')
router.register(r'friends-who-owe-you', FriendsWhoOwoYouViewSet, basename='friends_who_owe_you')

urlpatterns = [
    path('',include(router.urls)),

] + router.urls