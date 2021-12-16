from django.urls import path
from django.views.generic import TemplateView

from product.views.product import CreateProductView,ProductList, UpdateProductView, uploadProductImage
from product.views.variant import VariantView, VariantCreateView, VariantEditView

from product.views.api.views import getProduct,createNewProduct,updateProduct
app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),
    # api call  
    path('api/get/<int:pk>/',getProduct,name='api.get.product'),
    path('api/create/', createNewProduct, name='api.create.product'),
    path('api/update/<int:pk>/', updateProduct, name='api.update.product'),
    # Products URLs
    path('uploadimages/', uploadProductImage, name='image.upload.product'),
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('update/view/<int:pk>/', UpdateProductView.as_view(), name='update.product'),
    path('list/', ProductList.as_view(), name='list.product'),
]
