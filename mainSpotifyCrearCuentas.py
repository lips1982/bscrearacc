# -*- coding: utf-8 -*-

import time
from PQTs.MongoDB.MongoDB import MongoDB

from PQTs.Selenium.Base import BaseConexion
from PQTs.Selenium.Acciones import Acciones

def main():

    driver = BaseConexion().conexionChrome()
    
    acciones = Acciones(driver)

    acciones.ingresarSpotify()

    acciones.sleep(3)

    #print (acciones.currenturl())

    mongoDB = MongoDB()
    mongoDB.iniciarDB()

    result = mongoDB.find("accountmanager",{"acc_estado":0})
    print (len(result))
    
    if len(result) > 0:

        usuario = result[0]

        usuario_singupdata = mongoDB.findOne("acc_user_info_singup",{"_id":usuario["_id"]})

        #mongoDB.updateOne("accountmanager",usuario["_id"],{"acc_estado":5})

        mongoDB.cerrarConexion()

        print (f'INICIANDO {usuario["email"]} pass: {usuario["pass"]} user {usuario["username"]}')
        
        returnAgregarDatos =  acciones.agregarDatos(usuario["email"],usuario["pass"],usuario["username"],usuario_singupdata["month"],usuario_singupdata["day"],usuario_singupdata["year"],usuario_singupdata["genero"])
        
        '''
        print ("presiones C para actualizar la BD :")
        valor= input( )
        
        if valor =="c":
            mongoDB.iniciarDB()

            cuentaConEmail = mongoDB.find("accountmanager",{"email":usuario["email"]})
            cuentaRegistrada = cuentaConEmail[0]
            mongoDB.updateOne("accountmanager",cuentaRegistrada["_id"],{"acc_estado":1})
            mongoDB.cerrarConexion()
            print("actualizando la BD")
        else:
            pass
        '''
        
        if returnAgregarDatos:

            returnIframeCaptcha = acciones.iframeRecaptchaInicio()

            if returnIframeCaptcha:

                acciones.sleep(25)
                #print (f"01 {acciones.currenturl()}")
                mongoDB = MongoDB()
                mongoDB.iniciarDB()

                cuentaConEmail = mongoDB.find("accountmanager",{"email":usuario["email"]})

                cuentaRegistrada = cuentaConEmail[0]
                
                returnUrlContains = acciones.explicitWaitUrl(30,"https://www.spotify.com/us/download/linux")
                
                
                if returnUrlContains:

                    print ("entro a true", returnUrlContains)
                    mongoDB.updateOne("accountmanager",cuentaRegistrada["_id"],{"acc_estado":3})
                else:
                    mongoDB.updateOne("accountmanager",cuentaRegistrada["_id"],{"acc_estado":3})

                print (f'finalizado {usuario["email"]}')

                mongoDB.cerrarConexion()

            else:
                print(f"02 returnIframeCaptcha {returnIframeCaptcha}")

                acciones.tomarScreenshot("02 returnIframeCaptcha")
                acciones.obtenerHTML("02 returnIframeCaptcha")

                mongoDB = MongoDB()
                mongoDB.iniciarDB()

                cuentaConEmail = mongoDB.find("accountmanager",{"email":usuario["email"]})
                cuentaRegistrada = cuentaConEmail[0]

                mongoDB.updateOne("accountmanager",cuentaRegistrada["_id"],{"acc_estado":3})

                mongoDB.cerrarConexion()

        else:
            print(f"01 returnAgregarDatos {returnAgregarDatos}")

            acciones.tomarScreenshot("01 returnAgregarDatos")
            acciones.obtenerHTML("01 returnAgregarDatos")

if __name__ == '__main__':
   while True: 
        main()
        time.sleep(360)
   
