
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
        

class ExpenseWithSharesViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing expenses along with their shares for a specific user.
    """

    def list(self, request, username=None):
        # Get the user by username
        user = get_object_or_404(CustomUser, username=username)
        
        # Retrieve expenses where the user is the payer
        expenses = Expense.objects.filter(payer=user)

        # List to store combined data
        response_data = []
        
        # Iterate through expenses
        for expense in expenses:
            # Retrieve the shares related to the current expense
            shares = Share.objects.filter(expense=expense)
            
            # Serialize the expense
            expense_serializer = ExpenseSerializer(expense)
            
            # Serialize the shares
            shares_serializer = ShareSerializer(shares, many=True)
            
            # Combine the expense and shares data into a dictionary
            expense_and_shares = {
                'expense': expense_serializer.data,
                'shares': shares_serializer.data
            }
            
            # Add the combined data to the response list
            response_data.append(expense_and_shares)
        
        # Return the combined data as a response
        return Response(response_data, status=status.HTTP_200_OK)
    

# Create your views here.
class CustomUserViewset(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

class ExpenseViewset(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()


class ShareViewset(viewsets.ModelViewSet):
    serializer_class = ShareSerializer
    queryset = Share.objects.all()
    
class TotalBalanceViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        # to retrieve total balance for the specified username
        user = get_object_or_404(CustomUser, username=pk)
        total_balance = user.total_balance()
        return Response({'total_balance '  : total_balance})
    


class TotalYouOweViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        # to retrieve total amount the user owes to others.
        user = get_object_or_404(CustomUser, username=pk)
        total_owe = user.total_you_owe()
        return Response({'total_owe': total_owe})
    

class TotalDueToYouViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        # to retrieve total amount due to the user from others.
        user = get_object_or_404(CustomUser, username=pk)
        total_due_to_you = user.total_due_to_you()
        return Response({'total_due_to_you': total_due_to_you})

    

class FriendsWhoOwoYouViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        # Get the user object or return 404 if not found
        payer = get_object_or_404(CustomUser, username=pk)
        
        # Query unsettled shares for the specified payer
        unsettled_shares = Share.objects.filter(payer=payer, settled_at__isnull=True)
        print(unsettled_shares)

        # Calculate total amount for each settler
        settlers_totals = {}
        for share in unsettled_shares:
            settler = share.settler.username
            print(settler)
            amount = share.share
            settlers_totals[settler] = settlers_totals.get(settler, 0) + amount

        # Serialize the data
        serializer = FriendsWhoOwoYouSerializer([
            {'friends': settler, 'total_amount': total}
            for settler, total in settlers_totals.items()
        ], many=True)

        return Response(serializer.data)