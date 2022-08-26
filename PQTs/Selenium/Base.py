# -*- coding: utf-8 -*-

from logging import exception
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from PQTs.Paths import pathImg

import os

class BaseConexion():
    def __init__(self):
        self.options = webdriver.ChromeOptions()

        self.options.page_load_strategy = 'normal'   
        self.options.add_argument("--window-size=1280,982")     
        self.options.add_argument("--no-sandbox")
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument("--disable-setuid-sandbox")
        self.options.add_argument('--ignore-ssl-errors=yes')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-infobars')
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option("excludeSwitches", ["enable-logging","enable-automation"])
        self.options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})

    def conexionChromeHeadless(self) :
        self.options.add_argument("--headless")
        driver = webdriver.Chrome("chromedriver",options=self.options)
        return driver

    def conexionChrome(self) :        
        driver = webdriver.Chrome("chromedriver",options=self.options)
        return driver

class BaseAcciones():
    def __init__(self, driver):
        self.driver = driver

    def ir(self, url):
        self.driver.get(url)
    def ipdatos(self, el):
        ipinfo=self.findElement(el).text
        return ipinfo
        
        
    def salir(self):
        self.driver.quit()

    def findElement(self, el):
        elemento = self.driver.find_element(*el)
        return elemento

    def escribir(self, el, msj):
        self.findElement(el).send_keys(msj)
        self.sleep(1)

    def maximizar(self):
        self.driver.maximize_window()

    def click(self, el):
        self.findElement(el).click()
        self.sleep(0.8)

    def sleep(self, sec):
        time.sleep(sec)

    def currenturl(self):

        return self.driver.current_url

    def tituloventana(self):
        try: 
            resul=self.driver.title
            return resul
        except Exception as e:
            print ("AQUI ERROR",e)
            

    def executeScript(self, script):
        return self.driver.execute_script(script)

    def switchToIframe(self, el):
        iframe = self.findElement(el)
        self.driver.switch_to.frame(iframe)

    def switchToDefaultContent(self):
        self.driver.switch_to.default_content()

    def explicitWaitElementoVisibility(self,time,el):
        try:
            elemento = WebDriverWait(self.driver, timeout=time).until(expected_conditions.visibility_of_element_located(el))
            return elemento
        except:
            return False

    def explicitWaitElementoInvisibility(self,time,el):
        try:
            elemento = WebDriverWait(self.driver, timeout=time).until(expected_conditions.invisibility_of_element_located(el))
            return elemento
        except:
            return False

    def explicitWaitUrl(self,time,url):
        try:
            url = WebDriverWait(self.driver, timeout=time).until(expected_conditions.url_contains("us/download"))
            
            print (url)
            return url
        except:
            return False

    def screenshot(self,nombre):
        #directorio = os.path.join(os.path.dirname(__file__),'..','..','static','Almacenamiento','screenshots',f"{tiempo}",f"{nombre}.png")
        
        #directorio = os.path.join(os.path.dirname(__file__),'..','..',f"{nombre}.png")
        directorio = os.path.join(pathImg,f"{nombre}.png")
        self.driver.save_screenshot(directorio)