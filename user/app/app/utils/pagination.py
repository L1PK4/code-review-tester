import logging

from paginate_sqlalchemy import SqlalchemyOrmPage

from app.schemas.response import Paginator


def get_page(query, page: int | None = None, size: int = 30) -> tuple[list, Paginator | None]:
    if page is None:
        if size is None:
            return query.all(), None
        else:
            return query.limit(size).all(), None

    if size is None:
        size = 30

    page_obj = SqlalchemyOrmPage(query, page=page, items_per_page=size)

    total = page_obj.page_count

    paginator = Paginator(
        page=page,
        total=total,
        has_prev=page > 1,
        has_next=page < total
    )
    return page_obj.items, paginator
