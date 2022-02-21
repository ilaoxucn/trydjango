from socket import fromshare
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','content']

    def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        qs = Article.objects.filter(title__icontains=title)
        if qs.exists():
            self.add_error("title",f"标题{title}已经被占用")
        return data



class ArticleFormold(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    # def clean_title(self):
    #     cleaned_data = self.cleaned_data
    #     print(cleaned_data)
    #     title = cleaned_data.get('title')
    #     print(title)
    #     if title.lower().strip() == "我的文章":
    #         raise forms.ValidationError("文章标题冲突")
    #     return title

    def clean(self):
        cleaned_data = self.cleaned_data
        print('all cleaned data',cleaned_data)
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if title.lower().strip() == "我的文章":
            self.add_error('title',"文章标题冲突")
        if "百分之百" in content or "行业第一" in title.lower():
            self.add_error('content',"文章内容中不能含有百分之百")
            raise forms.ValidationError("确定的词不能出现在公共广告中")
        
        return cleaned_data