from django import forms
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget


# region add article comment

class AddArticleCommentForm(forms.Form):
    parent_id = forms.IntegerField(
        label=_('Parent'),
        widget=forms.HiddenInput(),
        initial=0
    )

    text = forms.CharField(
        label=_('Text'),
        widget=CKEditorWidget(config_name='user_side')
    )

# endregion
