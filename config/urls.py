from django.contrib import admin
from django.urls import path

from erp import views


urlpatterns = [

    # =========================================
    # DJANGO ADMIN
    # =========================================

    path(
        'admin/',
        admin.site.urls
    ),

    # =========================================
    # HOME
    # =========================================

    path(
        '',
        views.home,
        name='home'
    ),

    # =========================================
    # LOGIN
    # =========================================

    path(
        'admin-login/',
        views.admin_login,
        name='admin_login'
    ),

    path(
        'sales-login/',
        views.sales_login,
        name='sales_login'
    ),

    path(
        'manufacture-login/',
        views.manufacture_login,
        name='manufacture_login'
    ),

    # =========================================
    # LOGOUT
    # =========================================

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # =========================================
    # SALES MODULE
    # =========================================

    path(
        'sales/',
        views.sales_page,
        name='sales_page'
    ),

    path(
        'sales-details/',
        views.sales_details,
        name='sales_details'
    ),

    path(
        'edit-sale/<int:id>/',
        views.edit_sale,
        name='edit_sale'
    ),

    path(
        'delete-sale/<int:id>/',
        views.delete_sale,
        name='delete_sale'
    ),

    # =========================================
    # STOCK
    # =========================================

    path(
        'stock/',
        views.stock_overview,
        name='stock'
    ),

    # =========================================
    # PRODUCTION
    # =========================================

    path(
        'production/',
        views.production_page,
        name='production'
    ),

    path(
        'approve-production/<int:id>/',
        views.approve_production,
        name='approve_production'
    ),

    # =========================================
    # NEW ADDED
    # APPROVED PRODUCTION EDIT/DELETE
    # =========================================

    path(
        'edit-production/<int:id>/',
        views.edit_production,
        name='edit_production'
    ),

    path(
        'delete-production/<int:id>/',
        views.delete_production,
        name='delete_production'
    ),

    # =========================================
    # RAW MATERIAL
    # =========================================

    path(
        'raw-material/',
        views.raw_material,
        name='raw_material'
    ),

    path(
        'edit-material/<int:id>/',
        views.edit_material,
        name='edit_material'
    ),

    path(
        'delete-material/<int:id>/',
        views.delete_material,
        name='delete_material'
    ),

    # =========================================
    # DASHBOARD
    # =========================================

    path(
        'dashboard/',
        views.admin_dashboard,
        name='dashboard'
    ),

    # =========================================
    # EXPORT EXCEL
    # =========================================

    path(
        'export-sales-excel/',
        views.export_sales_excel,
        name='export_sales_excel'
    ),

    path(
        'export-material-excel/',
        views.export_material_excel,
        name='export_material_excel'
    ),

]