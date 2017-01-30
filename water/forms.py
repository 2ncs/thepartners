# -*- coding: utf-8 -*-

from django import forms
from .models import *
from django.forms import ModelForm

class search(forms.Form):
        onoma = forms.CharField(label='Choose Month', max_length=30,required=False,widget=forms.TextInput(attrs={'class': 'date-picker', 'name': 'startDate','id':'startDate','readonly':'true',}))



class profile_sales(forms.Form):
	user=forms.ModelChoiceField(label='',queryset=MyAppUser.objects.exclude(code_metapolishs__isnull=True).exclude(code_metapolishs__exact=''),widget=forms.Select(attrs={'id':'form','class':'form-control','style':"width:100px !important;"}))
	

class profile_all(forms.Form):
	user=forms.ModelChoiceField(label='',queryset=MyAppUser.objects.all(),widget=forms.Select(attrs={'id':'form','class':'form-control','style':"width:100px !important;"}))



class profile_customers_served(forms.Form):
	user=forms.ModelChoiceField(label='',queryset=MyAppUser.objects.exclude(code_paroxhs__isnull=True).exclude(code_paroxhs__exact=''),widget=forms.Select(attrs={'id':'form','class':'form-control','style':"width:100px !important;"}))
	

	
#class profile_customers_served(forms.Form):		
		
