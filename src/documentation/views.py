import json
from pathlib import Path

from django.shortcuts import render
from django.views.generic import TemplateView


class DocumentationPage(TemplateView):
    template_name = "documentation.html"

    def get(self, request, *args, **kwargs):
        fixture_path = Path(__file__).parent.parent / "fixtures" / "documentation.json"
        with open(fixture_path, "r", encoding="UTF-8") as f:
            data = json.load(f)

        context = {"doc": data}
        return render(request, self.template_name, context)
