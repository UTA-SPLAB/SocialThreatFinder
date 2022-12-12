import whois

def registrar_info(url):
   
   w = whois.whois(url)
   return w['registrar']



# Tester
# registrar_name=urlchecker('http://www.google.com')
# print(reg)

