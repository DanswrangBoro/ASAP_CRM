
import html
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render




def countries(request, country_name):
    country_templates = {
        "usa": "usa.html",
        "japan": "japan.html",
        "germany": "germany.html",
        "russia" : "russia.html",
        "canada" : "canada.html",
        "india" : "india.html"
    }

    # Check if the country_name exists in the dictionary
    if country_name in country_templates:
        template_name = country_templates[country_name]
        return render(request, template_name)
    else:
        # Handle the case where country_name is not in the dictionary
        return render(request, 'error_template.html', {'error_message': 'Invalid country name'})

