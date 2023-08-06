import urllib.parse as urlparse


def get_url_params(url):
    """
    获取url的params参数，返回dict形式
    """
    params_str = urlparse.urlsplit(url).query
    params_str_split = params_str.split('&')
    params_dict = dict()
    for each in params_str_split:
        each_split = each.split('=', maxsplit=1)
        params_dict[each_split[0]] = each_split[1]
    return params_dict
