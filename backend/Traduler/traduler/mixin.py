from django.core.paginator import Paginator


def pageProcess(queryset, serializer_class, cur_page, perPage, user=None):

    perPageNum = perPage #페이지당 여행지 수
    paginator = Paginator(queryset, perPageNum)
    total_count = paginator.count
    curPage_queryset = paginator.get_page(cur_page)
    start_page = 1
    end_page = paginator.num_pages
    prev_bool = curPage_queryset.has_previous()
    next_bool = curPage_queryset.has_next()

    # 기존에 넘겨주던 데이터는 data= 키워드로, 추가적인 정보는 context=로 넘겨줍니다(유저 정보)
    # Serializer 내부에서 user에 접근하는 CurrentUserDefault라는게 있다는데 너무 예전 답변이고, 더이상 작동하지 않는다는 이야기도 있어서 context로 넘겨주었습니다.
    serialized_queryset = serializer_class(data=curPage_queryset, context={'user': user}, many=True)
    page = {
        "curPage": cur_page, 
        "perPageNum": perPageNum, 
        "totalCount": total_count, 
        "startPage": start_page, 
        "endPage": end_page, 
        "prev_bool": prev_bool, 
        "next_bool":next_bool}

    # data를 data=키워드로 넘겨준 경우, 유효성 검사를 해야합니다.
    serialized_queryset.is_valid()

    return page, serialized_queryset.data