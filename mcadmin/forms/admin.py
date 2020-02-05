# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/forms/admin.py


from typing import (  # pylint: disable=W0611
    Any,
    Dict,
    List,
    Type,
    Union,
    Mapping,
    Optional,
)

from django import forms
from django.core.files import File
from django.db.models import Model
from django.forms.utils import ErrorList
from django.utils.translation import ugettext_lazy as _

from mcadmin.models.command import Command
from mcadmin.registry import registry


__all__ = [
    "CommandAdminForm",
]  # type: List[str]


class CommandAdminForm(forms.ModelForm):
    """
    Management command model admin form.
    """

    def __init__(
        self,
        data: Optional[Mapping[str, Any]] = None,
        files: Optional[Mapping[str, File]] = None,
        auto_id: Union[bool, str] = "id_%s",
        prefix: Optional[str] = None,
        initial: Optional[Dict[str, Any]] = None,
        error_class: Type[ErrorList] = ErrorList,
        label_suffix: Optional[str] = None,
        empty_permitted: bool = False,
        instance: Optional[Model] = None,
        use_required_attribute: Optional[bool] = None,
        renderer: Any = None,
    ):
        """
        Overridden to change command field choices on the fly.

        :arg data: form data.
        :type data: Optional[Mapping[str, Any]].
        :arg files: form files.
        :type files: Optional[Mapping[str, File]].
        :arg auto_id: field auto ID.
        :type auto_id: Union[bool, str].
        :arg prefix: field prefix.
        :type prefix: Optional[str].
        :arg initial: form initial data.
        :type initial: Optional[Dict[str, Any]].
        :arg error_class: form error class.
        :type error_class: Type[ErrorList].
        :arg label_suffix: field label suffix.
        :type label_suffix: Optional[str].
        :arg empty_permitted: allow empty.
        :type empty_permitted: bool.
        :arg instance: model instance.
        :type instance: Optional[Model].
        :arg use_required_attribute: add required HTML attribute.
        :type use_required_attribute: Optional[bool].
        :arg renderer: form renderer.
        :type renderer: Any.
        :return: nothing.
        :rtype: None.
        """

        super(CommandAdminForm, self).__init__(
            data=data,
            files=files,
            auto_id=auto_id,
            prefix=prefix,
            initial=initial,
            error_class=error_class,
            label_suffix=label_suffix,
            empty_permitted=empty_permitted,
            instance=instance,
            use_required_attribute=use_required_attribute,
            renderer=renderer,
        )

        self.fields["command"].choices = registry.choices

    command = forms.ChoiceField(
        label=_("Command"),
        choices=[],
        widget=forms.Select(),
        required=True,
        help_text=_("got from management commands admin registry"),
    )

    class Meta:

        model = Command  # type: Type[Command]
        fields = [
            "command",
            "group",
        ]  # type: List[str]
