from django import forms

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()



class UploadFileForm2(forms.Form):
    #title = forms.CharField(max_length=50)
    file2 = forms.FileField()

class UploadFileForm3(forms.Form):
    #title = forms.CharField(max_length=50)
    file3 = forms.FileField()
