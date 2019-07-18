import requests
import json
import time
import os
import random
from bs4 import BeautifulSoup
from collections import OrderedDict


def init_data():
    global info
    global name
    global lastnum
    global numbers
    print("read json")
    fi = open("lotto.json","r").read()
    data = json.loads(fi, object_pairs_hook=OrderedDict)
    info = data['info']
    name = info['name']
    lastnum = info['lastnum']
    numbers = data['number']
    number_counter()
    pass

def save_data():
    temp = {}
    fi = open("lotto.json","w")
    temp['info'] = info
    info['lastnum'] = lastnum
    temp['number'] = numbers
    json.dump(temp, fi)
    pass

def compare_number(list1, list2):
    cnt = 0
    for i in range(6):
        if list2[i] in list1 :
            cnt = cnt + 1        
        pass
    if cnt == 3 :
        return 5
    elif cnt == 4 :
        return 4
    elif cnt == 5 :
        if list2[6] in list1 :
            return 2
        else :
            return 3
    elif cnt == 6 :
        return 1
    else :
        return 0
    pass

def number_counter():
    global numbers
    global lastnum
    global count
    count = [0] * 46 
    for i in range(lastnum):
        temp = numbers[str(i+1)]
        for j in temp :
            count[int(j)] = count[int(j)] + 1
    pass

def print_counter():
    global numbers
    global lastnum
    global count

    for i in range(1, 46):
        print (str(i) + ' = ' + str(count[i] ) + ',   ' , end='' )
    print('')
    temp = 0
    for no in range(1, 46) :
        temp = temp + count[no]
    
    print('all  = ' + str( temp )  )
    tt =input("Enter any key...")
    pass

def get_lotto_num(no):
    print('get numbers!')
    lotto_url = "https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo=" + str(no)
    print(lotto_url)
    while 1:
        try:
            req = requests.get(lotto_url)
            break 
        except:
            print('ready...')
            time.sleep(3)
            continue
    soup = BeautifulSoup(req.text)
    line = str(soup.find("div",{'class':'nums'}))
    soup2 = BeautifulSoup(line)
    num = []
    for i in soup2.find_all('span'):
        temp = i.get_text()
        if temp == '':
            print('none data!!!')
            return False
        print (temp)
        num.append(temp)
    print(num)
    return num

def lotto_update():
    global lastnum
    global numbers
    no = lastnum
    ret = False
    check = True
    while check :
        no = no + 1
        ret = get_lotto_num(no)
        if ret == False :
            check = False
            break
        else :
            numbers[str(no)] = ret
            lastnum = no
            continue
    save_data()
    pass

def make_random():
    global count
    global lastnum
    global numbers
    num = []
    sel = []
    for i in range(1,46):
        for j in range(count[i]):
            num.append(str(i))
    for i in range(6):
        temp = random.choice(num)
        sel.append(temp)
        while 1 :
            try:
                num.remove(temp)
                continue
            except:
                # not exist
                break
            pass
        pass
    sel.sort()
    check_ranking(sel)
    tt = input("Enter any key...")

    pass


def check_numbers():
    global count
    global lastnum
    global numbers

    num_list = list(map(str, input('input num list (6) : ').split()))
    num_list.sort()
    check_ranking(num_list)
    tt = input("Enter any key...")
    pass

def check_ranking(list):
    global count
    global lastnum
    global numbers

    cnt = [0] * 6
    for i in range(lastnum):
        ret = compare_number(list, numbers[str(i+1)])
        cnt[ret] = cnt[ret] + 1
        print( str(i+1) + ' 회차 등수 : '  + str(ret) )
        pass
    print('number list : ', end='')
    print(list)
    print('ranking : ', end='')
    print(cnt)
    pass

def show_menu():
    global lastnum
    print('     ********  Info  ********')
    print('     Name : ' + name)
    print('     Last No : ' + str(lastnum) )
    print('''
    ******** Lotto Number ********
    1. Number Ranking
    2. Number Update
    3. Make number
    4. Check input numbers
    5. Exit
    ''')
    me = int(input("select : "))
    if me == 1:
        print_counter()
        return True
    elif me == 2:
        lotto_update()
        return True
    elif me == 3:
        make_random()
        return True
    elif me == 4:
        check_numbers()
        return True
    else :
        return False
    
def main():
    # 1. read json data
    init_data()
    checksum = True
    # 2. show menu
    while checksum :
        os.system('cls')
        checksum = show_menu()
    pass

if __name__ == "__main__":
    main()