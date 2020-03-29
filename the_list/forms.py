from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from django.utils.safestring import mark_safe
from .models import Item, Merchant,ShopGroup


class ItemForm(forms.ModelForm):
    description = forms.CharField()  # widget=PagedownWidget)
    #  vendor_select = forms.ModelChoiceField(queryset=Merchant.objects.all()) - this type should work for other lookup operations
    #  date_requested = forms.DateField(widget=forms.SelectDateWidget)
    #  used 2 methods either the model choice field above or adding the actual model field to the list below

    class Meta:
        model = Item
        fields = [
            'description',
            'quantity',
            # 'vendor_select',
            'to_get_from',
            # 'date_requested',
            # 'purchased',form
            # 'requested', not going to change requested
            # 'date_purchased'
        ]

    def __init__(self, *args, **kwargs):
        """ this limits the selection options to only the active list for the user"""
        list = kwargs.pop('list')
        active_list = Merchant.objects.filter(for_group_id=list)

        # super(ItemForm, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        self.fields['to_get_from'].queryset = active_list
        # not used part of the readonly
        # self.fields['requested'].widget.attrs['readonly'] = True

    def clean_description(self):
        return self.cleaned_data['description'].title()

    def clean_to_get_from(self):
        return self.cleaned_data['to_get_from']

    def clean_quantity(self):
        return self.cleaned_data['quantity']



class UsersGroupsForm(forms.ModelForm):
    groups_for_user = forms.ModelChoiceField(queryset=ShopGroup.objects.all())

    class Meta:
        model = ShopGroup
        fields = ['groups_for_user']


class ItemListForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['description', 'date_purchased']


class MerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ['name', 'for_group']

    def __init__(self, *args, **kwargs):
        """ this limits the selection options to only the active list for the user"""
        list = kwargs.pop('list')
        initial_value = kwargs.pop('default')
        active_list = ShopGroup.objects.filter(id=list)

        super(MerchantForm, self).__init__(*args, **kwargs)

        self.fields['for_group'].queryset = active_list
        self.fields['for_group'].initial = initial_value


class MerchantForm_RA(forms.ModelForm):
    # the original form
    class Meta:
        model = Merchant
        fields = ['name']


class ShopGroupForm(forms.ModelForm):
    class Meta:
        model = ShopGroup
        fields = ['name', 'purpose', 'manager', 'members', 'leaders']

    def clean_leaders(self):
        l_leaders = self.cleaned_data['leaders']
        print(l_leaders)
        l_members = self.cleaned_data['members']
        print(l_members)
        if all(elem in l_members for elem in l_leaders):
            return self.cleaned_data['leaders']
        else:
            raise forms.ValidationError('Only listed members can be leaders')


class NewGroupCreateForm(forms.ModelForm):
    """
    for existing members that want to create a new group
    """
    joining = forms.CharField(label='Group to create', max_length=100)
    purpose = forms.CharField(label='What is this group for?', max_length=200)

    class Meta:
        model = ShopGroup
        fields = [
            'joining',
            'purpose']

    def clean_joining(self):
        target_group = self.cleaned_data.get('joining')
        # now check that the group does not exists and create it, rather do this in the form
        qs_shop_group = ShopGroup.objects.all()
        this_found = qs_shop_group.filter(Q(name__iexact=target_group))
        if this_found.exists():
            raise ValidationError('That group already exists, please enter another name')
        return target_group

