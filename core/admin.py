import csv

from django.http import HttpResponse

__all__ = [
    "ExportCsvMixin"
]  # TODO: is it possible to that not only with classes, but with functions too??


class ExportCsvMixin:  # FIXME: is it fixed? should I make this be possible to use it only by superuser or staff too?
    def export_as_csv(self, _request, queryset):

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
