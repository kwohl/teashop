import sqlite3
from django.shortcuts import render, redirect, reverse
from teaapp.models import Tea
from ..connection import Connection

def tea_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                t.id,
                t.name,
                t.flavor
            FROM teaapp_tea AS t
            ORDER BY t.name
            """)

            all_teas = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                tea = Tea()
                tea.id = row['id']
                tea.name = row['name']
                tea.flavor = row['flavor']

                all_teas.append(tea)

        template = 'home.html'
        context = {
            'teas': all_teas
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO teaapp_tea
            (
                name, flavor
            )
            VALUES (?, ?)
            """,
            (form_data['name'], form_data['flavor']))

        return redirect(reverse('teaapp:tea_list'))