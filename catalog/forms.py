from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from django.forms import  ModelForm
from .models import BookInstance
class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']#与我们原始形式的唯一区别，是模型字段名为due_back 而不是“renewal_date”。

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
    class Meta:
        model=BookInstance
        fields=['due_back',]
        #你可以使用 fields = '__all__'，以包含所有字段，或者你可以使用 exclude （而不是字段），指定不包含在模型中的字段）。
        labels = {'due_back': _('Renewal date'), }
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).'), }
class RenewBookForm(forms.Form):
    renewal_date=forms.DateField(help_text='Enter a date between now and 4 weeks(default 3.')
    def clean_renewal_date(self):
        data=self.cleaned_data['renewal_date']
        if data<datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        if data>datetime.date.today()+datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date -renewal more than 4 weeks ahead'))
        return  data
