import requests

response = requests.get(
    "https://httpbin.org/get",
    proxies={
        "http": "http://4015c872c0e645929bb8360bb9638b10:@proxy.crawlera.com:8011/",
        "https": "http://4015c872c0e645929bb8360bb9638b10:@proxy.crawlera.com:8011/",
    },
    verify='zyte-proxy-ca.crt' 
)
print(response.text)