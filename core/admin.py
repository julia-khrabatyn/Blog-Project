import csv

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

__all__ = ["ExportCsvMixin"]


class BaseExportCsvMixin:
    """Base class for safely exporting csv file from admin site."""

    def export_as_csv(self, request, queryset):
        if not request.user.is_staff:
            raise PermissionDenied("You haven't permission for that action!")

        meta = self.model._meta
        hard_forbidden_fields = [
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
        ]
        extra_forbidden_fields = getattr(
            self,
            "csv_exclude_fields",
            [],
        )
        all_forbidden_fields = set(
            hard_forbidden_fields + extra_forbidden_fields
        )
        field_names = [
            field.name
            for field in meta.fields
            if field.name not in all_forbidden_fields
        ]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f"attachment; filename={meta.model_name}.csv"
        )

        writer = csv.writer(response)
        writer.writerow(field_names)

        for obj in queryset:
            writer.writerow(
                [str(getattr(obj, field)) for field in field_names]
            )

        return response

    export_as_csv.short_description = "Export Selected"


class UserExportCsvMixin(BaseExportCsvMixin):
    """Class for safely exporting info about users from admin site."""

    def export_as_csv(self, request, queryset):
        if not request.user.is_superuser:
            raise PermissionDenied("You haven't permission for that action!")
        self.csv_exclude_fields = [
            "groups",
            "user_permissions",
            "is_active",
            "date_joined",
        ]
        return super().export_as_csv(request, queryset)
