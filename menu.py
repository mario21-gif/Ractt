from colorama import Fore, Back, Style
import os, sys
import subprocess
import secrets
import urllib.request
from faker import Faker
from faker.providers import internet
import phonenumbers
from phonenumbers import geocoder, carrier
import socket
import whois
import urllib3
import requests
import json

# Tools
def PasswordMaker():

 banner = r"""

██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗     ███╗   ███╗ █████╗ ██╗  ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║    ██╔████╔██║███████║█████╔╝ █████╗  ██████╔╝
██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║    ██║╚██╔╝██║██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗
██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝    ██║ ╚═╝ ██║██║  ██║██║  ██╗███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                                  


"""

 print(Fore.RED + Style.NORMAL + banner)

 def password():
    print(Fore.WHITE + secrets.token_hex(7))
    print("┌── Do you want to make a new password ? (Y/n) ")
    restart = input("└───➤ PasswordMaker@User ")
    if restart == "Y":
        password()
    elif restart == "y":
        password()
    else:
        sys.exit()

 password()

def IPLookup():

 def main():
  banner = r"""
██╗██████╗     ██╗      ██████╗  ██████╗ ██╗  ██╗██╗   ██╗██████╗ 
██║██╔══██╗    ██║     ██╔═══██╗██╔═══██╗██║ ██╔╝██║   ██║██╔══██╗
██║██████╔╝    ██║     ██║   ██║██║   ██║█████╔╝ ██║   ██║██████╔╝
██║██╔═══╝     ██║     ██║   ██║██║   ██║██╔═██╗ ██║   ██║██╔═══╝ 
██║██║         ███████╗╚██████╔╝╚██████╔╝██║  ██╗╚██████╔╝██║     
╚═╝╚═╝         ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     



"""
  print(Fore.RED + Style.NORMAL + banner)
  print(Fore.GREEN + "[I] You can get: ISP, city and country.")
  print(Fore.GREEN + "[I] Rate Limit: 1000/Day")
  print(Fore.WHITE + Style.NORMAL + "┌── Please enter an IP Address")
  ip = input("└───➤ IPLookup@User ").strip()

  url = f"http://ip-api.com/json/{ip}?fields=isp,city,country,regionName,zip,lat,lon,timezone"
  data = json.loads(urllib.request.urlopen(url).read().decode())

  print(Fore.CYAN + "\n┌─── Results ───────────────────")
  print(Fore.GREEN + f"│ [+] Country   : {data.get('country', 'N/A')}")
  print(Fore.GREEN + f"│ [+] City      : {data.get('city', 'N/A')}")
  print(Fore.GREEN + f"│ [+] Region    : {data.get('regionName', 'N/A')}")
  print(Fore.GREEN + f"│ [+] ZIP       : {data.get('zip', 'N/A')}")
  print(Fore.GREEN + f"│ [+] ISP       : {data.get('isp', 'N/A')}")
  print(Fore.GREEN + f"│ [+] Timezone  : {data.get('timezone', 'N/A')}")
  print(Fore.GREEN + f"│ [+] Lat/Lon   : {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
  print(Fore.GREEN + f"│ [+] ORG  : {data.get('org', 'N/A')}")
  print(Fore.CYAN + "└───────────────────────────────\n")
  print("┌── Do you want to do a new lookup ? (Y/n) ")
  restart = input("└───➤ IPLookup@User ")
  if restart == "Y":
        main()
  elif restart == "y":
        main()
  else:
        sys.exit()

 main()

def IPGenerator():
 banner = r"""
██╗██████╗      ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
██║██╔══██╗    ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██║██████╔╝    ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
██║██╔═══╝     ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
██║██║         ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝╚═╝          ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                                                                                                                                                                            


"""
 def main():
  fake = Faker()



  print(Fore.RED + banner)

  for i in range(2):
            print(Fore.GREEN + "[+] Fake IPV4 (Public): " + fake.ipv4_public())

  for i in range(3):
            print(Fore.GREEN + "[+] Fake IPV4 (Private): " + fake.ipv4_private())

  for i in range(3):
            print(Fore.GREEN + "[+] Fake IPV6: " + fake.ipv6())
  print("┌── Do you want to generate a new IP ? (Y/n) ")
  restart = input("└───➤ IPGenerator@User ")
  if restart == "Y":
        main()
  elif restart == "y":
        main()
  else:
        sys.exit()

 main()

def PhoneChecker():   
 banner = r"""
██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██████╔╝███████║██║   ██║██╔██╗ ██║█████╗      ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██╔══╝      ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                       


"""
 def main():
  print(Fore.RED + Style.NORMAL + banner)

  print(Fore.RESET + "┌── Please enter a phone number (International Format Only)")
  num = input("└───➤ PhoneChecker@User ")
  numero = phonenumbers.parse(num)
  print(Fore.CYAN + "E164 Format:", phonenumbers.format_number(numero, phonenumbers.PhoneNumberFormat.E164))
  print(Fore.CYAN + "International Format:", phonenumbers.format_number(numero, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
  print(Fore.CYAN + "National Format:", phonenumbers.format_number(numero, phonenumbers.PhoneNumberFormat.NATIONAL))
  print(Fore.CYAN + "RFC3966 Format:", phonenumbers.format_number(numero, phonenumbers.PhoneNumberFormat.RFC3966))
  print(Fore.CYAN + "Carrier:", carrier.name_for_number(numero, "en"))
  print(Fore.CYAN + "Country:", geocoder.description_for_number(numero, "en"))
  print("┌── Do you want to check a new number ? (Y/n) ")
  restart = input("└───➤ PhoneChecker@User ")
  if restart == "Y":
        main()
  elif restart == "y":
        main()
  else:
        sys.exit()
 main()


def WhoisChecker():

 def main():
  banner = """
██╗    ██╗██╗  ██╗ ██████╗ ██╗███████╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██║    ██║██║  ██║██╔═══██╗██║██╔════╝    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║ █╗ ██║███████║██║   ██║██║███████╗    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██║███╗██║██╔══██║██║   ██║██║╚════██║    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
╚███╔███╔╝██║  ██║╚██████╔╝██║███████║    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
 ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                  

                                                                       
"""

  print(Fore.RED + Style.NORMAL + banner)
  print(Fore.WHITE + Style.NORMAL + "┌── Please enter a domain (Example: example.com)")
  domaine = input("└───➤ WhoisCheck@User ")
  results = whois.whois(domaine)
  print(Fore.CYAN + Style.BRIGHT + "Domain Name:", results.domain_name)
  print(Fore.CYAN + Style.BRIGHT + "Registrar:", results.registrar)
  print(Fore.CYAN + Style.BRIGHT + "Registrat site:", results.registrar_url)
  print(Fore.CYAN + Style.BRIGHT + "Whois Server:", results.whois_server)
  print(Fore.CYAN + Style.BRIGHT + "Last Update Date:", results.updated_date)
  print(Fore.CYAN + Style.BRIGHT + "Creation Date:", results.creation_date)
  print(Fore.CYAN + Style.BRIGHT + "Expiration Date:", results.expiration_date)
  print(Fore.CYAN + Style.BRIGHT + "Server:", results.name_server)
  print(Fore.CYAN + Style.BRIGHT + "Whois Server:", results.whois_server)
  print(Fore.CYAN + Style.BRIGHT + "Email", results.email)
  print(Fore.CYAN + Style.BRIGHT + "DNSSec:", results.dnssec)
  print(Fore.CYAN + Style.BRIGHT + "Name:", results.name)
  print(Fore.CYAN + Style.BRIGHT + "Organization:", results.org)
  print(Fore.CYAN + Style.BRIGHT + "Adress:", results.address)
  print(Fore.CYAN + Style.BRIGHT + "City:", results.city)
  print(Fore.CYAN + Style.BRIGHT + "State:", results.state)
  print(Fore.CYAN + Style.BRIGHT + "Postal Code:", results.registrant_postal_code)
  print(Fore.CYAN + Style.BRIGHT + "Country:", results.country)
  print(Fore.CYAN + Style.BRIGHT + "IP Address:", socket.gethostbyname(domaine))
  print("┌── Do you want to check a new domain ? (Y/n) ")
  restart = input("└───➤ WhoisChecker@User ")
  if restart == "Y":
        main()
  elif restart == "y":
        main()
  else:
        sys.exit()
 main()

def RobotsViewer():
 banner = """
██████╗  ██████╗ ██████╗  ██████╗ ████████╗███████╗████████╗██╗  ██╗████████╗    ██╗   ██╗██╗███████╗██╗    ██╗███████╗██████╗ 
██╔══██╗██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝╚══██╔══╝╚██╗██╔╝╚══██╔══╝    ██║   ██║██║██╔════╝██║    ██║██╔════╝██╔══██╗
██████╔╝██║   ██║██████╔╝██║   ██║   ██║   ███████╗   ██║    ╚███╔╝    ██║       ██║   ██║██║█████╗  ██║ █╗ ██║█████╗  ██████╔╝
██╔══██╗██║   ██║██╔══██╗██║   ██║   ██║   ╚════██║   ██║    ██╔██╗    ██║       ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝██████╔╝╚██████╔╝   ██║   ███████║██╗██║   ██╔╝ ██╗   ██║        ╚████╔╝ ██║███████╗╚███╔███╔╝███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝╚═╝   ╚═╝  ╚═╝   ╚═╝         ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝
                                                                                                                               


"""

 def main():
   print(Fore.RED + Style.NORMAL + banner)
   print(Fore.WHITE + "┌── Please enter an URL (Example: https://example.com)")
   lien = input("└───➤ Robots.txtViewer@User ")
   urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
   robots = (lien + "/robots.txt")
   reponse = requests.get(robots, verify=False)
   if reponse.status_code == 200:
    print(Fore.BLUE + reponse.text)
   elif reponse.status_code == 404:
    print(Fore.LIGHTRED_EX + "[I] Error 404")
   else:
    print(Fore.LIGHTRED_EX + "[I] Error")
   print("┌── Do you want to view a new robots.txt ? (Y/n) ")
   restart = input("└───➤ RobotTXTViewer@User ")
   if restart == "Y":
        main()
   elif restart == "y":
        main()
   else:
        sys.exit()
 main()


def IdentityGen():
 banner = """
██╗██████╗ ███████╗███╗   ██╗████████╗██╗████████╗██╗   ██╗     ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
██║██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██║╚══██╔══╝╚██╗ ██╔╝    ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██║██║  ██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║    ╚████╔╝     ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
██║██║  ██║██╔══╝  ██║╚██╗██║   ██║   ██║   ██║     ╚██╔╝      ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
██║██████╔╝███████╗██║ ╚████║   ██║   ██║   ██║      ██║       ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝   ╚═╝      ╚═╝        ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                                                                                            
                                                                                                                                                                                                                            

"""


 def main():
  fake = Faker()



  print(Fore.RED + banner)


  print(Fore.GREEN + "[+] IPV4 (Public): " + fake.ipv4_public())
  print(Fore.GREEN + "[+] Address: " + fake.address())
  print(Fore.GREEN + "[+] Name: " + fake.name())
  print(Fore.GREEN + "[+] Male Name: " + fake.name_male())
  print(Fore.GREEN + "[+] Female Name: " + fake.name_female())
  print(Fore.GREEN + "[+] Non Binary Name: " + fake.name_nonbinary())
  print(Fore.GREEN + "[+] City: ", fake.city())
  print(Fore.GREEN + "[+] Date Of Birth: ", fake.date_of_birth())
  print("┌── Do you want to generate a new identity ? (Y/n) ")
  restart = input("└───➤ IdentityGenerator@User ")
  if restart == "Y":
        main()
  elif restart == "y":
        main()
  else:
        sys.exit()
 main()




def UsrChecker():
 banner = r"""

██╗   ██╗███████╗███████╗██████╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██║   ██║██╔════╝██╔════╝██╔══██╗    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║   ██║███████╗█████╗  ██████╔╝    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██║   ██║╚════██║██╔══╝  ██╔══██╗    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
╚██████╔╝███████║███████╗██║  ██║    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
 ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                             

 
"""
 def main():
  print(Fore.RED + Style.NORMAL + banner)
 
  print("┌── Please enter an username")
  username = input("└───➤ ")


  print("Searching...")

  youtube = requests.get("https://youtube.com/@" + username)
  if youtube.status_code == 200:
    print(Fore.GREEN + Style.NORMAL + "[+] YouTube")
  elif youtube.status_code == 404:
    print(Fore.RED + Style.NORMAL +"[-] YouTube")

  github = requests.get("https://github.com/" + username)
  if github.status_code == 200:
    print(Fore.GREEN + Style.NORMAL + "[+] GitHub")
  elif github.status_code == 404:
    print(Fore.RED + Style.NORMAL +"[-] GitHub")
  print("┌── Do you want to check a new user ? (Y/n) ")
  restart = input("└───➤ UserChecker@User ")
  if restart == "Y":
        main()
  elif restart == "y":
        main()
  else:
        sys.exit()
 main()











# Menu

banner = r"""
    __  ___                  ___       __    __ 
   /  |/  /___  ____  ____  / (_)___ _/ /_  / /_
  / /|_/ / __ \/ __ \/ __ \/ / / __ `/ __ \/ __/
 / /  / / /_/ / /_/ / / / / / / /_/ / / / / /_  
/_/  /_/\____/\____/_/ /_/_/_/\__, /_/ /_/\__/  
                             /____/                   
"""
moonlight = r"""                                     
           ##***+++++++                          
         %%##*****##                              
       @%%#**++**                                 
      @@%#**+++                                   
     @@%#**+++                                    
     @@%#*+++                                     
    @@@%#*+++                                     
    @@@%#**++                                     
     @@@%#*+++                #++                 
     @@@@%#**+++             #**+                 
      @@@%%#***++++       ******                  
       @@@@%%##**+++++++****###                   
         @@@%%%%%############                     
           @@@@@@%%%%%%%%%%                       
               @@@@@@                            
                                                              
"""
print(Fore.RED + Style.BRIGHT + banner)
print(Fore.RED + Style.BRIGHT + moonlight)
print(Fore.RED + Style.BRIGHT + "┌── Main Menu")
print(Fore.RED + Style.BRIGHT + "⏐ 1 - Password Maker")
print(Fore.RED + Style.BRIGHT + "⏐ 2 - IP Lookup")
print(Fore.RED + Style.BRIGHT + "⏐ 3 - IP Generator")
print(Fore.RED + Style.BRIGHT + "⏐ 4 - Phone Checker")
print(Fore.RED + Style.BRIGHT + "⏐ 5 - Whois Checker")
print(Fore.RED + Style.BRIGHT + "⏐ 6 - Robots.txt Viewer")
print(Fore.RED + Style.BRIGHT + "⏐ 7 - Identity Generator")
print(Fore.RED + Style.BRIGHT + "└─── 8 - User Checker")
print(Fore.RED + Style.BRIGHT + "┌── Please enter your choice")
choice = input(Fore.RED + Style.BRIGHT + "└───➤ Moonlight@User ")
if choice == "1":
 PasswordMaker()
if choice == "2":
   IPLookup()
if choice == "3":
    IPGenerator()
if choice == "4":
    PhoneChecker()
if choice == "5":
    WhoisChecker()
if choice =="6":
    RobotsViewer()
if choice == "7":
 IdentityGen()
if choice == "8":
 UsrChecker()

