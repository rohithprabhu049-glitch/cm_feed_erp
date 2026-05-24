from django.contrib import admin
from django.urls import path

from erp.views import *

urlpatterns = [

    # ADMIN

    path(
        'admin/',
        admin.site.urls
    ),

    # HOME

    path(
        '',
        home
    ),

    # SALES

    path(
        'sales/',
        sales_page
    ),

    path(
        'sales-details/',
        sales_details
    ),

    path(
        'edit-sale/<int:id>',
        edit_sale
    ),

    path(
        'delete-sale/<int:id>',
        delete_sale
    ),

    # STOCK

    path(
        'stock/',
        stock_overview
    ),

    # PRODUCTION

    path(
        'production/',
        production_page
    ),

    path(
        'approve-production/<int:id>',
        approve_production
    ),

    # RAW MATERIAL

    path(
        'raw-material/',
        raw_material
    ),

    path(
        'edit-material/<int:id>',
        edit_material
    ),

    path(
        'delete-material/<int:id>',
        delete_material
    ),

    # DASHBOARD

    path(
        'dashboard/',
        admin_dashboard
    ),

    # EXPORT SALES EXCEL

    path(
        'export-sales/',
        export_sales_excel
    ),

    # EXPORT RAW MATERIAL EXCEL

    path(
        'export-material/',
        export_material_excel
    ),

]