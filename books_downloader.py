from bs4 import BeautifulSoup
from random import randint
from requests_tor import RequestsTor
import os


# If you use the Tor browser
# rt = RequestsTor()
# OR й                                                          для подключения к тор (это необходимо) нужно скачать тор браузер
# # If you use the Tor
# rt = RequestsTor(tor_ports=(9050,), tor_cport=9051)

url = 'http://flibustaongezhld6dibs2dps6vm4nvqg2kp7vgowbu76tzopgnhazqd.onion/booksearch?ask='
url2 = 'http://flibustaongezhld6dibs2dps6vm4nvqg2kp7vgowbu76tzopgnhazqd.onion'                  #ссылки для поиска
lst = []
lst_fb2 = []
lst_epub = []
repp = 0
flag = 0
flag_n = 0
form = 0
sb = 0                  # Куча переменных, не помню зачем они, но не мешают и ладно)
sn = ''
ful = ''
i = 0
count = 0
lst_ppp = []
lst_name = []
lst_ath = []
folder = '' # Сюда вставить путь к папке, в которую будут скачиваться книги 


def search(s, lst_fb2, lst_epub, lst_name, lst_ath, lst_ppp):           # Ищем ссылки на книги по названию
    lst_y = []
    rt = RequestsTor()
    response = rt.get(url + s)
    soup = BeautifulSoup(response.text, 'html.parser')              # Получаем код страницы
                
    for link in soup.find_all('li'):                                # Тут мы ищем ссылки на книги со страницы (знаю, ничего непонятно, но оно работает)
        if '/a/' in str(link) and '/b/' in str(link):
            s = str(link).split('<a href="/a/')
            if s[1] not in lst_ppp: 
                g = s[0].split('<a href="')
                u = g[1].split('">')
                lst_y.append(u[0])
                print(f'sfdfdsfdfs{s[1]}')
                lst_ppp.append(s[1])
             
    l = lst_y[:5]               # Программа будет качать только первые 5 книг со страницы
    lst_ppp = []
    return books_links(l, lst_fb2, lst_epub, lst_name, lst_ath)         # возвращаем функцию, которая будет находить название книги и автора
    
    
def books_links(l, lst_fb2, lst_epub, lst_name, lst_ath):           # Тут мы ищем названия
    rt = RequestsTor()
    
    for el in l:                        # Проходимся по списку книг
        response = rt.get(url2 + el)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a'):             # Ищем ссылки для книг соответствующего формата
            u = link.get('href')
            
            if u.startswith('/b/') and u.endswith('fb2'):
                lst_fb2.append(url2 + u) 
                
            elif u.startswith('/b/') and u.endswith('epub'):
                lst_epub.append(url2 + u) 
                    
        for link in soup.find_all('h1'):            # Тут ищем название книги
            
            if 'fb2' in str(soup):
                
                if 'class' in str(link):
                    w = str(link).replace('>', '%')
                    e = w.replace('<', '%')
                    y = e.split('%')
                    r = y[2].split('(')
                    name = r[0]
                    
                    if '/' in name:
                        o = name.split('/')
                        lst_name.append(o[0])

                    elif '\\' in name:
                        o = name.split('\\')
                        lst_name.append(o[0])
                    
                    elif '"' in name:
                        o = name.split('"')
                        lst_name.append(o[1])

                    else:
                        lst_name.append(name[:-1])
            
        for link in soup.find_all('a'):         # Тут ищем автора
            
            if 'fb2' in str(soup):
                
                if 'title' not in str(link) and '/a/' in str(link) and 'all' not in str(link):
                    w = str(link).replace('>', '%')
                    e = w.replace('<', '%')
                    r = e.split('%')
                    name = r[2]
                    n = name.split()
                    print(n)
                    lst_ath.append(n[-1])
                    
                    break
                
    return lst_fb2, lst_epub, lst_name, lst_ath         # Возвращаем списки, которые используются в функциях fb2 и epub


def search2(s, lst_fb2, lst_epub, lst_name, lst_ath, lst_ppp, a):
    lst_y = []
    rt = RequestsTor()
    response = rt.get(url + s)
    soup = BeautifulSoup(response.text, 'html.parser')
                
    for link in soup.find_all('li'):                    # То же самое, что и в search только книги отбираются и по фамилии автора
        
        if '/a/' in str(link) and '/b/' in str(link):
            s = str(link).split('<a href="/a/')
            fau = s[1].split('>')
            fau_2 = fau[1].split('<')
            n = fau_2[0].split()[-1]
            
            if str(a).lower() in str(n).lower(): 
                g = s[0].split('<a href="')
                u = g[1].split('">')
                lst_y.append(u[0])
                lst_ppp.append(s[1])
            
    l = lst_y[:5]
    lst_ppp = []
    
    return books_links2(l, lst_fb2, lst_epub, lst_name, lst_ath)            # Передаются для поиска названия и автора
    
    
def books_links2(l, lst_fb2, lst_epub, lst_name, lst_ath):
    rt = RequestsTor()
    
    for el in l:                                            
        response = rt.get(url2 + el)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a'):             # Ссылки для скачивания
            u = link.get('href')
            
            if u.startswith('/b/') and u.endswith('fb2'):
                lst_fb2.append(url2 + u) 
                
            elif u.startswith('/b/') and u.endswith('epub'):
                lst_epub.append(url2 + u) 
                    
        for link in soup.find_all('h1'):        # Ищет название
            
            if 'fb2' in str(soup):
                
                if 'class' in str(link):
                    w = str(link).replace('>', '%')
                    e = w.replace('<', '%')
                    y = e.split('%')
                    r = y[2].split('(')
                    name = r[0]
                    
                    if '/' in name:
                        o = name.split('/')
                        lst_name.append(o[0])

                    elif '\\' in name:
                        o = name.split('\\')
                        lst_name.append(o[0])
                        
                    elif '"' in name:
                        o = name.split('"')
                        lst_name.append(o[1])
                        
                    elif '[' in name:
                        o = name.split('[')
                        if o[0] != '' and o[0] != '':
                            lst_name.append(o[0])
                        if o[1] != '' and o[1] != '':
                            lst_name.append(o[1])
                        if o[2] != '' and o[2] != '':
                            lst_name.append(o[2])

                    else:
                        lst_name.append(name[:-1])
            
        for link in soup.find_all('a'):         # ищет автора (не уверен, что оно надо)
            
            if 'fb2' in str(soup):
                
                if 'title' not in str(link) and '/a/' in str(link) and 'all' not in str(link):
                    w = str(link).replace('>', '%')
                    e = w.replace('<', '%')
                    r = e.split('%')
                    name = r[2]
                    n = name.split()
                    lst_ath.append(n[-1])
                    
                    break
                
    return lst_fb2, lst_epub, lst_name, lst_ath         # Передаётся в функцию fb22 или epub2




def fb2(snn, rt): # Поиск по названию в фб2
    
    global ful
    global flag_n
    global i
    global flag
    global sn
    sn = ''
    lst_fb2 = []                # Куча переменных, можно не трогать
    lst_epub = []
    lst_name = []
    lst_ath = []
    lst_ppp = []
    count = 0
    c = randint(0, 9000000)
    
    full_path = os.path.join(folder, f'papka_{c}')          # Создаётся папка для книг с рандомным названием, можно удалить (изначально создавалось для бота, чтобы книги разных пользователей не смешивались, но для личного пользования это не требуется, наверно)
    if not os.path.exists(full_path):                       # Проверяет наличие папки с таким названием
        os.makedirs(full_path)
        print("\nПапка успешно создана")               
    else:                                                   # Если нашло папку с таким названием, то поменяет название 
        full_path = os.path.join(folder, f'papka_{c + 16}')
        os.makedirs(full_path)

    for link in list(search(snn, lst_fb2, lst_epub, lst_name, lst_ath, lst_ppp))[0]:        # Тут запускаем функцию, которая и будет искать книги
        filename = lst_name[count]
        ath = lst_ath[count]                # Функция отдаёт списки, по которым программа проходится
        response = rt.get(link)

        filepath = os.path.join(full_path, f'{ath}_{filename}.fb2')
        
        try:                                                        # Качаем книги по спискам
            os.path.isfile(f'{full_path}/{ath}_{filename}.fb2')
            with open(filepath, 'wb') as file:
                file.write(response.content)
            count += 1        
            print(f"\nФайл '{ath}_{filename}.fb2' успешно скачан.") 
        except FileNotFoundError:

            count += 1        
            print(f"\nФайл '{ath}_{filename}.fb2' не скачан.") 
        
    flag_n = 0
    flag = 0
    lst_fb2 = []
    ful = ''
    lst_epub = []
    lst_name = []                   # Обнуляем переменные на всякий случай
    lst_ath = []
    i = 0
    lst_ppp = []
    count = 0                       # Конец программы

    
def epub(snn, rt):          # То же, что и в прошлой функции, но для епаб
    global ful
    global flag_n
    global i
    global sn
    sn = ''
    lst_fb2 = []
    lst_epub = []
    lst_name = []
    lst_ath = []
    lst_ppp = []
    count = 0
    
    c = randint(0, 9000000)
    full_path = os.path.join(folder, f'papka_{c}')
    if not os.path.exists(full_path):
        # Создаем папку
        os.makedirs(full_path)
        print("\nПапка успешно создана")
    else:
        full_path = os.path.join(folder, f'papka_{c + 16}')
        os.makedirs(full_path)

    for link in list(search(snn, lst_fb2, lst_epub, lst_name, lst_ath, lst_ppp))[0]:
        filename = lst_name[count]
        ath = lst_ath[count]
        response = rt.get(link)

        # Путь к сохранению файла
        filepath = os.path.join(full_path, f'{ath}_{filename}.epub')
        try:
        # Сохраняем файл в указанную папку
            os.path.isfile(f'{full_path}/{ath}_{filename}.epub')
            with open(filepath, 'wb') as file:
                file.write(response.content)
            count += 1        
            print(f"\nФайл '{ath}_{filename}.epub' успешно скачан.") 
        except FileNotFoundError:

            count += 1        
            print(f"\nФайл '{ath}_{filename}.epub' не скачан.") 
                
    flag_n = 0
    lst_fb2 = []
    ful = ''
    lst_epub = []
    lst_name = []
    lst_ath = []
    i = 0
    lst_ppp = []
    count = 0

    
def fb22(snn, rt, aa):              # то же самое, что и в позапрошлой функции, но и по автору
    global ful
    global flag_n
    global flag
    global i
    global sn
    global a
    sn = ''                    
    a = ''
    lst_fb2 = []
    lst_epub = []
    lst_name = []
    lst_ath = []
    lst_ppp = []
    
    count = 0
    c = randint(0, 9000000)
    full_path = os.path.join(folder, f'papka_{c}')   
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print("\nПапка успешно создана")
    else:
        full_path = os.path.join(folder, f'papka_{c + 16}')
        os.makedirs(full_path)

    for link in list(search2(snn, lst_fb2, lst_epub, lst_name, lst_ath, lst_ppp, aa))[0]: # Здесь мы передаём переменные поисковику, как в прошлый раз + автора
        filename = lst_name[count]
        ath = lst_ath[count]
        response = rt.get(link)

        filepath = os.path.join(full_path, f'{ath}_{filename}.fb2')
        try:
            os.path.isfile(f'{full_path}/{ath}_{filename}.fb2')
            with open(filepath, 'wb') as file:
                file.write(response.content)
            count += 1        
            print(f"\nФайл '{ath}_{filename}.fb2' успешно скачан.") 
        except FileNotFoundError:

            count += 1        
            print(f"\nФайл '{ath}_{filename}.fb2' не скачан.") 

    flag_n = 0
    flag = 0
    lst_fb2 = []
    ful = ''
    lst_epub = []
    lst_name = []
    lst_ath = []
    lst_ppp = []
    i = 0
    count = 0
    
    
def epub2(snn, rt, aa):             # То же самое, что в прошлой функции, но для епаб
    global ful
    global flag_n
    global flag
    global i
    global sn
    global a
    sn = ''
    a = ''
    lst_fb2 = []
    lst = []
    lst_epub = []
    lst_name = []
    lst_ath = []
    lst_ppp = []
    
    count = 0
    c = randint(0, 9000000)
    full_path = os.path.join(folder, f'papka_{c}')
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print("\nПапка успешно создана")
    else:
        full_path = os.path.join(folder, f'papka_{c + 16}')
        os.makedirs(full_path)

    for link in list(search2(snn, lst_fb2, lst_epub, lst_name, lst_ath, lst_ppp, aa))[0]:
        filename = lst_name[count]
        ath = lst_ath[count]
        response = rt.get(link)

        filepath = os.path.join(full_path, f'{ath}_{filename}.epub')
        try:
            os.path.isfile(f'{full_path}/{ath}_{filename}.epub')
            with open(filepath, 'wb') as file:
                file.write(response.content)
            count += 1        
            print(f"\nФайл '{ath}_{filename}.epub' успешно скачан.") 
        except FileNotFoundError:

            count += 1        
            print(f"\nФайл '{ath}_{filename}.epub' не скачан.") 

    flag_n = 0
    flag = 0
    lst_fb2 = []
    lst = []
    ful = ''
    lst_epub = []
    lst_name = []
    lst_ath = []
    lst_ppp = []
    count = 0
    i = 0

    
rt = RequestsTor()      # Подключаемся

search_type = int(input('Выберите тип поиска:\n1 - по названию книги\n2 - по названию и автору\nОтвет: '))      # Выбираем тип поиска, можно сделать проверку на ввод верного числа 
book_format = int(input('Выберите формат книги:\n1 - fb2\n2 - epub\nОтвет: '))                                  # (то есть, вдруг пользователь введёт 3, и прога не заработает)
name = input('Введите название книги: ')            

if search_type == 1:        # Проверка типа поиска (название)
    
    if book_format == 1:            # Запускаем поиск по названию в фб2
        fb2(name, rt)
        
    elif book_format == 2:          # Запускаем поиск по названию в епаб
        epub(name, rt)
        
elif search_type == 2:      # Проверка типа поиска (название + автор)
    
    author = input('Введите фамилию автора: ')          
    
    if book_format == 1:               # Запускаем поиск по названию + автору в фб2
        fb22(name, rt, author) 
    
    elif book_format == 2:             # Запускаем поиск по названию + автору в епаб
        epub2(name, rt, author)

print('\n----------КОНЕЦ----------\n')