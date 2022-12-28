from math import ceil


def make_pagination_range(
    page_range,
    qty_pages,
    current_page,
):
    middle_range = ceil(qty_pages / 2)
    # Range começa/para a partir da página atual -+ meiuca da página
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)

    # Range que for negativo retornará num absoluto/inteiro
    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range -= abs(total_pages - stop_range)

    # fatiamento do range de 0 até 4
    # Para facilitar no template, faremos dicionário
    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }
