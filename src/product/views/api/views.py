from django.http.response import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND


from product.models import  ProductVariant, ProductVariantPrice, Variant,Product
from django.shortcuts import get_object_or_404
def extract_data(product):
    variants=Variant.objects.all()
    product_variant=[]
    for variant in variants:
        tags=product.productvariant_set.filter(
            variant=variant
        ).values_list('variant_title', flat=True)

        ids=product.productvariant_set.filter(
            variant=variant
        ).values_list('id', flat=True)

        product_variant.append({
            'option':variant.id,
            'tags':tags,
        })
    product_variant_prices=[]
      

    for variant_price in ProductVariantPrice.objects.filter(product=product):

        product_variant_prices.append(
            {
                'title':str(variant_price),
                'price':variant_price.price,
                'stock':variant_price.stock,

            }
        ) 

    # print(product_variant_prices)

    data={
        'product_name': product.title,
        'product_sku': product.sku,
        'description': product.description,
        "product_variant":product_variant,
        'product_variant_prices':product_variant_prices,
    } 

    return data 

@api_view(['get'])
def getProduct(request,pk):
    product=get_object_or_404(Product,pk=pk)

    data=extract_data(product)
    
    return Response(data=data)


@api_view(['POST'])
@parser_classes([JSONParser])
def createNewProduct(request,format=None):

    # print(request.POST)
    
        
    

    product=Product.objects.create(
            title=request.data.get('title'),
            sku=request.data.get('sku'),
            description=request.data.get('description')
        )


        

    

        
    # print(product.id)


    productVariant={}
    varients=request.data.get('product_variant')
    for v in varients:
        
        for title in v['tags']:
            pvobj=ProductVariant.objects.create(
                variant_title= title,
                variant=Variant.objects.get(id=int(v['option'])) ,
                product=product
            )
            productVariant[title.lower()]=pvobj
    # extract product variant price 

    '''
    example :
    0:
        price: "1"
        stock: "1"
        title: "red/xl/pk/"

    '''
    for product_v_p in  request.data.get('product_variant_prices'):
        productV = product_v_p['title'].split('/')

        print(productV)

        if len(productV[-1])==0:
            productV=productV[0:-1]


        

        if len(productV)==1:
            obj=ProductVariantPrice.objects.create(
                price=product_v_p.get('price'),
                stock=product_v_p.get('stock'),
                product=product,
                product_variant_one=productVariant[productV[0]],
            )
        elif len(productV)==2:
            obj=ProductVariantPrice.objects.create(
                price=product_v_p.get('price'),
                stock=product_v_p.get('stock'),
                product=product,
                product_variant_one=productVariant[productV[0]],
                product_variant_two=productVariant[productV[1]],
            )
        elif len(productV)==3:
            obj=ProductVariantPrice.objects.create(
                price=product_v_p.get('price'),
                stock=product_v_p.get('stock'),
                product=product,
                product_variant_one=productVariant[productV[0]],
                product_variant_two=productVariant[productV[1]],
                product_variant_three=productVariant[productV[2]],
            )
        else :
            return   Response({'detalis': 'product variant price cant added', 'pk': product.pk},status=HTTP_404_NOT_FOUND)

    return Response({'detalis': 'ok', 'pk': product.pk},status=HTTP_201_CREATED)

    
@api_view(['POST'])
@parser_classes([JSONParser])
def updateProduct(request,pk):

    
    product=get_object_or_404(Product,pk=pk)
 

    product.title=request.data.get('title')
    product.sku=request.data.get('sku')
    product.description=request.data.get('description')
    product.save()
    ProductVariant.objects.filter(product=product).delete()
    ProductVariantPrice.objects.filter(product=product).delete()

        
    # print(product.id)


    productVariant={}
    varients=request.data.get('product_variant')
    for v in varients:
        
        for title in v['tags']:
            productVariant[title.lower()]=ProductVariant.objects.create(
                variant_title= title,
                variant=Variant.objects.get(id=int(v['option'])) ,
                product=product
            )
    # extract product variant price 

    '''
    example :
    0:
        price: "1"
        stock: "1"
        title: "red/xl/pk/"

    '''
    for product_v_p in  request.data.get('product_variant_prices'):
        productV = product_v_p['title'].split('/')

        

        if len(productV[-1])==0:
            productV=productV[0:-1]
        print(productV)
        if len(productV)==1:
            obj=ProductVariantPrice.objects.create(
                price=product_v_p.get('price'),
                stock=product_v_p.get('stock'),
                product=product,
                product_variant_one=productVariant[productV[0]],
            )
        elif len(productV)==2:
            obj=ProductVariantPrice.objects.create(
                price=product_v_p.get('price'),
                stock=product_v_p.get('stock'),
                product=product,
                product_variant_one=productVariant[productV[0]],
                product_variant_two=productVariant[productV[1]],
            )
        elif len(productV)==3:
            obj=ProductVariantPrice.objects.create(
                price=product_v_p.get('price'),
                stock=product_v_p.get('stock'),
                product=product,
                product_variant_one=productVariant[productV[0]],
                product_variant_two=productVariant[productV[1]],
                product_variant_three=productVariant[productV[2]],
            )
        else :
            return   Response({'detalis': 'product variant price cant added', 'pk': product.pk},status=HTTP_404_NOT_FOUND)
    return Response({'detalis': 'ok', 'pk': product.pk},status=HTTP_201_CREATED)

