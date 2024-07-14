from base import base_beg, base_end_adv, clear_console, get_input_int_in_range, request_get
from database import database_get

def user_search_uni(unis: list[tuple[int, str]], university_year: int, include_all: bool):
    clear_console()
    
    print('\n'.join(f'{i}) {uni[1]}' for i, uni in enumerate(unis, start=1)))
    get_index_exact_uni = get_input_int_in_range(f'Введите номер нужного вуза: ', 1, len(unis))

    clear_console()

    exact_uni_id, exact_uni_title = unis[get_index_exact_uni - 1]
    faculties = database_get('Faculties', f'university_id={exact_uni_id}')
    if not faculties:
        return 'Факультеты не найдены.'
    
    print('\n'.join(f'{i}) {faculty[1]}' for i, faculty in enumerate(faculties, start=1)))
    
    get_index_exact_faculty = get_input_int_in_range(f'Введите номер нужного факультета: ', 1, len(faculties))
    
    clear_console()
    
    exact_faculty_id, exact_faculty_title = faculties[get_index_exact_faculty - 1]
    chairs = database_get('Chairs', f'faculty_id={exact_faculty_id}')

    if not chairs:
        return 'Кафедры не найдены.'
    
    print('\n'.join(f'{i}) {chair[1]}' for i, chair in enumerate(chairs, start=1)))
    get_index_exact_chair = get_input_int_in_range(f'Введите номер нужной кафедры (0 - любая кафедра): ', 0, len(chairs))
    
    clear_console()

    print('Подождите, идет сбор данных...')
    
    exact_chair_id, exact_chair_title = chairs[get_index_exact_chair - 1]
    result_url = f'{base_beg}/users.search?university={exact_uni_id}&university_faculty={exact_faculty_id}&university_year={university_year}' + \
                f'&count=1000&fields=universities,can_write_private_message&{base_end_adv}'
    
    if get_index_exact_chair: 
        result_url += f'&university_chair={exact_chair_id}'
    else:
        exact_chair_title = 'любая'

    response, result_ids = request_get(result_url)['response']['items'], []

    for res in response:
        cur_id, cur_unis, can_write_priv = res['id'], res['universities'], res['can_write_private_message']
        if (can_write_priv or include_all) and \
            any((uni.get('faculty', '') == exact_faculty_id) and \
              ((not get_index_exact_chair) or (uni.get('chair', '') == exact_chair_id)) \
                and (uni.get('graduation', 0) == university_year) for uni in cur_unis):
            
            result_ids.append(cur_id)

    clear_console()
    
    if not result_ids:
        return 'Студенты не найдены.'
    
    return result_ids, exact_uni_title, exact_faculty_title, exact_chair_title
