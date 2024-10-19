def check_is_valid_page_query_param(page_number, num_pages):
    if page_number == None:
        return False
    try:
        number = int(page_number)
        return number > 0 and number <= num_pages
    except ValueError:
        return False
