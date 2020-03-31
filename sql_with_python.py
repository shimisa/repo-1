import mysql.connector as mysql
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

###connecting to sql
db = mysql.connect(host="127.0.0.1", user="root", passwd="5864547", port="3306", database="YAD2")
print(db)
## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'##
cursor = db.cursor()


# cursor.execute("CREATE TABLE selenium_yad2 (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, url VARCHAR(225), address VARCHAR(255),rooms VARCHAR(10),price VARCHAR(22), floor VARCHAR(22))")

def main(address, city, room_num):
    global count_results
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\Alon_\OneDrive\שולחן העבודה\chromedriver.exe')
    driver.get("https://www.yad2.co.il/")
    driver.maximize_window()
    time.sleep(8)
    driver.find_element_by_xpath(
        '''/html/body/div[4]/div[2]/div/div[1]/header/nav/ul[2]/li[4]/a''').click()  # איזור אישי
    time.sleep(2)
    driver.find_element_by_xpath('''/html/body/div[8]/div[7]/div/div/div/form/table/tbody/tr[1]/td/input''').send_keys(
        "bertinidan4@gmail.com")  # username
    driver.find_element_by_xpath('''/html/body/div[8]/div[7]/div/div/div/form/table/tbody/tr[2]/td/input''').send_keys(
        "aa4455")  # password
    driver.find_element_by_xpath(
        '''/html/body/div[8]/div[7]/div/div/div/form/table/tbody/tr[3]/td/input''').click()  # enter
    driver.find_element_by_xpath('''/html/body/div[6]/div[1]/div[1]/div[1]/a''').click()  # back to home page
    time.sleep(2)
    driver.find_element_by_xpath(
        '''//*[@id="file-list"]/div/div[5]/div[1]/div/div/div[1]/a/img''').click()  # דירות להשכרה
    driver.find_element_by_xpath('''//*[@id="sub_item_realestate_1"]/div/div/h4''').click()  # יד 2 - הגדרות חיפוש
    time.sleep(10)
    driver.find_element_by_xpath(
        '''//*[@id="__layout"]/div/main/div/div[4]/div[4]/div/form/ul/li[1]/div/div/div[1]/div/label/div/input''').send_keys(
        address)
    time.sleep(10)
    options = driver.find_elements_by_xpath(
        '''//*[@id="__layout"]/div/main/div/div[4]/div[4]/div/form/ul/li[1]/div/div/div[2]/ul/li[3]''')  #
    for option in options:
        option_value = option.get_attribute("innerHTML")
        if city in option_value:
            option.click()
        else:
            print('cant find city')
            driver.close()
    driver.find_element_by_xpath(
        '''//*[@id="__layout"]/div/main/div/div[4]/div[4]/div/form/ul/li[2]/div/div/div[1]/button''').click()
    driver.find_element_by_xpath(
        '''//*[@id="__layout"]/div/main/div/div[4]/div[4]/div/form/ul/li[2]/div/div/div[2]/div/ul/li[1]/label''').click()  # סוג נכס
    driver.find_element_by_xpath(
        '''//*[@id="__layout"]/div/main/div/div[4]/div[4]/div/form/ul/li[3]/div/div/div[1]/button''').click()
    driver.find_element_by_xpath(
        '''//*[@id="__layout"]/div/main/div/div[4]/div[4]/div/form/ul/li[3]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div/label/div/input''').send_keys(
        str(room_num))
    time.sleep(2)
    driver.find_element_by_xpath(
        '''//*[@id="__layout"]/div/main/div/div[4]/div[4]/div/form/ul/li[3]/div/div/div[2]/div/div/div/div[1]/div/div[2]/i''').click()
    x = room_num * 2
    manu = driver.find_elements_by_xpath(
        '''/html/body/div[4]/div[2]/div/main/div/div[4]/div[4]/div/form/ul/li[3]/div/div/div[2]/div/div/div/div[1]/div/div[3]/ul/li[''' + str(
            x) + ''']''')
    for i in manu:  # מ  חדרים
        ivalue = i.get_attribute("innerHTML")
        if str(room_num) in ivalue:
            i.click()
    time.sleep(2)
    driver.find_element_by_xpath(
        '''//*[@id="__layout"]/div/main/div/div[4]/div[4]/div/form/ul/li[3]/div/div/div[2]/div/div/div/div[2]/div/div[2]/i''').click()
    p = driver.find_elements_by_xpath(
        '''/html/body/div[4]/div[2]/div/main/div/div[4]/div[4]/div/form/ul/li[3]/div/div/div[2]/div/div/div/div[2]/div/div[3]/ul/li[2]''')
    for l in p:  # עד 3 חדרים
        lvalue = l.get_attribute("innerHTML")
        time.sleep(2)
        if str(room_num) in lvalue:
            l.click()
    driver.find_element_by_xpath(
        '''//*[@id="__layout"]/div/main/div/div[4]/div[4]/div/form/ul/li[6]/button''').click()  # Search
    time.sleep(10)
    print(driver.current_url)
    try:
        count_results = driver.find_element_by_xpath(
            '''/html/body/div[4]/div[2]/div/main/div/div[4]/div[6]/div[2]/div[1]/div[1]/div/span[2]''')
    except:
        print("no results")
        driver.close()
        quit()
    cr = int(count_results.text[0:2])
    print(cr, "תוצאות חיפוש")
    z = 1
    i = 3
    while z <= cr:  # changing the xpath to get the next result on page --> 3->5->8..
        try:
            time.sleep(2)
            address = driver.find_element_by_xpath(
                '''/html/body/div[4]/div[2]/div/main/div/div[4]/div[6]/div[2]/div[4]/div[''' + str(
                    i) + ''']/div/div/div[1]/div[2]/span[1]/span''')
            details = driver.find_element_by_xpath(
                '''/html/body/div[4]/div[2]/div/main/div/div[4]/div[6]/div[2]/div[4]/div[''' + str(
                    i) + ''']/div/div/div[2]''')
            price = driver.find_element_by_xpath(
                '''/html/body/div[4]/div[2]/div/main/div/div[4]/div[6]/div[2]/div[4]/div[''' + str(
                    i) + ''']/div/div/div[3]/div[2]''')
            z += 1
            i += 2
            if i % 7 == 0:
                i += 1
            print_apartment(address, price, details)
            insert_sql(driver.current_url, address, details, price)
        except:
            i += 1
    driver.close()


def print_apartment(address, price, details):
    print(address.text + " " + price.text)
    print(details.text[0] + " " + details.text[2:7] + "    " + details.text[8] + " " + details.text[10:15])
    print("*" * 30)


def insert_sql(url, address, details, price):
    query = "INSERT INTO selenium_yad2 (url, address, rooms, price, floor) VALUES (%s, %s, %s, %s, %s)"
    values = [(url, address.text, details.text[0], price.text, details.text[8])]
    cursor.executemany(query, values)
    db.commit()


main("רוטשילד, תל אביב", "תל אביב", 3)
