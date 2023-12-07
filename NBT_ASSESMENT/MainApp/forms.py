from django import forms  

class IntervalForm(forms.Form):  
    interval=forms.IntegerField()
    file      = forms.FileField() # for creating file input s