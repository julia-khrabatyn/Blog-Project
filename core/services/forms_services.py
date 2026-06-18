from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from .translation_services import LANGUAGES_LIST, translate_changed_fields


class BaseTranslationForm(ModelForm):
    """Base class for Forms with dynamic language switching."""

    translatable_fields = []
    optional_fields = []
    required_translatable_fields = []
    UI = None

    def _hide_non_current_language_fields(self):
        current_lang = get_language()

        for field_name in self.translatable_fields:
            for lang in LANGUAGES_LIST:

                translated_field = f"{field_name}_{lang}"

                if translated_field not in self.fields:
                    continue

                if lang == current_lang:
                    self.fields[translated_field].required = True
                    continue

                self.fields[translated_field].required = False
                self.fields[translated_field].widget = forms.HiddenInput()

    def _configure_optional_fields(self):
        for field_name in self.optional_fields:
            field = self.fields.get(field_name)

            if field:
                field.required = False
                continue

            for lang in LANGUAGES_LIST:
                field = self.fields.get(f"{field_name}_{lang}")
                if field:
                    field.required = False

    def _apply_translatable_ui(self):
        if not self.UI:
            return

        for field_base in self.translatable_fields:

            ui = self.UI.get(field_base)
            if not ui:
                continue

            for lang in LANGUAGES_LIST:

                field_name = f"{field_base}_{lang}"

                field = self.fields.get(field_name)
                if not field:
                    continue

                field.label = ui["label"]
                field.widget.attrs["placeholder"] = ui["placeholder"]
                field.help_text = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hide_non_current_language_fields()
        self._configure_optional_fields()
        self._apply_translatable_ui()

    def clean(self):
        cleaned_data = super().clean()

        for field_name in self.required_translatable_fields:
            filled = any(
                cleaned_data.get(f"{field_name}_{lang}")
                for lang in LANGUAGES_LIST
            )
            if not filled:
                self.add_error(
                    f"{field_name}_en", _(f"You should add {field_name}")
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        translate_changed_fields(
            instance=instance,
            changed_fields=self.changed_data,
        )

        if commit:
            instance.save()
            self.save_m2m()

        return instance
