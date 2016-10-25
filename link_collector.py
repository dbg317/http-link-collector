import time, requests, glob, os, re
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


def batch_rename():
    path = glob.glob('C:/Users/dbg316/Downloads/*.txt')  # return list of file paths in specified folder and file type
    print('found files:')
    for file_name in path:
        print(file_name)
    i = 1
    for pathname in path:
        basename = os.path.basename(pathname)  # get file name from full file path
        new_filename = basename.replace(basename[0:-4], str(i))  # use zfill(4) if want fixed digits

        try:
            # file name should be full file path
            os.rename(pathname, os.path.join(os.path.dirname(pathname), new_filename))
            i += 1
        except FileExistsError:
            i += 1
            pass

    path_renamed = glob.glob('C:/Users/dbg316/Downloads/*.txt')
    print('renamed to:')
    for file_name in path_renamed:
        print(file_name)


def get_all_links():
    file_name = '.txt'
    content = []
    final_content = []
    counter = 1
    for i in range(1,200):
        try:
            file = open('C:/Users/dbg316/Downloads/'+str(i)+file_name, 'r', encoding='gbk')  # utf-8, big5, gbk
            content.append(file.readlines())
            file.close()
            print('file number:',counter)
            counter += 1

        except UnicodeDecodeError:
            file.close()
            file = open('C:/Users/dbg316/Downloads/' + str(i) + file_name, 'r', encoding='big5')  # utf-8, big5, gbk
            content.append(file.readlines())
            file.close()
            print('file number:', counter)
            counter += 1

        except FileNotFoundError:
            print('FileNotFoundError, check if renamed all files')
            break
    # print(content)
    for item in content:
        for i in item:
            if 'http' in i and 'img]' not in i and '【圖站名稱】:' not in i:
                i = i.strip('\n')
                i = i.strip('\ufeff')
                final_content.append(i)
    for i in final_content:
        print(i)
    print('link number:', len(final_content))
    file = open('C:/Users/dbg316/Downloads/final content.txt','w')
    for i in final_content:
        file.writelines(i+'\n')
    return final_content


def open_all_links():  # too slow, copy all links to firefox bookmarks the open from browser is way faster
    link_list = get_all_links()
    driver = webdriver.Chrome()
    driver.get('http://www.google.ca')
    driver.maximize_window()
    time.sleep(2)
    tab_number = 1
    link_index = 1
    total_run_times = len(link_list)+1
    for i in link_list:
        time.sleep(2)
        tag_element = driver.find_element_by_tag_name('body')
        tag_element.send_keys(Keys.CONTROL + "t")
        time.sleep(2)
        print(tab_number, i)
        link_index += 1
        driver.switch_to_window(driver.window_handles[tab_number])
        tab_number += 1
        driver.get(i)
        if tab_number == total_run_times:
            input('press enter to quit')

# open_all_links()
batch_rename()
get_all_links()
