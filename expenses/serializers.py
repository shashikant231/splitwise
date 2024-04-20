from rest_framework import serializers
from .models import *
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'

class FriendsWhoOwoYouSerializer(serializers.Serializer):
    friends = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)