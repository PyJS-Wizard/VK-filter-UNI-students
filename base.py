from dotenv import load_dotenv
from random import uniform
import os, requests, time

class ErrorCodeException(Exception):
    pass

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def get_input_int_in_range(prompt: str, start: int, end: int) -> int:
    while True:
        try_prompt = input(prompt)
        if try_prompt.isdigit() and (start <= (result := int(try_prompt)) <= end):
            return result

def request_get(url) -> dict:
    delay, finished = 1, False
    while True:
        try:
            r = requests.get(url)
            result = r.json()
            if 'error' in result:
                raise ErrorCodeException
            finished = True
            break
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения. Повторная попытка...')
        except requests.exceptions.Timeout:
            print('Ошибка тайм-аута. Повторная попытка...')    
        except requests.exceptions.TooManyRedirects:
            print('Ошибка: слишком много перенаправлений. Повторная попытка...')   
        except requests.exceptions.HTTPError:
            print('Ошибка HTTP. Повторная попытка...')   
        except requests.exceptions.RequestException:
            print('Ошибка requests. Повторная попытка...')   
        except ErrorCodeException:
            error_code = result['error']['error_code']
            if error_code in (1, 10, 29):
                print('Произошла непредвиденная ошибка на сервере. Попробуйте повторить запрос позже.')
                quit() 
        except Exception as e:
            print(f'Произошла сторонняя ошибка: {e}.\nПовторная попытка...')
        finally:
            if finished:
                break

            time.sleep(delay)

            delay = delay * 2 + uniform(0, 1)

            if delay > max_request_delay:
                print(f'Запрос выполнялся слишком долго. Попробуйте повторить запрос позже.')
                quit()
            

    return result


load_dotenv()

access_token_adv = os.getenv('user_token_advanced')
base_beg = 'https://api.vk.com/method'
base_end_adv = f'access_token={access_token_adv}&v=5.124'

max_request_delay = 30
