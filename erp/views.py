from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.db.models import Q

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import *

import pandas as pd


# =========================================
# HOME
# =========================================

def home(request):

    return render(request, 'home.html')


# =========================================
# ADMIN LOGIN
# =========================================

def admin_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(

            request,

            username=username,

            password=password

        )

        if user is not None and user.username == 'CM_Admin':

            login(request, user)

            return redirect('/dashboard')

        else:

            messages.error(

                request,

                'Invalid Admin Login'

            )

    return render(

        request,

        'admin_login.html'

    )


# =========================================
# SALES LOGIN
# =========================================

def sales_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(

            request,

            username=username,

            password=password

        )

        if user is not None and user.username == 'CM_Sales':

            login(request, user)

            return redirect('/sales')

        else:

            messages.error(

                request,

                'Invalid Sales Login'

            )

    return render(

        request,

        'sales_login.html'

    )


# =========================================
# MANUFACTURE LOGIN
# =========================================

def manufacture_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(

            request,

            username=username,

            password=password

        )

        if user is not None and user.username == 'CM_PR':

            login(request, user)

            return redirect('/production')

        else:

            messages.error(

                request,

                'Invalid Manufacture Login'

            )

    return render(

        request,

        'manufacture_login.html'

    )


# =========================================
# LOGOUT
# =========================================

@login_required
def logout_view(request):

    logout(request)

    return redirect('/')


# =========================================
# SALES PAGE
# =========================================

@login_required
def sales_page(request):

    if (

        request.user.username != 'CM_Sales'

        and

        request.user.username != 'CM_Admin'

    ):

        return HttpResponseForbidden(

            "Sales/Admin Access Only"

        )

    products = Product.objects.all()

    if request.method == 'POST':

        date = request.POST.get('date')

        rd_name = request.POST.get('rd_name')

        retail_partner = request.POST.get(

            'retail_partner'

        )

        mobile = request.POST.get('mobile')

        customer_name = request.POST.get(

            'customer_name'

        )

        sales_person_name = request.POST.get(

            'sales_person_name'

        )

        address = request.POST.get('address')

        collected_payment = request.POST.get(

            'collected_payment'

        )

        due = request.POST.get('due')

        product_id = request.POST.get(

            'product'

        )

        bag_count = request.POST.get(

            'bag_count'

        )

        unit_price = request.POST.get(

            'unit_price'

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

            customer_name=customer_name,

            sales_person_name=sales_person_name,

            address=address,

            product=product,

            bag_count=int(bag_count),

            unit_price=float(unit_price),

            collected_payment=float(

                collected_payment

            ),

            due=float(due)

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


# =========================================
# SALES DETAILS
# =========================================

@login_required
def sales_details(request):

    if (

        request.user.username != 'CM_Sales'

        and

        request.user.username != 'CM_Admin'

    ):

        return HttpResponseForbidden(

            "Sales/Admin Access Only"

        )

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


# =========================================
# EDIT SALE
# =========================================

@login_required
def edit_sale(request, id):

    if (

        request.user.username != 'CM_Sales'

        and

        request.user.username != 'CM_Admin'

    ):

        return HttpResponseForbidden(

            "Sales/Admin Access Only"

        )

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

        sale.customer_name = request.POST.get(

            'customer_name'

        )

        sale.sales_person_name = request.POST.get(

            'sales_person_name'

        )

        sale.address = request.POST.get(

            'address'

        )

        sale.collected_payment = float(

            request.POST.get(

                'collected_payment'

            )

        )

        sale.due = float(

            request.POST.get('due')

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


# =========================================
# DELETE SALE
# =========================================

@login_required
def delete_sale(request, id):

    if (

        request.user.username != 'CM_Sales'

        and

        request.user.username != 'CM_Admin'

    ):

        return HttpResponseForbidden(

            "Sales/Admin Access Only"

        )

    sale = Sale.objects.get(id=id)

    sale.delete()

    messages.success(

        request,

        'Sale Deleted Successfully'

    )

    return redirect('/sales-details')


# =========================================
# STOCK OVERVIEW
# =========================================

@login_required
def stock_overview(request):

    products = Product.objects.all()

    return render(

        request,

        'stock.html',

        {

            'products': products

        }

    )


# =========================================
# PRODUCTION PAGE
# =========================================

@login_required
def production_page(request):

    if (
        request.user.username != 'CM_PR'
        and
        request.user.username != 'CM_Admin'
    ):

        return HttpResponseForbidden(
            "Manufacture/Admin Access Only"
        )

    products = Product.objects.all()

    if request.method == 'POST':

        product_id = request.POST.get('product')

        date = request.POST.get('date')

        bag_count = request.POST.get('bag_count')

        print("POST PRODUCT ID:", product_id)

        product = Product.objects.filter(
            id=product_id
        ).first()

        if not product:

            messages.error(
                request,
                f'Product ID {product_id} Not Found'
            )

            return redirect('/production')

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


# =========================================
# APPROVE PRODUCTION
# =========================================

@login_required
def approve_production(request, id):

    if request.user.username != 'CM_Admin':

        return HttpResponseForbidden(

            "Admin Access Only"

        )

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


# =========================================
# EDIT PRODUCTION
# =========================================

@login_required
def edit_production(request, id):

    if request.user.username != 'CM_Admin':

        return HttpResponseForbidden(

            "Admin Access Only"

        )

    production = Production.objects.get(id=id)

    products = Product.objects.all()

    if request.method == 'POST':

        production.date = request.POST.get(

            'date'

        )

        product_id = request.POST.get(

            'product'

        )

        production.product = Product.objects.get(

            id=product_id

        )

        production.bag_count = int(

            request.POST.get(

                'bag_count'

            )

        )

        production.save()

        messages.success(

            request,

            'Production Updated Successfully'

        )

        return redirect('/dashboard')

    return render(

        request,

        'edit_production.html',

        {

            'production': production,

            'products': products

        }

    )


# =========================================
# DELETE PRODUCTION
# =========================================

@login_required
def delete_production(request, id):

    if request.user.username != 'CM_Admin':

        return HttpResponseForbidden(

            "Admin Access Only"

        )

    production = Production.objects.get(id=id)

    production.delete()

    messages.success(

        request,

        'Production Deleted Successfully'

    )

    return redirect('/dashboard')


# =========================================
# RAW MATERIAL PAGE
# =========================================

@login_required
def raw_material(request):

    if (

        request.user.username != 'CM_PR'

        and

        request.user.username != 'CM_Admin'

    ):

        return HttpResponseForbidden(

            "Manufacture/Admin Access Only"

        )

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


# =========================================
# EDIT MATERIAL
# =========================================

@login_required
def edit_material(request, id):

    if (

        request.user.username != 'CM_PR'

        and

        request.user.username != 'CM_Admin'

    ):

        return HttpResponseForbidden(

            "Manufacture/Admin Access Only"

        )

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

            request.POST.get('current_balance')

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


# =========================================
# DELETE MATERIAL
# =========================================

@login_required
def delete_material(request, id):

    if (

        request.user.username != 'CM_PR'

        and

        request.user.username != 'CM_Admin'

    ):

        return HttpResponseForbidden(

            "Manufacture/Admin Access Only"

        )

    material = RawMaterial.objects.get(id=id)

    material.delete()

    messages.success(

        request,

        'Material Deleted Successfully'

    )

    return redirect('/raw-material')


# =========================================
# ADMIN DASHBOARD
# =========================================

@login_required
def admin_dashboard(request):

    if request.user.username != 'CM_Admin':

        return HttpResponseForbidden(

            "Admin Access Only"

        )

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


# =========================================
# EXPORT SALES EXCEL
# =========================================

@login_required
def export_sales_excel(request):

    sales = Sale.objects.all().values(

        'bill_no',
        'date',
        'rd_name',
        'retail_partner',
        'mobile',
        'customer_name',
        'sales_person_name',
        'address',
        'product_id',
        'bag_count',
        'unit_price',
        'total_price',
        'collected_payment',
        'due'

    )

    df = pd.DataFrame(sales)

    response = HttpResponse(

        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    )

    response['Content-Disposition'] = (

        'attachment; filename=sales.xlsx'

    )

    df.to_excel(response, index=False)

    return response


# =========================================
# EXPORT MATERIAL EXCEL
# =========================================

@login_required
def export_material_excel(request):

    materials = RawMaterial.objects.all().values(

        'item_name',
        'date',
        'used_kg',
        'current_balance'

    )

    df = pd.DataFrame(materials)

    response = HttpResponse(

        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    )

    response['Content-Disposition'] = (

        'attachment; filename=raw_material.xlsx'

    )

    df.to_excel(response, index=False)

    return response