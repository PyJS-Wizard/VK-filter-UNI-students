# Поиск студентов ВУЗов в ВК
Данный проект, написанный на Python, позволяет отфильтровать пользователей социальной сети **ВКонтакте** по ВУЗу, факультету и кафедре (последнее может быть как конкретной кафедрой, так и любой). 

Программа работает на основе отправки запросов к официальному VK API, документация: https://dev.vk.com/ru/reference.

## Перед использованием
Перед тем, как приступить к использованию, нужно удостовериться, что у вас скачан **Python** (желательно недавней версии). Это можно проверить, написав в командной строке / терминале (в Windows: Win + R -> cmd):

`python --version`

Если всё ок, то выводится что-то вроде:
`Python 3.12.4` (формат: Python <версия>)

Если у вас не скачан python или скачан, но старой версии / неправильно, то удалите его, если он у вас установлен  (в Windows: в поисковой строке напишите "Установка и удаление программ" -> напишите "Python" и удалите его, а также Python Launcher, если таковой появляется при поиске) и затем зайдите на [официальный сайт](https://www.python.org/downloads/) и скачайте последнюю версию.

**Примечание: при установке Python, пожалуйста, поставьте галочку в поле "Add python.exe to PATH". Это важно для корректной работы программы.**

Далее: перед первым использованием запустите файл `setup.py` (если система спрашивает, какую программу использовать для открытия, выберите Python, причем выберите использование "всегда", ведь так будет удобнее для дальнейшего использования программы). Это установит пару библиотек, нужных для работы основной программы. После успешного выполнения скрипта файл переименуется на `setup_completed.py`.
При дальнейшем использовании основной программы вам не нужно будет делать этот шаг повторно, можете в принципе забыть про этот файл.

Всё, основная подготовка окончена.

## Использование
Чтобы использовать программу с функционалом по умолчанию, запустите главный файл `main.py` и следуйте инструкциям программы: вас попросят ввести название ВУЗа, затем, если будут найдены ВУЗы, попросят ввести год окончания обучения студентов. Последнее нужно вам, чтобы уточнить на каком курсе они, либо в каком году окончили ВУЗ. 

Дальше нужно будет выбрать конкретный ВУЗ из предложенного пронумерованного списка  (введите число, соответствующее нужному названию). Здесь следует заметить, что некоторые названия могут показаться неофициальными, как если бы какой-то хулиган зарегистрировал фальшивые ВУЗы с юмористически подтекстом (название самого ВУЗа, факультетов, кафедр и т. д.). Общая рекомендация: идти сверху-вниз по списку, пока не найдете самое подходящее название (если в первый раз нашли что-то подходящее, пройдите всё же до конца списка, вдруг найдете еще более подходящее / полное название).

Дальше выпадет тот же пронумерованный список с факультетами выбранного ВУЗа, выберите номер нужного факультета.

И, наконец, выпадет список с кафедрами выбранного факультета: введите номер нужной кафедры **или введите 0, если хотите выбрать любую кафедру.**

Дальше подождите несколько секунд, и программа выдаст список идентификаторов найденных пользователей. Программа спросит, сколько из этого списка вы хотите отобрать для результата (например, если слишком много результатов и вы хотите поменьше, просто напишите сколько оставить). В таком случае программа в случайном порядке отеберет введенное количество. Или вы можете **ввести 0, что оставит всех пользователей (итоговый список останется целым).**

Далее финальная операция: ссылки на профили отобранных (или всех) пользователи будут записаны в файл `result_user_ids.txt` (в текущей директории) с указанием времени момента операции и параметров поиска: ВУЗа, факультета и кафедры.

Группы результатов, записанных в этом файле, записываются в следующем формате:
```
-->#######################  
[дд.мм.гг, чч:мм:сс]
Университет: <название ВУЗа>
Факультет: <название факультета>
Кафедра: <название кафедры или "любая">
Ссылки на профили (кол-во: <количество итоговых профилей>)

https://vk.com/id<идентификатор первого пользователя>
https://vk.com/id<идентификатор второго пользователя>
...
https://vk.com/id<идентификатор последнего пользователя>

<--#######################
```


## Флаги программы
В папке проекта имеется json-файл `config_flags.json`, в котором содержится словарь с двумя парами ключ-значение: 

```
{
    "include_all": false,
    "write_file": false 
}
```

Оба ключа по умолчанию имеют значение false.

Первый ключ `include_all` отвечает за следующее. Если `include_all` соответствует `true`, то программа будет искать **всех пользователей, независимо от того, открытая у них личка или закрытая.** Поэтому для удобства `include_all` соответствует `false` по умолчанию, то есть отбираются только те, кто имеет открытую личку.

Второй ключ `write_file`. отвечает за следующее. Если `write_file` соответствует `false` (по умолчанию), то после очередного выполнения программы **полученные данные записываются в файл `result_user_ids.txt` <u>в конец</u>, не стирая то, что было уже заполнено (если было).** Это подходит в случае, если вам важно сохранять результаты предыдущих поисков программы в одном файле.

В противном случае (`write_file` соответствует `true`) программа будет стирать все данные в файле `result_user_ids.txt` (если он не пустой) и записывать новые данные "с чистого листа". Это нужно в случае, если для вас излишне нагромождать данные в одном файле (тогда убедитесь, что если вам нужны полученные раннее данные, то вы их сохраните в другое место).

## Дальнейшее пользование
Чтобы продолжать использовать программу, просто запускайте главный файл `main.py` и следуйте инструкциям в консоли

Другие файлы в папке не трогайте, кроме, разве что, файла `config_flags.json`, в котором вы можете изменять значения флагов, как вам будет нужно. Не забывайте сохранять внесенные изменения в этом файле (в Windows: Ctrl + S).