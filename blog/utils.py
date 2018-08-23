import math


def custom_paginator(current_page, num_pages, max_page):

    middle = math.ceil(max_page / 2)
    # 先考虑特殊情况
    if num_pages <= max_page:
        start = 1
        end = num_pages
    elif current_page <= middle:
        start = 1
        end = max_page
    elif middle < current_page < num_pages - middle + 1:
        start = current_page - middle
        end = current_page + middle -1
    else:
        start = num_pages - max_page + 1
        end = num_pages
    return start, end