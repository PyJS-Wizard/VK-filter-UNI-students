from user import user_search_uni
from base import get_input_int_in_range, clear_console
from database import database_get
from random import shuffle
from time import strftime
import json

def write_result_user_ids(result_ids, uni, faculty, chair, writing_mode):
    formatted_user_ids = '\n'.join(f'https://vk.com/id{user_id}' for user_id in result_ids)
    cur_time_formatted = strftime('%d.%m.%Y, %H:%M:%S')

    with open('result_user_ids.txt', writing_mode, encoding='utf-8') as file:
        file.write('-->#######################\n')
        file.write(f'[{cur_time_formatted}]\n')
        file.write(f'Университет: {uni}\n')
        file.write(f'Факультет: {faculty}\n')
        file.write(f'Кафедра: {chair}\n')
        file.write(f'Ссылки на профили (кол-во: {len(result_ids)}):\n\n')
        file.write(formatted_user_ids + '\n\n')
        file.write('<--#######################\n\n\n')

    clear_console()
    print('*\nСписок идентификаторов студентов добавлен в файл "result_user_ids.txt".\n*')
    input()
    return

    
def main(): 

    try:
        with open('config_flags.json') as file:
            config_flags = json.loads(file.read())
            include_all = config_flags.get('include_all', False)
            write_file = config_flags.get('write_file', False)
    except json.decoder.JSONDecodeError:
        include_all = write_file = False
        
    clear_console()
    
    university = input('Введите название университета: ')
    while not (unis := database_get('Universities', f'q={university}')):
        university = input('Результаты не найдены. Еще раз введите название университета: ')

    university_year = get_input_int_in_range('Введите год окончания обучения студентов: ', 1946, 2031)

    result_uni = user_search_uni(unis, university_year, include_all)
    
    if isinstance(result_uni, str):
        print(f'*\n{result_uni}\n*')
        input()
        return 
    
    result_ids, uni, faculty, chair = result_uni
    
    print(f'Вот список идентификаторов найденных студентов (кол-во: {len(result_ids)}):\n{result_ids}')
    remaining = get_input_int_in_range('\nСколько из них вы хотите оставить в конечном результате?\n'
                f'Программа в случайном порядке определит, кого оставить (0 - оставить всех): ', 0, len(result_ids))
    
    if remaining:
        shuffle(result_ids)
        result_ids = result_ids[:remaining]

    write_result_user_ids(result_ids, uni, faculty, chair, 'w' if write_file else 'a')


if __name__ == '__main__':
    main()
    