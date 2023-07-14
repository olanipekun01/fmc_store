from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import *
from .forms import *
from django.contrib import messages

from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid




# Create your views here.


def index(request):
    dept = Department.objects.all()
    return render(request, 'index.html', {'dept': dept})


def dept(request, pk):
    if request.method == "POST":
        input_name = request.POST['input_name']
        input_amount = request.POST['input_amount']
        op_type = request.POST['op_type']
        if op_type == "add":
            if validate(input_amount) == True:
                item = Items.objects.all().filter(item_name=input_name, dept__dept_name=pk)[0]
                amnt = int(input_amount)
                item.amount += amnt
                item.save()
                history = History.objects.create(item_name=item.item_name, amount="+ "+str(amnt), bal=str(item.amount), dept=item.dept, slug=item.slug)
                history.save()
                return redirect('/dept/' + pk)
            else:
                messages.info(request, 'enter a valid amount')
                return redirect('/dept/' + pk)
        elif op_type == "subtract":
            if validate(input_amount) == True:
                item = Items.objects.all().filter(item_name=input_name, dept__dept_name=pk)[0]
                if item.amount >= int(input_amount):
                    amnt = int(input_amount)
                    item.amount -= amnt
                    item.save()
                    history = History.objects.create(item_name=item.item_name, amount="- "+str(amnt), bal=str(item.amount), dept=item.dept, slug=item.slug)
                    history.save()
                    return redirect('/dept/'+pk);
                else:
                    messages.info(request, 'Not enough in stock')
                    return redirect('/dept/'+pk);
            else:
                messages.info(request, 'enter a valid amount')
                return redirect('/dept/' + pk)
    dept = Department.objects.all()
    items = Items.objects.all().filter(dept__dept_name=pk)
    return render(request, 'dept1.html', {'dept': dept, 'active_dept': pk, 'items': items})


def newstock(request):
    if request.method == "POST":
        item_name = request.POST['item_name']
        item_amount = request.POST['item_amount']
        dept = request.POST['dept']

        if Items.objects.all().filter(item_name=item_name).exists():
            return redirect("/dept/"+dept)  
        else:
            test = uuid.uuid4()
            items = Items.objects.create(item_id=test,
                item_name=item_name, amount=item_amount, dept=Department.objects.all().filter(dept_name=dept)[0])
            items.save()
            item = Items.objects.all().filter(item_name=item_name)[0]
            history = History.objects.create(item_id=str(item.item_id), item_name=item.item_name, amount="+ "+str(
                item_amount), bal=str(item_amount), dept=item.dept, slug=item.slug)
            history.save()
            return redirect("/dept/"+dept)   
    return render(request, 'index.html')

def history(request, pk, item=""):
    if item != "":
        history = History.objects.all().filter(dept__dept_name=pk, slug=item).order_by('-date_created')
        history = history.values()
    else:
        history = History.objects.all().filter(dept__dept_name=pk).order_by('-date_created')
        history = history.values()
    
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
    context = {'page_obj': page_obj, "active_dept":pk}
    
    return render(request, 'history.html', context)

def login(request):
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
