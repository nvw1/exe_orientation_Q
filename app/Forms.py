from django.db import models

class DropDown(ModelForm):
    cats = forms.ModelChoiceField(queryset=Part.objects.order_by('CATEGORY').values_list('CATEGORY', flat=True).distinct())