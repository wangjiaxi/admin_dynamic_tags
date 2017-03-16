from django import forms
from django.db import transaction
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, pgettext_lazy, npgettext_lazy
from django.forms.models import BaseInlineFormSet
from datetime import timedelta
from django.contrib.contenttypes.fields import ContentType

from django.forms import ValidationError
from django.contrib.contenttypes.forms import generic_inlineformset_factory, BaseGenericInlineFormSet

from . import models


def unique_field_formset(field_name):
    class UniqueFieldFormSet (BaseGenericInlineFormSet):
        def __init__(self, *args, **kwargs):
            return super(UniqueFieldFormSet, self).__init__(*args, **kwargs)

        def clean(self):
            if any(self.errors):
                # Don't bother validating the formset unless each form is valid on its own
                return
            values = set()
            for form in self.forms:
                try:
                    value = form.cleaned_data[field_name]
                except:
                    raise forms.ValidationError(_('have tags not selected'))
                if value and value in values:
                    raise forms.ValidationError(_('had repeat options'))
                values.add(value)
    return UniqueFieldFormSet


class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'd_tags'):
            self.fields['d_tags'].choices = [(self.instance.d_tags.id, self.instance.d_tags.name)]

    class Meta:
        model = models.Tag
        fields = '__all__'


class SceneForm(forms.ModelForm):

    class Meta:
        model = models.TagBind
        fields = '__all__'

TagInlineFormSet = generic_inlineformset_factory(models.Tag, formset=unique_field_formset('d_tag'))
