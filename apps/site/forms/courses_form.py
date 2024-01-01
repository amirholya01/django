from django import forms
from ckeditor.fields import CKEditorWidget
from django.utils.translation import gettext_lazy as _


class AddCourseCommentForm(forms.Form):
    course_id = forms.IntegerField(widget=forms.HiddenInput)
    comment_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    text = forms.CharField(
        widget=CKEditorWidget(attrs={
            'class': 'form-control simple',
        }, config_name='user_side'),
        label=_('Text')
    )
