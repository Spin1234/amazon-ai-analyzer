import re

def get_bsr_number(bsr_text):
    if not bsr_text:
        return 5000

    match = re.search(r'#([\d,]+)', bsr_text)
    if match:
        return int(match.group(1).replace(",", ""))

    return 5000


def estimate_sales(bsr):
    if bsr < 100: return 10000
    elif bsr < 500: return 3000
    elif bsr < 1000: return 1500
    elif bsr < 5000: return 500
    else: return 100


def estimate_revenue(price, bsr_text):
    try:
        price = int(price.replace(",", ""))
    except:
        price = 0

    bsr = get_bsr_number(bsr_text)
    sales = estimate_sales(bsr)
    revenue = sales * price

    return sales, revenue, bsr