#import from django

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse

#import local
from find_it.mixins import UserIsOverMixin
from find_it import models
from find_it.models import Product, Store
from find_it.forms import ProductForm, ProductFilterForm, StoreForm

# Create your views here.

def index(request):
    return render(request, template_name="find_it/index.html")

def get_product_by_id(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        "product": product
    }
    return render(request,
                    template_name="find_it/product_detail.html",
                    context=context
    )

class ProductDetailView(DetailView):
    model = models.Product
    context_object_name = "product"
    template_name = "find_it/products/product_detail.html"


class ProductListView(ListView):
    model = models.Product
    context_object_name = "products"
    template_name = "find_it/products/product_list.html"

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

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = models.Product
    template_name = "find_it/products/product_form.html"

    form_class = ProductForm
    success_url = reverse_lazy("find_it:list-product")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class StoreManagementView(LoginRequiredMixin, View):
    template_name = "find_it/store/store_management.html"

    def get(self, request):
        stores = Store.objects.filter(name=request.user)
        form = StoreForm()
        print(f"GET: Found {stores.count()} stores for user {request.user.id}")  # Debug
        return render(request, self.template_name, {'stores': stores, 'form': form})

    def post(self, request):
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)  # Don't save to DB yet
            store.creator = request.user      # Set the creator to the current user
            store.save()                      # Now save to DB
            return redirect('find_it:store-management')
        else:
            stores = Store.objects.filter(creator=request.user)
            return render(request, self.template_name, {'stores': stores, 'form': form})
        
class StoreUpdateView(LoginRequiredMixin, UserIsOverMixin, UpdateView):
    model = models.Store
    form_class = StoreForm
    template_name = "find_it/store/store_update_form.html"
    success_url = reverse_lazy("find_it:store-management")
        
class StoreDeleteView(LoginRequiredMixin, UserIsOverMixin, DeleteView):
    model = models.Store
    success_url = reverse_lazy("find_it:store-management")
    template_name = "find_it/store/store_delete_confirmation.html"

