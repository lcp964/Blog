def get_page_data(pt,current_page,around_count=6):
    """
    分页对象  单前页   总页数,around_count显示页面数
    :return:
    """
    current_page_num = current_page.number  # 1
    # 获取总也码数
    total_page_num = pt.num_pages   # 1--100

    # 默认左右两边都没有页码
    left_more_page = False
    right_more_page = False

    # 计算左边的值
    left_start_index = current_page_num- around_count  # -3
    left_end_index = current_page_num
    if current_page_num <= around_count * 2 + 1:
        left_page_range = range(1,left_end_index)
    else:
        left_more_page = True
        left_page_range = range(left_start_index,left_end_index)

    # 搞右边  页码
    right_start_index = current_page_num + 1  # 2
    right_end_index = current_page_num + around_count + 1
    if current_page_num >= total_page_num - around_count * 2:
        right_page_range = range(right_start_index,total_page_num+1)
    else:
        right_more_page = True
        right_page_range = range(right_start_index,right_end_index)

    return {
        'current_page_num':current_page_num,

        # 页码总数
        'total_page_num':total_page_num,
        # 左标记
        'left_has_more_page':left_more_page,
        # 右标记
        'right_has_more_page':right_more_page,
        # 左范围
        'left_page_range':left_page_range,
        # 右范围
        'right_page_range':right_page_range
    }