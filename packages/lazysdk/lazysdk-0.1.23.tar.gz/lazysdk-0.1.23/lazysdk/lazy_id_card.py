from . import lazytime


def id_info(
        id_str: str
):
    """
    在身份证号码中，第17位是性别位，用于表示持证人的性别。性别位的奇偶性规则如下：

    奇数表示男性（例如，1、3、5、7、9）
    偶数表示女性（例如，0、2、4、6、8）

通过身份证号码的性别位，我们可以快速判断持证人的性别。
    """
    if len(id_str) == 18:
        pass
    else:
        return {'err_msg': '只支持18位身份证号码'}
    ana_id_info = dict()
    ana_id_info['id_str'] = id_str

    year_now = lazytime.get_year()
    ana_id_info['year_now'] = year_now

    year = id_str[6:10]
    month = id_str[10:12]
    day = id_str[12:14]
    ana_id_info['year'] = year
    ana_id_info['month'] = month
    ana_id_info['day'] = day

    age = year_now - eval(year)
    ana_id_info['age'] = age

    gender_num = id_str[16]
    s = eval(gender_num)
    if s % 2 == 0:
        gender_str = "女"
    else:
        gender_str = "男"
    ana_id_info['gender_num'] = gender_num
    ana_id_info['gender_str'] = gender_str
    return ana_id_info
