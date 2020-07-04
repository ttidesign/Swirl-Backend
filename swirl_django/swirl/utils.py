import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart ={}

    # print('Cart',cart)
    items =[]
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            item = Item.objects.get(id=i)
            total = (item.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            product = {
                'item':{
                    'id':item.id,
                    'title' : item.title,
                    'price': item.price,
                    'preview_url': item.preview_url,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(product)
        except:
            pass
    return{'cartItems':cartItems, 'order':order,'items':items}

def favoriteList(request):
    try:
        favorite = json.loads(request.COOKIES['favorite'])
    except:
        favorite ={}

    # print('Cart',cart)
    items =[]
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']

    for i in favorite:
        try:
            cartItems += favorite[i]['quantity']
            item = Item.objects.get(id=i)
            total = (item.price * favorite[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += favorite[i]['quantity']

            product = {
                'item':{
                    'id':item.id,
                    'title' : item.title,
                    'price': item.price,
                    'preview_url': item.preview_url,
                },
                'quantity': favorite[i]['quantity'],
                'get_total': total
            }
            items.append(product)
        except:
            pass
    return{'cartItems':cartItems, 'order':order,'items':items}
