from django.core.paginator import Paginator


def pageProcess(queryset, serializer_class, cur_page, perPage):

    perPageNum = perPage #페이지당 여행지 수
    paginator = Paginator(queryset, perPageNum)
    total_count = paginator.count
    curPage_queryset = paginator.get_page(cur_page)
    start_page = 1
    end_page = paginator.num_pages
    prev_bool = curPage_queryset.has_previous()
    next_bool = curPage_queryset.has_next()

    serialized_queryset = serializer_class(curPage_queryset, many=True)

    page = {"curPage": cur_page, "perPageNum": perPageNum, "totalCount": total_count, "startPage": start_page, "endPage": end_page, "prev_bool": prev_bool, "next_bool":next_bool}
    return {"page": page, "result":serialized_queryset.data }