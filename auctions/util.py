def getCurrentPrice(product):

    allCurrentBids = product.bids.all()


    if allCurrentBids:
        #highestBid = allCurrentBids.aggregate(Max('bidPrice'))['bidPrice__max']
        highestBid = allCurrentBids.order_by("-bidPrice")[0].bidPrice
        return highestBid
    return product.initialPrice

