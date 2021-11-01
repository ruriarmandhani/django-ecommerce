from .models import Category, OrderItem


def parent_categories(request):
    categories = Category.objects.filter(parent=None)
    return {'categories': categories}


def count_cart_items(request):
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(
            user=request.user, ordered=False)
        count_items = sum([item.quantity for item in order_items])
        return {'total_item_in_cart': count_items}
    else:
        return {'total_item_in_cart': 0}
