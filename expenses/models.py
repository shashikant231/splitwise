# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username
    
    def total_balance(self):
        # Calculate the total balance by summing up the amounts due to the user and subtracting the amounts the user owes
        # amount_due_to_user sums up all the amount where user is payer and share has not been settled yet
        amount_due_to_user = sum(share.share for share in self.shares_paid.filter(settled_at__isnull=True))
         # amount_owed_by_user sums up all the amount where user is settler and share has not been settled yet
        amount_owed_by_user = sum(share.share for share in self.shares_received.filter(settled_at__isnull=True))
        return amount_due_to_user - amount_owed_by_user
    
    def total_you_owe(self):
        # Calculate the total amount the user owes to others
        return sum(share.share for share in self.shares_received.filter(settled_at__isnull=True))

    def total_due_to_you(self):
        # Calculate the total amount due to the user from others
        return sum(share.share for share in self.shares_paid.filter(settled_at__isnull=True))




class Expense(models.Model):
    description = models.TextField(_('description'), blank=True, unique=False, null=True,help_text=_('Description of expense [optional].'))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(_('date added'), auto_now_add=True)
    payer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False,null=False, related_name='payers')
    participants = models.ManyToManyField(CustomUser, related_name='expenses_shared')

    def __str__(self):
        return f'{self.description}-{self.payer}-{self.amount}'


class Share(models.Model):
    EQUAL_SPLIT = 'EQUAL'
    UNEQUAL_SPLIT = 'UNEQUAL'
    SPLIT_CHOICES = [
        (EQUAL_SPLIT, 'Equally'),
        (UNEQUAL_SPLIT, 'Unequally'),
    ]
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, blank=False, null=False,
                                related_name='shares')
    payer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False,
                             null=False, related_name='shares_paid')
    settler = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True, 
                                help_text=_('Who has to pay for this share'),related_name='shares_received')
    comment = models.TextField(blank=True, unique=False, null=True,help_text=_('Add a comment[OPTIONAL].'))
    # stores the timestamp when the share was settled, None indicate share has not been settels yet
    settled_at = models.DateTimeField(null=True, blank=True)

    share = models.DecimalField(max_digits=10, decimal_places=2,help_text=_('share amount'))
    split_type = models.CharField(max_length=7, choices=SPLIT_CHOICES, default=EQUAL_SPLIT)
    
    updated_at = models.DateTimeField(_('last update'), auto_now=True)

    def settled(self):
        return self.settled_at is not None

    def share_percentage(self):
        pass

    def __str__(self):
        return f'{self.payer} - {self.settler} - {self.expense.description} - {self.share}'
    