from django.shortcuts import render, redirect
from find_it import models
from django.contrib.auth.decorators import login_required
from find_it.forms import *
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from find_it.models import Product
from django import forms
from find_it.forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    return render(request, template_name="find_it/index.html")

class ProductListView(ListView):
    model = models.Product
    context_object_name = "find_it"
    template_name = "find_it/product_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get("category", "")
        if category:
            queryset = queryset.filter(category=category)
        return queryset
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["form"] = ProductFilterForm(self.request.GET)
        return context
    

def get_post_by_id(request, post_id):
    product = Product.objects.get(id=post_id)
    context = {
        "product": product
    }
    return render(request,
                    template_name="find_it/product_detail.html",
                    context=context
    )

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = models.Product
    template_name = "find_it/product_form.html"

    form_class = ProductForm()
    success_url = reverse_lazy("find_it:list-product")

    def form_valid(self, form):
        #form.instance.creator = self.request.user
        return super().form.valid(form)
    