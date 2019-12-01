from django.urls import path, include

from .views import *
from django.views.generic import TemplateView

app_name = 'menu'

urlpatterns = [
    path('', TemplateView.as_view(template_name='menu/main/index.html'), name='index'),
    path('single/', TemplateView.as_view(template_name='menu/main/single.html'), name='single'),
    path('order1/', Order1, name='order'),
    path('order2/', Order2, name='order2'),
    path('order_detail/<int:pk>',order_detail,name='order_detail'),
    path('order_detail2/<int:pk>', order_detail2, name='order_detail2'),
    path('order_more_detail/<int:pk>',TemplateView.as_view(template_name='menu/order/order_more_detail.html')),
    #path('order/orderDetail/<str:store_name>/<str:menu_name>', OrderDetail.as_view(), name='order_detail'),
   # path('orderList/', OrderList.as_view(), name='order_list'),
    #path('orderList/<int:orderList_id>', OrderListDetail.as_view(), name='order_list_detail'),

]
