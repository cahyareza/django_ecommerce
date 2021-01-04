import pathlib
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from products.models import Product
from .models import Order
from .forms import OrderForm

@login_required
def order_checkout_view(request):
    qs = Product.objects.filter(featured=True)
    if not qs.exists():
        return redirect("/")
    product = qs.first()
    user = request.user # Anonuser
    order_id = request.session.get("order_id")
    order_obj = None
    new_creation = False
    try:
        order_obj = Order.objects.get(id=order_id)
    except:
        order_id = None
    if order_id == None:
        new_creation = True
        order_obj = Order.objects.create(product=product, user=user)
    if order_obj != None and new_creation == False:
        if order_obj.product.id != product.id:
            order_obj = Order.objects.create(product=product, user=user)
    request.session['order_id'] = order_obj.id

    form = OrderForm(request.POST or None, product=product, instance=order_obj)
    if form.is_valid():
        order_obj.shipping_address = form.cleaned_data.get("shipping_address")
        order_obj.billing_address = form.cleaned_data.get("billing_address")
        order_obj.mark_paid(save=False)
        order_obj.save()
        del request.session['order_id']
        request.session['checkout_success_order_id'] = order_obj.id
        return redirect("/success")
    return render(request, 'orders/checkout.html', {"form": form, "object": order_obj})

def download_order(request, *args, **kwargs):
    '''
    Download our order product media
    if it exists.
    '''
    order_id = 'abc'
    qs = Product.objects.filter(media_isnull=False)
    project_obj = qs.first()
    if not project_obj.media:
        raise Http404
    product_path = media.path #/abc/adsg/jajj/media/ads.csv
    path = pathlib.Path(product_path)
    pk = product_obj.pk
    ext = path.suffix #.csv .png .mov
    fname = f"my-cool-product-{order_id}-{pk}{ext}"
    with open(path):

    return HttpResponse