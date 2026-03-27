import csv

from django.http import HttpResponse


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        forbidden_fields = getattr(
            self,
            "csv_exclude_fields",
            ["password", "last_login", "is_superuser"],
        )
        field_names = [
            field.name
            for field in meta.fields
            if field.name not in forbidden_fields
        ]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(
            meta
        )
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow(
                [str(getattr(obj, field)) for field in field_names]
            )

        return response

    export_as_csv.short_description = "Export Selected"
