from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q

from .models import *

import pandas as pd


# HOME

def home(request):

    return render(request, 'home.html')


# SALES PAGE

def sales_page(request):

    products = Product.objects.all()

    if request.method == 'POST':

        date = request.POST.get('date')

        rd_name = request.POST.get('rd_name')

        retail_partner = request.POST.get(
            'retail_partner'
        )

        mobile = request.POST.get('mobile')

        address = request.POST.get('address')

        product_id = request.POST.get(
            'product'
        )

        bag_count = request.POST.get(
            'bag_count'
        )

        unit_price = request.POST.get(
            'unit_price'
        )

        payment_term = request.POST.get(
            'payment_term'
        )

        product = Product.objects.get(
            id=product_id
        )

        Sale.objects.create(

            bill_no='',

            date=date,

            rd_name=rd_name,

            retail_partner=retail_partner,

            mobile=mobile,

            address=address,

            product=product,

            bag_count=int(bag_count),

            unit_price=float(unit_price),

            payment_term=payment_term

        )

        messages.success(

            request,

            'Sales Submitted Successfully'

        )

        return redirect('/sales')

    return render(

        request,

        'sales.html',

        {

            'products': products

        }

    )


# SALES DETAILS

def sales_details(request):

    query = request.GET.get('q')

    sales = Sale.objects.all().order_by('-id')

    if query:

        sales = sales.filter(

            Q(rd_name__icontains=query) |
            Q(mobile__icontains=query) |
            Q(bill_no__icontains=query)

        )

    return render(

        request,

        'sales_details.html',

        {

            'sales': sales

        }

    )


# EDIT SALE

def edit_sale(request, id):

    sale = Sale.objects.get(id=id)

    products = Product.objects.all()

    if request.method == 'POST':

        sale.date = request.POST.get('date')

        sale.rd_name = request.POST.get(
            'rd_name'
        )

        sale.retail_partner = request.POST.get(
            'retail_partner'
        )

        sale.mobile = request.POST.get(
            'mobile'
        )

        sale.address = request.POST.get(
            'address'
        )

        product_id = request.POST.get(
            'product'
        )

        sale.product = Product.objects.get(
            id=product_id
        )

        sale.bag_count = int(

            request.POST.get('bag_count')

        )

        sale.unit_price = float(

            request.POST.get('unit_price')

        )

        sale.payment_term = request.POST.get(
            'payment_term'
        )

        sale.save()

        messages.success(

            request,

            'Sale Updated Successfully'

        )

        return redirect('/sales-details')

    return render(

        request,

        'edit_sale.html',

        {

            'sale': sale,

            'products': products

        }

    )


# DELETE SALE

def delete_sale(request, id):

    sale = Sale.objects.get(id=id)

    sale.delete()

    messages.success(

        request,

        'Sale Deleted Successfully'

    )

    return redirect('/sales-details')


# STOCK OVERVIEW

def stock_overview(request):

    products = Product.objects.all()

    return render(

        request,

        'stock.html',

        {

            'products': products

        }

    )


# PRODUCTION PAGE

def production_page(request):

    products = Product.objects.all()

    if request.method == 'POST':

        product_id = request.POST.get(
            'product'
        )

        date = request.POST.get('date')

        bag_count = request.POST.get(
            'bag_count'
        )

        product = Product.objects.get(
            id=product_id
        )

        Production.objects.create(

            product=product,

            date=date,

            bag_count=int(bag_count),

            approved=False

        )

        messages.success(

            request,

            'Production Entry Added Successfully'

        )

        return redirect('/production')

    return render(

        request,

        'production.html',

        {

            'products': products

        }

    )


# APPROVE PRODUCTION

def approve_production(request, id):

    production = Production.objects.get(id=id)

    production.approved = True

    production.save()

    product = production.product

    product.stock += production.bag_count

    product.save()

    messages.success(

        request,

        'Production Approved Successfully'

    )

    return redirect('/dashboard')


# RAW MATERIAL PAGE

def raw_material(request):

    query = request.GET.get('q')

    if request.method == 'POST':

        item_name = request.POST.get(
            'item_name'
        )

        date = request.POST.get('date')

        used_kg = request.POST.get(
            'used_kg'
        )

        current_balance = request.POST.get(
            'current_balance'
        )

        RawMaterial.objects.create(

            item_name=item_name,

            date=date,

            used_kg=float(used_kg),

            current_balance=float(current_balance)

        )

        messages.success(

            request,

            'Raw Material Added Successfully'

        )

        return redirect('/raw-material')

    materials = RawMaterial.objects.all().order_by('-id')

    if query:

        materials = materials.filter(

            Q(item_name__icontains=query) |
            Q(date__icontains=query)

        )

    return render(

        request,

        'raw_material.html',

        {

            'materials': materials

        }

    )


# EDIT RAW MATERIAL

def edit_material(request, id):

    material = RawMaterial.objects.get(id=id)

    if request.method == 'POST':

        material.item_name = request.POST.get(
            'item_name'
        )

        material.date = request.POST.get(
            'date'
        )

        material.used_kg = float(

            request.POST.get('used_kg')

        )

        material.current_balance = float(

            request.POST.get(
                'current_balance'
            )

        )

        material.save()

        messages.success(

            request,

            'Material Updated Successfully'

        )

        return redirect('/raw-material')

    return render(

        request,

        'edit_material.html',

        {

            'material': material

        }

    )


# DELETE RAW MATERIAL

def delete_material(request, id):

    material = RawMaterial.objects.get(id=id)

    material.delete()

    messages.success(

        request,

        'Material Deleted Successfully'

    )

    return redirect('/raw-material')


# ADMIN DASHBOARD

def admin_dashboard(request):

    total_sales = Sale.objects.count()

    total_products = Product.objects.count()

    production_count = Production.objects.count()

    total_stock = 0

    products = Product.objects.all()

    pending_productions = Production.objects.filter(
        approved=False
    ).order_by('-id')

    approved_productions = Production.objects.filter(
        approved=True
    ).order_by('-id')

    for i in products:

        total_stock += i.stock

    context = {

        'total_sales': total_sales,

        'total_products': total_products,

        'production_count': production_count,

        'total_stock': total_stock,

        'pending_productions': pending_productions,

        'approved_productions': approved_productions

    }

    return render(

        request,

        'dashboard.html',

        context

    )


# EXPORT SALES EXCEL

def export_sales_excel(request):

    sales = Sale.objects.all().values()

    df = pd.DataFrame(sales)

    response = HttpResponse(

        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    )

    response['Content-Disposition'] = (

        'attachment; filename=sales.xlsx'

    )

    df.to_excel(response, index=False)

    return response


# EXPORT RAW MATERIAL EXCEL

def export_material_excel(request):

    materials = RawMaterial.objects.all().values()

    df = pd.DataFrame(materials)

    response = HttpResponse(

        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    )

    response['Content-Disposition'] = (

        'attachment; filename=raw_material.xlsx'

    )

    df.to_excel(response, index=False)

    return response