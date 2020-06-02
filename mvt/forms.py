from django import forms
from mvt.models import CareSeeker
from mvt.models import Request
from mvt.models import Review
from datetime import date


class FundForm(forms.ModelForm):

    class Meta:
        model = CareSeeker
        
        fields = ['wallet']
    
class ApproveFrom(forms.ModelForm):
    start_date = forms.DateField()
    end_date = forms.DateField()
   
    class Meta:
        model = Request
        fields = ['start_date','end_date']
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
    
        if start_date < date.today():
            self.add_error("start_date","Date must be selected from today")
 
        if end_date <= start_date:
            self.add_error("end_date","Service end date must be greater then start date")
    
    
        
class ReviewForm(forms.ModelForm):
    rating = forms.FloatField()

    class Meta:
        model = Review
        fields = ['msg','rating']
    
    def clean_rating(self):
        rating = self.cleaned_data.get("rating")

        if rating > 5 or rating <= 0:
            raise forms.ValidationError("rating must be given between 1 to 5",code="invalid")
        else:
            return rating
       
        





# def clean_password(self):
#         password = self.cleaned_data.get("password")
#         match = re.search("[A-Z]",password)

#         if not match:
#             raise forms.ValidationError("atleast one uppercase",code="upper")
#         else:
#             return password