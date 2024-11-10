import math
from uuid import UUID
from django.core.paginator import Paginator

PAGINATION_LIMIT = 10
MAX_PAGE_BUTTONS = 5
DEFAULT_PAGE = 1

def check_is_valid_page_query_param(page_number, num_pages):
    if page_number == None:
        return False
    try:
        number = int(page_number)
        return number > 0 and number <= num_pages
    except ValueError:
        return False

def paginate(requested_page_number, post_list):
    paginator = Paginator(post_list, PAGINATION_LIMIT)
    num_pages = paginator.num_pages
    is_valid_page = check_is_valid_page_query_param(requested_page_number, num_pages)

    if (requested_page_number and not is_valid_page) or requested_page_number == "":
        # Query param cannot be parsed to an int
        return {"page_error": True}

    else:
        page_number = (
            DEFAULT_PAGE
            if requested_page_number == None
            else int(requested_page_number)
        )
        page = paginator.page(page_number)
        paginated_posts = page.object_list
        central_page_button_index = math.floor(MAX_PAGE_BUTTONS / 2)
        is_last_window = page_number > (num_pages - ((MAX_PAGE_BUTTONS / 2) - 1))
        first_page_button = (
            max(((num_pages - MAX_PAGE_BUTTONS) + 1), 1)
            if is_last_window
            else max(page_number - central_page_button_index, 1)
        )
        last_page_button = min(first_page_button + (MAX_PAGE_BUTTONS - 1), num_pages)
        page_buttons = range(first_page_button, last_page_button + 1) if num_pages > 1 else None

        pagination = {
            "is_first_page": page_number == 1,
            "is_last_page": page_number == num_pages,
            "page_buttons": page_buttons,
            "page_number": page_number,
            "previous_page": page_number - 1,
            "next_page": page_number + 1,
        }

        return {"paginated_posts": paginated_posts, "pagination": pagination}

def check_is_valid_uuid(uuid_string):
    try:
        # Attempt to create a UUID object; will raise ValueError if invalid
        UUID(uuid_string, version=4)
        return True
    except ValueError:
        return False
