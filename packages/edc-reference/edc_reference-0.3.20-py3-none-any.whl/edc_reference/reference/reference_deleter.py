from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.apps import apps as django_apps
from django.db import transaction

from ..site_reference import site_reference_configs

if TYPE_CHECKING:
    from ..models import Reference


class ReferenceDeleter:

    """A class to delete all instances from edc_reference.Reference
    model linked to this Crf or Requisition model instance.

    See signals and edc_reference.Reference.
    """

    def __init__(self, model_obj=None):
        reference_model = site_reference_configs.get_reference_model(
            name=model_obj.reference_name
        )
        self.model_obj = model_obj
        self.reference_model_cls: Reference = django_apps.get_model(reference_model)
        with transaction.atomic():
            self.reference_model_cls.objects.filter(**self.options).delete()

    @property
    def options(self) -> dict[str, Any]:
        """Returns query lookup options.

        Note: `Reference` model instances for requisitions use the
        `label_lower.panel_name` format for field `reference_name`.
        """
        return dict(
            identifier=self.model_obj.related_visit.subject_identifier,
            report_datetime=self.model_obj.related_visit.report_datetime,
            timepoint=self.model_obj.related_visit.timepoint,
            model=self.model_obj.reference_name,
        )
