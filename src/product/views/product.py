import datetime
from django.core.files.storage import FileSystemStorage

from django.http.response import JsonResponse
from django.views import generic


from product.models import ProductImage, ProductVariant, Variant,Product
from django.shortcuts import get_object_or_404
from django.db.models import Q


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class UpdateProductView(generic.TemplateView):
    template_name = 'products/update.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')

        context['product'] = True
        context['variants'] = list(variants.all())

        # context['object']= Product.objects.get(kwargs.get('pk'))
        get_object_or_404(Product,pk=kwargs.get('pk'))
        context['pk']=kwargs.get('pk')


        return context



def uploadProductImage(request):
    # print(request.POST)
    if request.method=='POST':
        pk=request.POST.get('pk')
        product=get_object_or_404(Product,pk=pk)
        for key in request.FILES:
            
            fs = FileSystemStorage()
            filename = fs.save('product_images/'+request.FILES[key].name, request.FILES[key])
            uploaded_file_url = fs.url(filename)

            ProductImage.objects.create(
                product=product,
                file_path=uploaded_file_url
            )
        return JsonResponse(data={"details":"image been uploaded"}) 
    return JsonResponse(data={'detail':"opps"},status_code=404)

class ProductList(generic.ListView):
    template_name='products/list.html'
    model = Product 
    paginate_by = 2
    def get_queryset(self) :

        title=self.request.GET.get('title',None)
        price_from=self.request.GET.get('price_from',None)
        price_to=self.request.GET.get('price_to',None)
        date=self.request.GET.get('date',None)
        variant=self.request.GET.get('variant',None)

        
        # print('here',)
            



        qs= Product.objects.all()
        if title:
            qs=qs.filter(title__icontains=title)
        if date:
            try:
                date=datetime.datetime.strptime(date, '%Y-%m-%d').date()
                qs=qs.filter(created_at=date)
            except:
                pass 

        if price_from and price_to:
            qs=qs.filter(
                Q(productvariantprice__price__gte=price_from),
                Q(productvariantprice__price__lte=price_to),
            )
        if variant:
            qs=qs.filter( 
                Q(productvariantprice__product_variant_one__variant_title__icontains=variant)|
                Q(productvariantprice__product_variant_two__variant_title__icontains=variant)|
                Q(productvariantprice__product_variant_three__variant_title__icontains=variant),
                )

        return qs

    def get_context_data(self,**kwargs):
        context = super(ProductList,self).get_context_data(**kwargs)
        # context['variants']=Variant.objects.all()
        variant_grp={}

        for pv in ProductVariant.objects.all().select_related('variant'):
            if pv.variant.title in variant_grp:
                variant_grp[pv.variant.title].add(pv.variant_title.lower())
            else:
                variant_grp[pv.variant.title]=set([pv.variant_title.lower()])

            
        context['variant_grp']=variant_grp
        
    
        return context

