from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render


from .models import Product
from .forms import ProductModelForm

# Create your views here.
#def bad_view(request, *args, **kwargs):
#     # print(dict(request.GET))
#     my_request_data = dict(request.GET)
#     new_product = my_request_data.get("new_product")
#     print(my_request_data, new_product)
#     if new_product[0].lower() == "true":
#         print("new product")
#         Product.objects.create(title=my_request_data.get('title')[0], content=my_request_data.get('content')[0])
#     return HttpResponse("Dont do this")

def search_view(request, *args, **kwargs): # /search/
    # before use templates
    # return HttpResponse("<h1> Hello world </h1>")
    query = request.GET.get('q', " ") # q
    qs = Product.objects.filter(title__icontains=query)
    print(query, qs)
    # after use templates
    context = {"name": "abc", "query": query}
    return render (request, "home.html", context)

#def product_create_view(request, *args, **kwargs):
#    print(request.POST)
#    print(request.GET)
#    if request.method == "POST":
#        post_data = request.POST or None
#        if post_data != None:
#            my_form = ProductForm(request.POST)
#            if my_form.is_valid():
#                print(my_form.cleaned_data.get("title"))
#                title_from_input = my_form.cleaned_data.get("title")
#                Product.objects.create(title=title_from_input)
#            #print ("post_data", post_data)
#    return render(request, "form.html", {})

@staff_member_required
def product_create_view(request, *args, **kwargs):
    form = ProductModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        image = request.FILES.get('image')
        media = request.FILES.get('media')
        # do some stuff
        if image:
            obj.image = image
        if media:
            obj.media = media
        obj.user = request.user
        obj.save()
        #print(form.cleaned_data)
        #data = form.cleaned_data
        #Product.objects.create(**data)
        # Product(**data)
        form = ProductModelForm()

    return render(request, "form.html", {"form": form})


def product_detail_view(request, pk): #/products/<int:pk>/
    #obj = Product.objects.get(id=id)
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        # render html page, with HTTP status code of 404
        raise Http404
    # before templates/detail.html
    #return HttpResponse(f"Product id {obj.id}")
    return render(request,"products/detail.html", {"object": obj})

def product_api_detail_view(request, pk):
    #obj = Product.objects.get(id=id)
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        # return Json with HTTP status code of 404
        return JsonResponse ({"message": "Not found"})

    return JsonResponse({"id": obj.id})


# views also can be class
#class HomeView:
#   return