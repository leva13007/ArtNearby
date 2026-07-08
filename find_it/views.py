from django.shortcuts import render
from find_it import models
from find_it.forms import TaskFilterForm
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView

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
        context["form"] = TaskFilterForm(self.request.GET)
        return context
    
class ProductDetailView(DetailView):
    model = models.Product
    context_object_name = "product"
    template_name = "find_it/product_detail.html"