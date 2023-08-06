import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from antlr4.InputStream import InputStream
from blended.lint.lint import lint


@csrf_exempt
def validate(request):
    """
    view to return error messages if passed string is invalid.
    """    
    try:
        message = request.POST['message']
    except KeyError:
        return HttpResponse("A 'message' must be passed in POST request")
    results = lint(InputStream(message))
    if not results:
        return HttpResponse(json.dumps('No Errors'), content_type='application/json')
    else:
        return HttpResponse(json.dumps(results), content_type='application/json')
            
