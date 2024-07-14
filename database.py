from base import base_beg, base_end_adv, request_get

def database_get(type_, params):
    result_url = f'{base_beg}/database.get{type_}?{params}&count=1000&{base_end_adv}'
    result = request_get(result_url)['response']['items']
    return [(res['id'], res['title']) for res in result]
