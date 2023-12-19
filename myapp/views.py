# myapp/views.py
from django.http import HttpResponse

# myapp/views.py
from django.shortcuts import render

def hello_world(request):
    # Define the context with the necessary information
    context = {
        'company_name': 'Warner Sisters Inc',
        'challenge_description': (
            "A leading technology company, Warner Sisters Inc, faces a critical challenge "
            "in efficiently deploying and managing its Python applications. As the company "
            "grows and its application portfolio expands, the need for a scalable, resilient, "
            "and automated deployment solution has become paramount."
        ),
    }

    # Render the template with the provided context
    return render(request, 'myapp/hello_world.html', context)

