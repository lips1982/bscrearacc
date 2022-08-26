# -*- coding: utf-8 -*-

import time
from PQTs.MongoDB.MongoDB import MongoDB

import string, random, httpx,  time
from pystyle import *

import ssl

def main():
    
    httpx._config.DEFAULT_CIPHERS += ":ALL:@SECLEVEL=1"
    
    acciones = True

    if acciones:
        
        mongoDB = MongoDB()
        mongoDB.iniciarDB()

        result = mongoDB.find("accountmanager",{"acc_estado":0})
        print (len(result))
    
        if len(result) > 0:

            usuario = result[0]

            mongoDB.cerrarConexion()

            print (f'INICIANDO {usuario["email"]} pass: {usuario["pass"]} user {usuario["username"]}')
        
            def getRandomString(length):
                pool=string.ascii_lowercase+string.digits
                return "".join(random.choice(pool) for i in range(length))


            headers={"Accept-Encoding": "gzip",
                        "Accept-Language": "en-US",
                        "App-Platform": "Android",
                        "Connection": "Keep-Alive",
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Host": "spclient.wg.spotify.com",
                        "User-Agent": "Spotify/8.6.72 Android/29 (SM-N976N)",
                        "Spotify-App-Version": "8.6.72", "X-Client-Id": getRandomString(32)
                        }
            payload = {"creation_point": "client_mobile",
                        "gender": "male" if random.randint(0, 1) else "female",
                        "birth_year": random.randint(1999, 2001),
                        "displayname": usuario["username"],
                        "iagree": "true",
                        "birth_month": random.randint(1, 11),
                        "password_repeat": usuario["pass"],
                        "password": usuario["pass"],
                        "key": "4c7a36d5260abca4af282779720cf631",
                        "platform": "Android-ARM",
                        "email": usuario["email"],
                        "birth_day": random.randint(1, 20)}
            context = ssl.create_default_context()
            context.load_verify_locations(cafile="zyte-proxy-ca.crt")
            # context = httpx.create_ssl_context(None,)# .create_ssl_context(verify="zyte-proxy-ca.crt")
            r = httpx.post('https://spclient.wg.spotify.com/signup/public/v1/account/', headers=headers, data=payload)
            print(r.text)

            if r.status_code==200:
                if r.json()['status']==1:
                    mongoDB = MongoDB()
                    mongoDB.iniciarDB()

                    cuentaConEmail = mongoDB.find("accountmanager",{"email":usuario["email"]})
                    cuentaRegistrada = cuentaConEmail[0]

                    mongoDB.updateOne("accountmanager",cuentaRegistrada["_id"],{"acc_estado":1})
                    mongoDB.updateOne("accountmanager",cuentaRegistrada["_id"],{"pais":"US"})
                    
                    print("cuenta creada")
                    mongoDB.cerrarConexion()
                else:
                    print("cuenta fail") 
                    exit()       

if __name__ == '__main__':
   while True: 
        main()

        time.sleep(10)
   
