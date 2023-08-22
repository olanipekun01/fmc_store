from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import *
from .forms import *
from django.contrib import messages

from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
from datetime import datetime

import csv
from django.http import HttpResponse


def is_valid(param):
    return param != "" and param is not None

# Create your views here.

@login_required
def index(request):
    dept = Department.objects.all()
    items = Items.objects.all()
    history = History.objects.all()
    # dept = Department.objects.all()
    total_items = len(items)
    out_of_stock = len(items.filter(amount__lt=11))
    suppliers = len(history.filter(action="received"))
    issued = len(dept)
    
  
    context = {
        "total_items": total_items,
        "out_of_stock": out_of_stock,
        "suppliers": suppliers,
        "issued": issued
    }
    return render(request, 'index.html', context)


@login_required
def dept(request):
    if request.method == "POST":
        op_type = request.POST["op_type"]
        if op_type == "add":
            input_name = request.POST['input_name']
            input_voucher = request.POST['input_voucher']
            input_supplier_name = request.POST['input_supplier_name']
            input_amount = request.POST['input_amount']
            input_unit_issue = request.POST["input_unit_issue"]
            input_unit_rate = request.POST["input_unit_rate"]
            if validate(input_amount) == True:
                item = Items.objects.all().filter(item_name=input_name)[0]
                amnt = int(input_amount)
                item.amount += amnt
                item.unit_issue = input_unit_issue
                item.unit_rate = input_unit_rate
                item.save()
                history = History.objects.create(item_name=item.item_name, 
                                                 voucher_no=input_voucher,
                                                 description=input_supplier_name,
                                                 action="received",
                                                 amount=str(amnt), 
                                                 bal=str(item.amount), 
                                                 unit_issue=input_unit_issue,
                                                 unit_rate=input_unit_rate,
                                                 slug=item.slug)
                history.save()
                return redirect('/dept')
            else:
                messages.info(request, 'enter a valid amount')
                return redirect('/dept')
        elif op_type == "subtract":
            input_name = request.POST['input_name']
            input_voucher = request.POST['input_voucher']
            input_dept_name = request.POST['input_dept_name']
            input_amount = request.POST['input_amount']
            input_unit_issue = request.POST["input_unit_issue"]
            input_unit_rate = request.POST["input_unit_rate"]
            if validate(input_amount) == True:
                item = Items.objects.all().filter(item_name=input_name)[0]
                if item.amount >= int(input_amount):
                    amnt = int(input_amount)
                    item.amount -= amnt
                    item.save()
                    history = History.objects.create(item_name=item.item_name, 
                                                     voucher_no=input_voucher,
                                                    description=input_dept_name,
                                                    action="issued",
                                                    amount=str(amnt), 
                                                    bal=str(item.amount), 
                                                    unit_issue=input_unit_issue,
                                                    unit_rate=input_unit_rate,
                                                     slug=item.slug)
                    history.save()
                    return redirect('/dept');
                else:
                    messages.info(request, 'Not enough in stock')
                    return redirect('/dept');
            else:
                messages.info(request, 'enter a valid amount')
                return redirect('/dept' )
    
    item_name_input = request.GET.get('item_name')
    min_amnt = request.GET.get('min_amnt')
    max_amnt = request.GET.get('max_amnt')
    issue_unit = request.GET.get('issue_unit')
     
    
    dept = Department.objects.all()
    items = Items.objects.all()
    
    if is_valid(item_name_input):
        items = items.filter(item_name__contains=item_name_input)
        
    if is_valid(min_amnt):
        items = items.filter(amount__gte=min_amnt)
    
    if is_valid(max_amnt):
        items = items.filter(amount__lt=max_amnt)
    
    if is_valid(issue_unit):
        items = items.filter(unit_issue__icontains=issue_unit)
    
    return render(request, 'dept1.html', {'department': dept, 'items': items})


@login_required
def newstock(request):
    if request.method == "POST":
        item_name = request.POST['item_name']
        item_amount = request.POST['item_amount']
        input_unit_issue = request.POST['input_unit_issue']
        input_unit_rate = request.POST['input_unit_rate']

        if Items.objects.all().filter(item_name=item_name).exists():
            return redirect("/dept/"+dept)  
        else:
            test = uuid.uuid4()
            items = Items.objects.create(item_id=test,
                item_name=item_name, amount=item_amount, unit_issue=input_unit_issue, unit_rate=input_unit_rate)
            items.save()
            item = Items.objects.all().filter(item_name=item_name)[0]
            history = History.objects.create(item_id=str(item.item_id), 
                                             item_name=item.item_name, 
                                             voucher_no="",
                                             description="",
                                             action="added",
                                             amount=str(item_amount), 
                                             bal=str(item.amount), 
                                             unit_issue=input_unit_issue,
                                             unit_rate=input_unit_rate,
                                             slug=item.slug)
            history.save()
            return redirect("/dept")   
    return render(request, 'index.html')

@login_required
def history(request, item=""):
    history = History.objects.all()

    item_name_input = request.GET.get('item_name')
    description = request.GET.get('description')
    issue_unit = request.GET.get('issue_unit')
    # rate_unit = request.GET.get('rate_unit')
    min_date_string = request.GET.get('min_date')
    max_date_string = request.GET.get('max_date')
    action = request.GET.get('action')
    
    if item != "":
        history = history.filter(slug=item)
    else:
        if is_valid(item_name_input):
            history = history.filter(item_name__icontains=item_name_input)
        
        if is_valid(description):
            history = history.filter(description__icontains=description)
        
        if is_valid(action) and action != "Choose...":
            history = history.filter(action__iexact=action)
        
        if is_valid(issue_unit):
            history = history.filter(unit_issue__iexact=issue_unit)
            
        # if is_valid(rate_unit):
        #     print("rateping")
        #     history = history.filter(unit_rate=rate_unit)
            
        if is_valid(min_date_string):
            specific_date = datetime.strptime(min_date_string, '%Y-%m-%d').date()
            print("min date", min_date_string)
            print("specific date", specific_date)
            # formatted_date = specific_date.strftime('%B %d, %Y')
            history = history.filter(dateCreated__gte=specific_date)
            
        
        if is_valid(max_date_string):
            specific_date = datetime.strptime(max_date_string, '%Y-%m-%d').date()
            # formatted_date = specific_date.strftime('%B %d, %Y')
            history = history.filter(dateCreated__lt=specific_date)
        
    
        
    history = history.order_by('-date_created')
    history = history.values()
    
    if request.method == "POST":
        # Create the CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="my_model.csv"'
        
        # Write model data to the CSV file
        writer = csv.writer(response)
        writer.writerow(['date', 'item', 'voucher no', 'action', 'description', 'unit issue', 'unit rate', 'amount', 'balance'])
        for obj in history:
            writer.writerow([obj.dateCreated, obj.item_name, obj.voucher_no, obj.action, obj.description, obj.unit_issue, obj.unit_rate, obj.amount, obj.bal])

        return response
    
    
    p = Paginator(history, 7)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # print('obj', page_obj.object_list)
    acts = ["issued","received", "removed", "added"]
    context = {'page_obj': page_obj, "actions": acts}
    
    return render(request, 'history.html', context)



@login_required
def delete(request, id):
    item = Items.objects.filter(item_id=id)[0]
    history = History.objects.create(item_id=str(item.item_id), 
                                    item_name=item.item_name, 
                                    voucher_no="",
                                    description="",
                                    action="removed",
                                    amount=str(item.amount), 
                                    bal=str(0), 
                                    unit_issue=item.unit_issue,
                                    unit_rate=item.unit_rate,
                                    slug=item.slug)
    history.save()
    items = Items.objects.filter(item_id=id).delete()
    return redirect("/dept")
    

def login(request):
    if request.method  == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credetials Invalid')
            return redirect('/login')
    else:
        return render(request, 'login.html')
        
    # return render(request, 'login.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def department(request):
    dept = Department.objects.all()
    
    if request.method == "POST":
        dept_name = request.POST["dept_name"]
        
        if dept.filter(dept_name=dept_name).exists():
            messages.info(request, 'Department exist')
            return redirect("/department")
        
        dept = dept.create(dept_name=dept_name)
        
        dept.save()
        
        return redirect("/department")
    
    return render(request, 'department.html', {"department": dept})

@login_required
def removeDept(request, id):
    dept = Department.objects.filter(dept_name=id).delete()
    
    return redirect("/department")

@login_required
def outOfStock(request):
    items = Items.objects.all()
    items = items.filter(amount__lt=11)
    arr = [item.item_name for item in items]
    return render(request, 'base.html', {"names": arr})

@login_required
def suppliers(request):
    history = History.objects.all()
    supliers = history.filter(action="received")
    arr = [sup.description for sup in supliers]
    
    return render(request, 'base.html', {"names": arr})