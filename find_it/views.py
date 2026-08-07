#import from django
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

#import local
from find_it.mixins import UserIsOverMixin
from find_it import models
from find_it.models import Product, Store
from find_it.forms import ProductForm, ProductFilterForm, StoreForm
from find_it.decorators import company_required


#Views
def index(request):
    showcase_products = Product.objects.all().order_by('?')[:3]  # 3 random products for cards
    products = Product.objects.all().order_by('?')[:6]           # 6 random products for the list
    return render(request, template_name='find_it/index.html', context={
        'showcase_products': showcase_products,  # For the 3 cards
        'products': products                      # For the "Some products that might be interesting" section
    })

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

@method_decorator(company_required, name='dispatch')
class ProductsManagementView(LoginRequiredMixin, View):
    template_name = "find_it/products/products_management.html"

    def get(self, request):
        products = Product.objects.filter(creator=request.user)
        form = ProductForm()
        return render(request, self.template_name, {'products': products, 'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.creator = request.user
            product.save()
            return redirect('find_it:products-management')
        else:
            products = Product.objects.filter(creator=request.user)
            return render(request, self.template_name, {'products': products, 'form': form})

@method_decorator(company_required, name='dispatch')
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Product
    form_class = ProductForm
    template_name = "find_it/products/product_update.html"
    success_url = reverse_lazy("find_it:list-product")

class ProductDeleteView(LoginRequiredMixin, UserIsOverMixin, DeleteView):
    model = models.Product
    template_name = "find_it/products/product_delete_confirmation.html"
    success_url = reverse_lazy("find_it:product-management")

@method_decorator(company_required, name='dispatch')
class StoreManagementView(LoginRequiredMixin, View):
    template_name = "find_it/store/store_management.html"

    def get(self, request):
        stores = Store.objects.filter(creator=request.user)
        form = StoreForm()
        return render(request, self.template_name, {'stores': stores, 'form': form})

    def post(self, request):
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.creator = request.user      
            store.save()                      
            return redirect('find_it:store-management')
        else:
            stores = Store.objects.filter(creator=request.user)
            return render(request, self.template_name, {'stores': stores, 'form': form})

@method_decorator(company_required, name='dispatch')       
class StoreUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Store
    form_class = StoreForm
    template_name = "find_it/store/store_update_form.html"
    success_url = reverse_lazy("find_it:store-management")

@method_decorator(company_required, name='dispatch')       
class StoreDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Store
    success_url = reverse_lazy("find_it:store-management")
    template_name = "find_it/store/store_delete_confirmation.html"

