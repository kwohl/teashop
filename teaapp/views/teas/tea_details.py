import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from teaapp.models import Tea, TeaPackaging, Packaging
from ..connection import Connection

def get_packaging(tea_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.name,
            p.handmade,
            p.production_location,
            tp.longevity_in_months,
            tp.id
        FROM teaapp_teapackaging AS tp 
        JOIN teaapp_packaging AS p ON tp.packaging_id = p.id
        WHERE tp.tea_id = ?
        """, (tea_id,))

        return db_cursor.fetchall()

def get_tea(tea_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.name,
            t.flavor
        FROM teaapp_tea AS t
        WHERE t.id = ?
        """, (tea_id,))

        return db_cursor.fetchone()


def tea_details(request, tea_id):
    if request.method == 'GET':
        tea = get_tea(tea_id)
        packaging_options = get_packaging(tea_id)

        template = 'teas/tea_details.html'
        context = {
            'tea': tea,
            'packaging_options': packaging_options
        }

        return render(request, template, context)

    elif request.method == 'POST':
        
        form_data = request.POST
            
        if(
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM teaapp_teapackaging
                WHERE id = ?
                """, (tea_id,))

            return redirect(reverse('teaapp:tea_list'))
        
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):   
            with sqlite3.connect(Connection.db_path) as conn:
                    db_cursor = conn.cursor()
                    db_cursor.execute("""
                    UPDATE teaapp_tea
                    SET flavor = ?
                    WHERE id = ?
                    """,
                    (
                        form_data['flavor'],
                        tea_id,
                    ))
            return redirect(reverse('teaapp:tea_list'))