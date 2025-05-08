from  django  import forms
from .models import  *
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        labels = {
            'title': 'عنوان الكتاب',
            'author': 'المؤلف',
            'category': 'التصنيف',
            'photo_book': 'صورة الكتاب',
            'photo_author': 'صورة المؤلف',
            'pages': 'عدد الصفحات',
            'price': 'السعر',
            'retail_price_day': 'سعر الإيجار اليومي',
            'retail_period': 'مدة الإيجار (بالأيام)',
            'status': 'الحالة',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل عنوان الكتاب'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المؤلف'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'photo_book': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_author': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'retail_price_day': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'retail_period': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'price': 'أدخل السعر بالجنيه أو الدولار (مثال: 99.99)',
            'retail_price_day': 'أدخل سعر الإيجار اليومي (مثال: 5.00)',
            'retail_period': 'عدد الأيام التي يمكن استئجار الكتاب فيها',
        }

class CatForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            'name': "",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'اسم التصنيف'}),
        }

