def estimate_revenue(price, bsr):

    try:
        price = int(str(price).replace(",", ""))
    except:
        price = 0

    if not bsr:
        return 100, price * 100, 5000

    if bsr < 100:
        sales = 10000
    elif bsr < 500:
        sales = 3000
    elif bsr < 1000:
        sales = 1500
    else:
        sales = 500

    return sales, sales * price, bsr
