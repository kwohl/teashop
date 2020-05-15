import sqlite3
from django.shortcuts import render

def tea_form(request):
    if request.method == 'GET':
        template = 'teas/tea_form.html'
        context = {}
        return render(request, template, context)