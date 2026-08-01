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
    products = Product.objects.all().order_by('?')[:6]  # Random 6 products
    return render(request, template_name='find_it/index.html', context={'products': products})

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
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = models.Product
    template_name = "find_it/products/product_form.html"

    form_class = ProductForm
    success_url = reverse_lazy("find_it:list-product")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

@method_decorator(company_required, name='dispatch')
class StoreManagementView(LoginRequiredMixin, UserIsOverMixin, View):
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
class StoreUpdateView(LoginRequiredMixin, UserIsOverMixin, UpdateView):
    model = models.Store
    form_class = StoreForm
    template_name = "find_it/store/store_update_form.html"
    success_url = reverse_lazy("find_it:store-management")

@method_decorator(company_required, name='dispatch')       
class StoreDeleteView(LoginRequiredMixin, UserIsOverMixin, DeleteView):
    model = models.Store
    success_url = reverse_lazy("find_it:store-management")
    template_name = "find_it/store/store_delete_confirmation.html"

