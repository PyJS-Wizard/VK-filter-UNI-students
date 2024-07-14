import subprocess, os

def install_requirements():
    try:
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

        old_filename = os.path.basename(__file__)
        if old_filename != 'setup_completed.py':
            os.rename(old_filename, 'setup_completed.py')

        print('\nВсё успешно установлено!')
        input()
    except subprocess.CalledProcessError as e:
        print(f'Произошла ошибка при установке зависимостей: {e}')
    except Exception as e:
        print(f'Произошла непредвиденная ошибка: {e}')

if __name__ == '__main__':
    install_requirements()
