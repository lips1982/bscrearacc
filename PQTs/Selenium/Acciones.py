# -*- coding: utf-8 -*-

from outcome import acapture
from PQTs.Selenium.Base import BaseAcciones

from PQTs.Utilizar import urlSpotifySingUp

from PQTs.Paths import pathDescargas,pathAudioMp3,pathAudioWav,pathImg

from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import urllib
import pydub
import speech_recognition as sr

import os
import glob
from bs4 import BeautifulSoup


scriptDivButtonRegistrate = """
let xpathDivButtonRegistrate = '//button/div[contains(text(),"Registrarte")]';
let elementoDivButtonRegistrate = document.evaluate(xpathDivButtonRegistrate, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
if (elementoDivButtonRegistrate) {
    elementoDivButtonRegistrate.click();
    return true;
} else return false;
"""


class Acciones(BaseAcciones):

    def __init__(self, driver):
        self.driver = driver

      #-----------------#
     #---> Spotify <---#
    #-----------------#
#ipinfo=(requests.get('https://api.myip.com').json())

    def checkipinfo(self):
        self.ir("https://api.myip.com")
        self.sleep(10)
        elemento= (By.XPATH,"/html/body")
        ipinfo= self.ipdatos(elemento)
        if '"CO"' in ipinfo:
            print (ipinfo)
            return True
        else:
            return False
        self.sleep(4)
        #self.driver.execute_script("document.body.style.zoom='100%'")
        #self.sleep(5)
    def agregarDatos(self,emails,password,username,mes,dia,year,genero):
        idInputEmail = (By.ID,"email")
        idInputConfirm = (By.ID,"confirm")
        idInputPassword = (By.ID,"password")
        idInputDisplayname = (By.ID,"displayname")
        idInputMonth = (By.ID,"month")
        idInputDay = (By.ID,"day")
        idInputYear = (By.ID,"year")
        idButtonGenero = (By.XPATH,genero)

        visibleInputEmail = self.explicitWaitElementoVisibility(20,idInputEmail)
        if visibleInputEmail:
            self.escribir(idInputEmail,emails)
            self.escribir(idInputConfirm,emails)
            self.escribir(idInputPassword,password)
            self.escribir(idInputDisplayname,username)
            self.escribir(idInputMonth,mes)
            self.escribir(idInputDay,dia)
            self.escribir(idInputYear,year)

            
            buttonGenero = self.findElement(idButtonGenero)
            self.driver.execute_script("arguments[0].click();",buttonGenero)

            self.sleep(3)

            return True
        else:
            print(f"visibleInputEmail {visibleInputEmail}")
            return False


    def iframeRecaptchaInicio(self,contador = 0):
        xpathIframeRecaptcha = (By.XPATH,'//iframe[@title="reCAPTCHA" and contains(@src,"size=normal")]')
        xpathSpanRecaptchaAnchor = (By.XPATH,'//span[@id="recaptcha-anchor"]')

        xpathSpanAriaChecked = (By.XPATH,'//span[@id="recaptcha-anchor"]')

        xpathDivButtonRegistrate = (By.XPATH,'//button/div[contains(text(),"Registrarte")]')

        xpathIframeImagenes = (By.XPATH,'//iframe[@style="width: 400px; height: 580px;"]')
        xpathIframeImagenesButtonAudio = (By.XPATH,'//button[@id="recaptcha-audio-button"]')

        xpathIframeAudio = (By.XPATH,'//iframe[@style="width: 280px; height: 275px;"]')
        xpathIframeAudioInput = (By.XPATH,'//input[@id="audio-response"]')



        scriptExisteIframeRecaptcha = """
        let xpathrecaptcha = '//iframe[@title="reCAPTCHA" and contains(@src,"size=normal")]';
        let elementoIframeRecaptcha = document.evaluate(xpathrecaptcha, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (elementoIframeRecaptcha) {
        return true;
        } else return false;
        """
        existeIframeRecaptcha = self.driver.execute_script(scriptExisteIframeRecaptcha)
        if existeIframeRecaptcha:
            self.switchToDefaultContent()
            self.switchToIframe(xpathIframeRecaptcha)
            
            self.sleep(3)

            self.driver.execute_script("document.getElementById('recaptcha-anchor').click();")

            self.sleep(8)
            
            attributeAriaChecked = self.findElement(xpathSpanAriaChecked).get_attribute("aria-checked")
            self.switchToDefaultContent()
            print(f"--- attributeAriaChecked {attributeAriaChecked}")
            if attributeAriaChecked == "true":

                visibleDivButtonRegistrate = self.explicitWaitElementoVisibility(20,xpathDivButtonRegistrate)
                if visibleDivButtonRegistrate:
                    #self.click(xpathDivButtonRegistrate)
                    clickDivButtonRegistrate = self.driver.execute_script(scriptDivButtonRegistrate)
                    if clickDivButtonRegistrate:
                        return True
                    else:
                        self.tomarScreenshot(f"visibleDivButtonRegistrate {visibleDivButtonRegistrate}")
                        self.obtenerHTML(f"visibleDivButtonRegistrate {visibleDivButtonRegistrate}")
                else:
                    return False
            else:
                visibleIframeImagenes = self.explicitWaitElementoVisibility(5,xpathIframeImagenes)
                if visibleIframeImagenes:
                    self.driver.execute_script("window.scrollTo(0, window.scrollY + 600)")
                    self.switchToIframe(xpathIframeImagenes)

                    visibleIframeImagenesButtonAudio = self.explicitWaitElementoVisibility(8,xpathIframeImagenesButtonAudio)
                    if visibleIframeImagenesButtonAudio:
                        self.click(xpathIframeImagenesButtonAudio)

                        self.sleep(8)
                        self.switchToDefaultContent()


                        visibleIframeAudio = self.explicitWaitElementoVisibility(8,xpathIframeAudio)
                        if visibleIframeAudio:
                            self.switchToIframe(xpathIframeAudio)

                            scriptSrcAudioCaptcha = """
                            let elementoAudioSource = document.getElementById("audio-source");
                            if (elementoAudioSource) {
                                return elementoAudioSource.getAttribute("src");
                            } else {
                                return false;
                            }
                            """
                            srcAudioCaptcha = self.executeScript(scriptSrcAudioCaptcha)
                            if srcAudioCaptcha:
                                try:

                                    urllib.request.urlretrieve(srcAudioCaptcha,pathAudioMp3)

                                    sound = pydub.AudioSegment.from_mp3(pathAudioMp3)
                                    sound.export(pathAudioWav, format="wav")
                                    sample_audio = sr.AudioFile(pathAudioWav)
                                    
                                    r = sr.Recognizer()
                                    with sample_audio as source:
                                        audio = r.record(source)
                                    key = r.recognize_google(audio)
                                    print(f"[INFO] Recaptcha Passcode: {key}")

                                    self.click(xpathIframeAudioInput)

                                    self.escribir(xpathIframeAudioInput,key.lower())
                                    self.escribir(xpathIframeAudioInput,Keys.ENTER)

                                    self.sleep(8)
                                    self.switchToDefaultContent()

                                    self.sleep(5)

                                    #self.click(xpathDivButtonRegistrate)
                                    clickDivButtonRegistrate = self.driver.execute_script(scriptDivButtonRegistrate)
                                    if clickDivButtonRegistrate:
                                        return True
                                    else:
                                        self.tomarScreenshot(f"visibleDivButtonRegistrate {visibleDivButtonRegistrate}")
                                        self.obtenerHTML(f"visibleDivButtonRegistrate {visibleDivButtonRegistrate}")
                                except:
                                    return False
                                finally:
                                    ficherosAudios = os.listdir(pathDescargas)
                                    if len(ficherosAudios) > 0:
                                        #os.system(f"remove {pathDescargas}/*")
                                        files = glob.glob(f'{pathDescargas}/*.wav')
                                        for wav in files:
                                            try:
                                                os.remove(wav)
                                            except OSError as e:
                                                print(f"Error:{ e.strerror}") 
                                        self.sleep(1)           
                                        files = glob.glob(f'{pathDescargas}/*.mp3')
                                        for mp3 in files:
                                            try:
                                                os.remove(mp3)
                                            except OSError as e:
                                                print(f"Error:{ e.strerror}")    
                            else:
                                return False

                        else:
                            return False
                    else:
                        return False

                else:
                    if contador >= 3:
                        return False
                    else:
                        contador+=1
                        self.iframeRecaptchaInicio(contador)

      #----------------------#
     #---> Herramientas <---#
    #----------------------#

    def tomarScreenshot(self,nombreImagen):
        self.screenshot(nombreImagen)

    def obtenerHTML(self,nombre):
        html_source_code = self.executeScript("return document.body.innerHTML;")
        soup = BeautifulSoup(html_source_code, 'html.parser')
        with open(os.path.join(pathImg,f"{nombre}.html"), 'w') as f:
            f.write(str(soup))