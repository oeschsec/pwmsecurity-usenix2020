import selenium
from selenium import webdriver
import subprocess
import time
import math
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys


class Scraper:

    def __init__(self,url,driver):
        self.url = url
        self.options = Options()
        self.options.headless = True # /home/toesch/Passwords/geckodriver
        self.initialize()

    def initialize(self):
        self.driver = webdriver.Firefox(options=self.options,executable_path='/home/toesch/Passwords/geckodriver')
        self.driver.get(self.url)

    def cleanup(self):
        self.driver.quit()

    def generatePassword(self):
        return ["",0]

    def waitForElement(self,element,type):

        wait = True
        while wait:
            try:
                if type == "id":
                    self.driver.find_element_by_id(element)
                elif type == "class":
                    self.driver.find_element_by_class_name(element)
                else:
                    self.driver.find_element_by_xpath(element)
            except NoSuchElementException:
                pass
            wait = False

class OnePass(Scraper):

    def __init__(self,length,digits,symbols):
        super().__init__("https://1password.com/password-generator","firefox")
        self.setlength(length)
        self.digits(digits)
        self.symbols(symbols)

    def generatePassword(self):
        self.driver.find_element_by_id('refresh-token').click()
        self.password = self.driver.find_element_by_class_name('password-overlay').text
        return self.password

    def setlength(self,length):
        move = ActionChains(self.driver)
        slider = self.driver.find_element_by_id('myRange')
        width = slider.size['width'] # width of slider
        inc = float(width)/100 # units by which to increment
        xpos = length*inc - 8*inc # start closer to value
        # move slider until it is at appropriate value
        while str(length) != self.driver.find_element_by_class_name('slider-value').text:
            print(self.driver.find_element_by_class_name('slider-value').text)
            #move.move_to_element_with_offset(slider, xpos,0).click_and_hold().release().perform()
            xpos = xpos + inc
            slider.send_keys(Keys.LEFT) #Goot it!
            
            #if int(self.driver.find_element_by_class_name('slider-value').text) > length:
             #   xpos = xpos - 2*inc 
            #else:
             #   xpos = xpos + inc/2


    def digits(self,input):
        if input:
            if not self.driver.find_element_by_id('numbers').is_selected():
                self.driver.find_element_by_id('numbers').click()
        else:
            if self.driver.find_element_by_id('numbers').is_selected():
                self.driver.find_element_by_id('numbers').click()

    def symbols(self,input):
        if input:
            if not self.driver.find_element_by_id('symbols').is_selected():
                self.driver.find_element_by_id('symbols').click()
        else:
            if self.driver.find_element_by_id('symbols').is_selected():
                self.driver.find_element_by_id('symbols').click()

class DashLane(Scraper):

    def __init__(self,length,letters,digits,symbols):
        super().__init__("https://www.dashlane.com/features/password-generator","firefox")
        self.setlength(length)
        self.letters(letters)
        self.digits(digits)
        self.symbols(symbols)

    def generatePassword(self):
        self.driver.find_element_by_class_name('js-generate-password-btn').click()
        time.sleep(.5) # it scrambles password - takes about half a second and you'll get bad value if you grab earlier
        self.password = str(self.driver.find_element_by_class_name('js-password').text)
        return self.password

    def setlength(self,length):
        self.driver.execute_script("arguments[0].innerHTML="+str(length), self.driver.find_element_by_class_name('js-range-slider-length-value'))

    def digits(self,input):
        if input:
            if not self.driver.find_element_by_id('contains-digits').is_selected():
                self.driver.find_element_by_xpath('//label[text()="Digits"]').click()
        else:
            if self.driver.find_element_by_id('contains-digits').is_selected():
                self.driver.find_element_by_xpath('//label[text()="Digits"]').click()              


    def letters(self,input):
        if input:
            if not self.driver.find_element_by_id('contains-letters').is_selected():
                self.driver.find_element_by_xpath('//label[text()="Letters"]').click()
        else:
            if self.driver.find_element_by_id('contains-letters').is_selected():
                print("click")
                self.driver.find_element_by_xpath('//label[text()="Letters"]').click()                

    def symbols(self,input):
        if input:
            if not self.driver.find_element_by_id('contains-symbols').is_selected():
                self.driver.find_element_by_xpath('//label[text()="Symbols"]').click()
        else:
            if self.driver.find_element_by_id('contains-symbols').is_selected():
                self.driver.find_element_by_xpath('//label[text()="Symbols"]').click()

class LastPass(Scraper):

    hidden = False

    def __init__(self,length,letters,digits,symbols):
        super().__init__("https://www.lastpass.com/password-generator","firefox")
        self.setlength(length)
        self.letters(letters)
        self.digits(digits)
        self.symbols(symbols)

    def generatePassword(self):
        while not self.driver.find_element_by_class_name('lp-pg-generated-password__icon-generate').is_displayed():
            pass
        self.driver.find_element_by_class_name('lp-pg-generated-password__icon-generate').click()
        #self.driver.find_element_by_class_name('lp-pg-copy-password__button').click()
        # hide popup so that it does not obscur element
        #if not self.hidden: 
            #self.driver.execute_script("arguments[0].style.visibility='hidden'", self.driver.find_element_by_class_name("lp-pg-popup"))
            #self.hidden = True
        #self.password = subprocess.check_output(["xsel", "--clipboard"])
        while str(self.driver.find_element_by_class_name('lp-pg-generated-password__input').get_attribute('value')) == "":
            pass
        self.password = str(self.driver.find_element_by_class_name('lp-pg-generated-password__input').get_attribute('value'))
        return self.password
        #return self.password.decode()

    def setlength(self,length):
        #self.driver.execute_script("arguments[0].innerHTML="+str(length), self.driver.find_element_by_id('lp-pg-password-length'))
        self.driver.find_element_by_id('lp-pg-password-length').clear()
        self.driver.find_element_by_id('lp-pg-password-length').send_keys(str(length))

    def digits(self,input):
        if input:
            if not self.driver.find_element_by_id('lp-pg-numbers').is_selected():
                self.driver.find_element_by_xpath('//label[@for="lp-pg-numbers"]').click()
        else:
            if self.driver.find_element_by_id('lp-pg-numbers').is_selected():
                self.driver.find_element_by_xpath('//label[@for="lp-pg-numbers"]').click()

    def symbols(self,input):
        if input:
            if not self.driver.find_element_by_id('lp-pg-symbols').is_selected():
                self.driver.find_element_by_xpath('//label[@for="lp-pg-symbols"]').click()
        else:
            if self.driver.find_element_by_id('lp-pg-symbols').is_selected():
                self.driver.find_element_by_xpath('//label[@for="lp-pg-symbols"]').click()

    def letters(self,input):
        if input:
            if not self.driver.find_element_by_id('lp-pg-uppercase').is_selected():
                self.driver.find_element_by_xpath('//label[@for="lp-pg-uppercase"]').click()
            if not self.driver.find_element_by_id('lp-pg-lowercase').is_selected():
                self.driver.find_element_by_xpath('//label[@for="lp-pg-lowercase"]').click()
        else:
            if self.driver.find_element_by_id('lp-pg-uppercase').is_selected():
                self.driver.find_element_by_xpath('//label[@for="lp-pg-uppercase"]').click()
            if self.driver.find_element_by_id('lp-pg-lowercase').is_selected():
                self.driver.find_element_by_xpath('//label[@for="lp-pg-lowercase"]').click()

class PassGen(Scraper):

    def __init__(self,length,letters,digits,symbols):
        super().__init__("https://passwordsgenerator.net/","firefox")
        self.setlength(length)
        self.letters(letters)
        self.digits(digits)
        self.symbols(symbols)
        self.driver.find_element_by_xpath('//label[text()="( e.g. i, l, 1, L, o, 0, O )"]').click() #don't want this one selected

    def generatePassword(self):
        while not self.driver.find_element_by_class_name('GenerateBtn').is_displayed():
            pass
            
        self.driver.find_element_by_class_name('GenerateBtn').click()

        self.password = str(self.driver.find_element_by_id('final_pass').get_attribute('value'))
        return self.password

    def setlength(self,length):
        el = self.driver.find_element_by_id('pgLength')
        for option in el.find_elements_by_tag_name('option'):
            if option.text == str(length):
                option.click() 
                break

    def digits(self,input):
        if input:
            if not self.driver.find_element_by_id('Numbers').is_selected():
                self.driver.find_element_by_xpath('//label[text()="( e.g. 123456 )"]').click()
        else:
            if self.driver.find_element_by_id('Numbers').is_selected():
                self.driver.find_element_by_xpath('//label[text()="( e.g. 123456 )"]').click()


    def symbols(self,input):
        if input:
            if not self.driver.find_element_by_id('Symbols').is_selected():
                self.driver.find_element_by_xpath('//label[text()="( e.g. @#$% )"]').click()
        else:
            if self.driver.find_element_by_id('Symbols').is_selected():
                self.driver.find_element_by_xpath('//label[text()="( e.g. @#$% )"]').click()

    def letters(self,input):
        if input:
            if not self.driver.find_element_by_id('Lowercase').is_selected():
                self.driver.find_element_by_xpath('//label[text()="( e.g. abcdefgh )"]').click()
            if not self.driver.find_element_by_id('Uppercase').is_selected():
                self.driver.find_element_by_xpath('//label[text()="( e.g. ABCDEFGH )"]').click()
        else:
            if self.driver.find_element_by_id('Lowercase').is_selected():
                self.driver.find_element_by_xpath('//label[text()="( e.g. abcdefgh )"]').click()
            if self.driver.find_element_by_id('Uppercase').is_selected():
                self.driver.find_element_by_xpath('//label[text()="( e.g. ABCDEFGH )"]').click()

class RoboForm(Scraper):

    def __init__(self,length,letters,digits,symbols):
        super().__init__("https://www.roboform.com/password-generator","firefox")
        self.setlength(length)
        self.letters(letters)
        self.digits(digits)
        self.symbols(symbols)

    def generatePassword(self):
        #element = self.driver.find_element_by_xpath("//div[@class='c']")
        #self.driver.execute_script("arguments[0].style.visibility='hidden'", element)
        #element = self.driver.find_element_by_xpath("//div[@class='cookies-notification']")
        #self.driver.execute_script("arguments[0].style.visibility='hidden'", element)
        element = self.driver.find_element_by_xpath("//div[@class='cookies-notification-container']")
        self.driver.execute_script("arguments[0].style.visibility='hidden'", element)
        self.driver.find_element_by_id('button-password').click()
        self.password = str(self.driver.find_element_by_class_name('text-password').get_attribute('value'))
        return self.password

    def setlength(self,length):
        self.driver.find_element_by_class_name('number-password-text').clear()
        self.driver.find_element_by_class_name('number-password-text').send_keys(str(length))

    def digits(self,input):
        if input:
            if not self.driver.find_element_by_id('check-numeric-register').is_selected():
                self.driver.find_element_by_class_name('label-numeric-register').click()
        else:
            if self.driver.find_element_by_id('check-numeric-register').is_selected():
                self.driver.find_element_by_class_name('label-numeric-register').click()              


    def letters(self,input):
        if input:
            if not self.driver.find_element_by_id('check-lowercase').is_selected():
                self.driver.find_element_by_class_name('label-lowercase').click()
            if not self.driver.find_element_by_id('check-uppercase').is_selected():
                self.driver.find_element_by_class_name('label-uppercase').click()
        else:
            if self.driver.find_element_by_id('check-lowercase').is_selected():
                self.driver.find_element_by_class_name('label-lowercase').click()
            if self.driver.find_element_by_id('check-uppercase').is_selected():
                self.driver.find_element_by_class_name('label-uppercase').click()                

    def symbols(self,input):
        if input:
            if not self.driver.find_element_by_id('check-character').is_selected():
                self.driver.find_element_by_class_name('label-character').click()
        else:
            if self.driver.find_element_by_id('check-character').is_selected():
                self.driver.find_element_by_class_name('label-character').click()




