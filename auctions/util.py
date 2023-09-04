from django.db.models import Max, Count
from .models import AuctionList

def getCurrentPrice(product):
    allCurrentBids = product.bids.all()
    if allCurrentBids:
        #highestBid = allCurrentBids.aggregate(Max('bidPrice'))['bidPrice__max']
        highestBid = allCurrentBids.order_by("-bidPrice")[0].bidPrice
        return highestBid
    return product.initialPrice


def getCategoriesWithCount():
    # Get all unique categories and annotate them with the count of items per category
    categories_with_counts = AuctionList.objects.values('category').annotate(category_count=Count('category'))

    # Create a list of all possible categories with a count of 0 for those that don't exist in the database
    all_categories = AuctionList.CATEGORY_CHOICES
    all_categories_with_counts = [{'category': category[0], 'category_count': 0} for category in all_categories]

    # Merge the two lists to include categories with 0 items
    merged_categories = {category['category']: category for category in all_categories_with_counts}
    for category in categories_with_counts:
        merged_categories[category['category']] = category

    # Sort the merged categories alphabetically
    sorted_categories = sorted(merged_categories.values(), key=lambda x: x['category'])
    return sorted_categories