from socket import fromshare
from django import forms

from .models import Recipe,RecipeIngredient

class RecipeForm(forms.ModelForm):
    # required_css_class = 'required-field'
    # error_css_class = 'error-field'
    name = forms.CharField(label='',widget=forms.TextInput(attrs={"class":"form-control","placeholder":"输入菜谱的名称"}))
    # description = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['name'].widget.attrs.update({"class":"form-control-2"})
        #self.fields['name'].label=''   
        self.fields['description'].widget.attrs.update(rows="2") 
        self.fields['directions'].widget.attrs.update(rows='3')
    class Meta:
        model = Recipe
        fields = ['name','description','directions']

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['name','quantity','unit']



