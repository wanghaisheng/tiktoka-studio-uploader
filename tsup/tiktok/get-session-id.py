import requests , time , os
from colorama import Fore , init
class ExtractSessionid:
    def __init__(self):
        self.count = 0
        init(autoreset=True)
        self.green = Fore.LIGHTGREEN_EX
        self.red = Fore.LIGHTRED_EX
        self.reset = Fore.RESET
    def choice(self):
        print(f'[{self.green}+{self.reset}] 1 - Extract Sessionid From File ( account.txt )\n[{self.green}+{self.reset}] 2 - Extract Sessionid From Input\n[{self.green}+{self.reset}] Number : ', end='')
        self.number = int(input())
        if self.number == 1:
            try:
                open('account.txt').read().splitlines()
                print(f'[{self.green}+{self.reset}] Successfully Found File ( account.txt )')
                print(f'[{self.green}+{self.reset}] Sleep : ', end='')
                self.sleep = int(input())
                self.ExtractSessionidFile('account.txt', self.sleep)
            except FileNotFoundError:
                self.ExtractSessionidFile('account.txt', 0)
        elif self.number == 2:
            print(f'[{self.green}+{self.reset}] Email : ', end='')
            self.email = input()
            print(f'[{self.green}+{self.reset}] Password : ', end='')
            self.password = input()
            self.ExtractSessionidInput(self.email, self.password)
    def ExtractSessionidFile(self, file, sleep):
        try:
            for self.account in open(file).read().splitlines():
                try:
                    self.email = self.account.split(':')[0]
                    self.password = self.account.split(':')[1]
                    try:
                        self.login = requests.post("https://api2.musical.ly/passport/user/login/?mix_mode=1&username=1&email=&mobile=&account=&password=hg&captcha=&ts=&app_type=normal&app_language=en&manifest_version_code=2018073102&_rticket=1633593458298&iid=7011916372695598854&channel=googleplay&language=en&fp=&device_type=SM-G955F&resolution=1440*2792&openudid=91cac57ba8ef12b6&update_version_code=2018073102&sys_region=AS&os_api=28&is_my_cn=0&dpi=560&carrier_region=OM&ac=wifi&device_id=6785177577851504133&mcc_mnc=42203&timezone_offset=14400&os_version=9&version_code=800&carrier_region_v2=422&app_name=musical_ly&version_name=8.0.0&device_brand=samsung&ssmix=a&build_number=8.0.0&device_platform=android&region=US&aid=&as=&cp=Qm&mas=",headers={'User-Agent':'Connectionzucom.zhiliaoapp.musically/2018073102 (Linux; U; Android 9; en_AS; SM-G955F; Build/PPR1.180610.011; Cronet/58.0.2991.0)z','Host':'api2.musical.ly','Connection':'keep-alive'},data={'email':self.email,'password':self.password})
                        if 'email' in self.login.text:
                            self.count +=1
                            print(f'[{self.green}+{self.reset}] Successfully Login In {self.green}{self.count}{self.reset} Account')
                            self.sessionid = self.login.json()['data']['session_key']
                            with open('sessionidsaved.txt', 'a') as self.saved:
                                self.saved.write(f'[+] Sessionid In {self.count} Account : {self.sessionid}\n')
                            time.sleep(sleep)
                        elif 'Incorrect account or password' in self.login.text:
                            self.count +=1
                            print(f'[{self.red}+{self.reset}] Password Error In {self.green}{self.count}{self.reset} Account')
                            time.sleep(sleep)
                        elif 'Invalid Email address' or 'The account you entered does not exist.' in self.login.text:
                            self.count +=1
                            print(f'[{self.red}+{self.reset}] Email Error In {self.green}{self.count}{self.reset} Account')
                            time.sleep(sleep)
                        elif '"error_code":7' in self.login.text:
                            print(f'[{self.red}+{self.reset}] To Many Attempts , Try Again Later\n[{self.red}+{self.reset}] Press Enter To Exit')
                            time.sleep(sleep)
                    except:
                        pass
                except:
                    pass
            print(f'[{self.green}+{self.reset}] Successfully For Check All Account\n[{self.green}+{self.reset}] Press Enter To Exit')
            input()
            exit(0)
        except FileNotFoundError:
            print(f'[{self.green}+{self.reset}] Successfully Created File ( account.txt )')
            self.count_account_number = 0
            self.create_file = open('account.txt', 'a')
            print(f'[{self.green}+{self.reset}] How much do you want to enter an account : ', end='')
            self.count_account_input = int(input())
            for self.save_account in range(self.count_account_input):
                self.count_account_number +=1
                print(f'[{self.green}+{self.reset}] Account {self.count_account_number}')
                print(f'[{self.green}+{self.reset}] Email : ', end='')
                self.email = input()
                print(f'[{self.green}+{self.reset}] Password : ', end='')
                self.password = input()
                with open('account.txt', 'a') as self.create_file_save_input:
                    self.create_file_save_input.write(self.email + ':' + self.password + '\n')
                os.system("cls")
                print(f'[{self.green}+{self.reset}] 1 - Extract Sessionid From File ( account.txt )\n[{self.green}+{self.reset}] 2 - Extract Sessionid From Input\n[{self.green}+{self.reset}] Number : {self.number}')
                print(f'[{self.green}+{self.reset}] Successfully Created File ( account.txt )')
                print(f'[{self.green}+{self.reset}] How much do you want to enter an account : {self.count_account_input}')
            os.system("cls")
            print(f'[{self.green}+{self.reset}] 1 - Extract Sessionid From File ( account.txt )\n[{self.green}+{self.reset}] 2 - Extract Sessionid From Input\n[{self.green}+{self.reset}] Number : 1')
            print(f'[{self.green}+{self.reset}] Successfully Found File ( account.txt )')
            print(f'[{self.green}+{self.reset}] Sleep : ', end='')
            self.sleep = int(input())
            self.ExtractSessionidFile('account.txt', self.sleep)
    def ExtractSessionidInput(self, email, password):
        try:
            self.login = requests.post("https://api2.musical.ly/passport/user/login/?mix_mode=1&username=&email=&mobile=&account=&password=&captcha=&ts=&app_type=normal&app_language=en&manifest_version_code=2018073102&_rticket=1633593458298&iid=7011916372695598854&channel=googleplay&language=en&fp=&device_type=SM-G955F&resolution=1440*2792&openudid=91cac57ba8ef12b6&update_version_code=2018073102&sys_region=AS&os_api=28&is_my_cn=0&dpi=560&carrier_region=OM&ac=wifi&device_id=6785177577851504133&mcc_mnc=42203&timezone_offset=14400&os_version=9&version_code=800&carrier_region_v2=422&app_name=musical_ly&version_name=8.0.0&device_brand=samsung&ssmix=a&build_number=8.0.0&device_platform=android&region=US&aid=&as=&cp=Qm&mas=",headers={'User-Agent':'Connectionzucom.zhiliaoapp.musically/2018073102 (Linux; U; Android 9; en_AS; SM-G955F; Build/PPR1.180610.011; Cronet/58.0.2991.0)z','Host':'api2.musical.ly','Connection':'keep-alive'},data={'email':email,'password':password})
            if 'email' in self.login.text:
                self.sessionid = self.login.json()['data']['session_key']
                print(f'[{self.green}+{self.reset}] Successfully Login\n[{self.green}+{self.reset}] Sessionid : {self.sessionid}\n[{self.green}+{self.reset}] Press Enter To Exit')
                with open('sessionidsaved.txt', 'a') as self.saved:
                    self.saved.write(f'[+] Sessionid Input : {self.sessionid}\n')
                input()
                exit(0)
            elif 'Incorrect account or password' in self.login.text:
                print(f'[{self.red}+{self.reset}] Password Error\n[{self.red}+{self.reset}] Press Enter To Exit')
                input()
                exit(0)
            elif 'Invalid Email address' or 'The account you entered does not exist.' in self.login.text:
                print(f'[{self.red}+{self.reset}] Email Error\n[{self.red}+{self.reset}] Press Enter To Exit')
                input()
                exit(0)
            elif '"error_code":7' in self.login.text:
                print(f'[{self.red}+{self.reset}] To Many Attempts , Try Again Later\n[{self.red}+{self.reset}] Press Enter To Exit')
                input()
                exit(0)
            else:
                pass
        except:
            pass
if __name__ == '__main__':
    E = ExtractSessionid()
    E.choice()
