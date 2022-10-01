import os
import random
import string
import sys
import time
import paramiko
import mysql.connector
import pyperclip
from bs4 import BeautifulSoup
from imap_tools import MailBox, AND
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Database Information's
db_host = ""
db_user = ""
db_password = ""
database = ""

# Settings

imap_username = ""
imap_password = ""
imap_server = ""

traff_refferal_link = "https://app.traffmonetizer.com/sign-up?aff=xxxxx"
traff_password = ""
random_email_domain = "@gmail.com"
payeer_secret = ""

# Functions

def payeer_add_account_to_traff():
    try:
        browser.get("https://app.traffmonetizer.com/account/profile")
        browser.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
        time.sleep(2)
        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="inputPaymentSystem"]'))).click()
        WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-option-5"]'))).click()
        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="inputPaymentPayeerEmail"]'))).send_keys(account_name)
        WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/section/div[2]/app-account/div/div/div/app-profile/div/div/form/div[2]/button[2]"))).click()
        # WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/button[2]"))).click()                                                                            for i in range(10):
        while True:
            try:
                with MailBox(imap_server).login(imap_username, imap_password, 'INBOX') as add_payeer_mailbox:
                    for add_payeer_msg in add_payeer_mailbox.fetch(AND(from_='admin@traffmonetizer.com', seen=False)):
                        if "Confirm changes" in add_payeer_msg.subject:
                            soup_idk = BeautifulSoup(add_payeer_msg.html, "html.parser")
                            for payeer_add_link in soup_idk.findAll('a'):
                                fixed_link_idk = payeer_add_link.get('href')
                                if "https://app.traffmonetizer.com/account/profile/confirm-payment-settings/" in fixed_link_idk:
                                    # Go to link and finish connecting payment type
                                    browser.get(fixed_link_idk)

                                    mydb = mysql.connector.connect(
                                        host=f"{db_host}",
                                        user=f"{db_user}",
                                        password=f"{db_password}",
                                        database=f"{database}"
                                    )

                                    mycursor = mydb.cursor()

                                    sql = "INSERT INTO traff_new (email, password, token, need_new) VALUES (%s, %s, %s, %s)"
                                    val = (f"{random_email}", f"{traff_password}", f"{token}", "False")
                                    mycursor.execute(sql, val)
                                    mydb.commit()
                                    print(mycursor.rowcount, "record inserted.")

                                    # Connect to mysql
                                    mydb = mysql.connector.connect(
                                        host=f"{db_host}",
                                        user=f"{db_user}",
                                        password=f"{db_password}",
                                        database=f"{database}"
                                    )
                                    try:
                                        mycursor = mydb.cursor()
                                    except Exception as db_error:
                                        print(f"MySQL Connection Error: {db_error}")

                                    # Get account information's from database
                                    sql = "SELECT * FROM servers"
                                    mycursor.execute(sql)
                                    myresult = mycursor.fetchall()
                                    for servers in myresult:
                                        # Connect to servers and close traffmonetizer containers
                                        client = paramiko.client.SSHClient()
                                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                        client.connect(servers[0], username=servers[1], password=servers[2])
                                        _stdin, _stdout, _stderr = client.exec_command(f"python3 creator.py {token} {servers[3]}")
                                        print(_stdout.read().decode())
                                        client.close()


                                    while True:
                                        try:
                                            mydb = mysql.connector.connect(
                                                host=f"{db_host}",
                                                user=f"{db_user}",
                                                password=f"{db_password}",
                                                database=f"{database}"
                                            )
                                            mycursor = mydb.cursor()
                                            sql = "SELECT COUNT(1) FROM traff_new WHERE need_new = 'True'"
                                            mycursor.execute(sql)

                                            if mycursor.fetchone()[0]:
                                                print("Daemon wants new account.")
                                                browser.quit()

                                                os.execl(sys.executable, sys.executable, *sys.argv)
                                            else:
                                                print("Daemon doesn't need new account.")
                                                time.sleep(1200)
                                        except Exception as mysql_error:
                                            print(f"MySQL Error: {mysql_error}")
                                            time.sleep(1200)
            except Exception as change_mail_error:
                print(f"Change Mail Error: {change_mail_error}")
                time.sleep(5)

    except Exception as payeer_add_error:
        print(f"Payeer to Account Error: {payeer_add_error}")
        time.sleep(5)



try:
    # Generate random email
    letters = string.ascii_lowercase
    random_email = f"{''.join(random.choice(letters) for _ in range(10))}{random_email_domain}"

    browser = webdriver.Firefox()
    browser.get(traff_refferal_link)

    # Get Email element and input email in it
    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/section/div[2]/zoog-auth/section/div/div/div[1]/monetizer-sign-up/form/div[2]/div/input"))).send_keys(f"{random_email}")

    # Get password element and input password in it
    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/section/div[2]/zoog-auth/section/div/div/div[1]/monetizer-sign-up/form/div[3]/div/input"))).send_keys(f"{traff_password}")

    # Repeat password
    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/section/div[2]/zoog-auth/section/div/div/div[1]/monetizer-sign-up/form/div[4]/div/input"))).send_keys(f"{traff_password}")

    # Click Register Button
    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/section/div[2]/zoog-auth/section/div/div/div[1]/monetizer-sign-up/form/button"))).click()

    # Wait for email arrive
    for i in range(10):
        while True:
            try:
                with MailBox(imap_server).login(imap_username, imap_password, 'INBOX') as mailbox:
                    for msg in mailbox.fetch(AND(from_='admin@traffmonetizer.com', seen=False)):
                        if "Account activation" in msg.subject:
                            soup = BeautifulSoup(msg.html, "html.parser")
                            for link in soup.findAll('a'):
                                fixed_link = link.get('href')
                                if "https://app.traffmonetizer.com/activate/" in fixed_link:
                                    # Login to account and get token
                                    browser.get(fixed_link)
                                    time.sleep(3)
                                    if browser.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/mat-dialog-container/monetizer-success-verify-component/div/button"):
                                        WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/mat-dialog-container/monetizer-success-verify-component/div/button"))).click()
                                    else:
                                        if browser.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/mat-dialog-container/monetizer-error-verify-component/div/button"):
                                            WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/mat-dialog-container/monetizer-error-verify-component/div/button"))).click()

                                    # Login to account
                                    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/section/div[2]/zoog-auth/section/div/div/div[1]/zoog-sign-in/form/div[1]/div/input"))).send_keys(f"{random_email}")
                                    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/section/div[2]/zoog-auth/section/div/div/div[1]/zoog-sign-in/form/div[2]/div[1]/input"))).send_keys(f"{traff_password}")
                                    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/section/div[2]/zoog-auth/section/div/div/div[1]/zoog-sign-in/form/button"))).click()
                                    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/section/div[2]/app-dashboard/div/div/div/div[1]/dashboard-app-token/div/div/div/div/div/div/button"))).click()
                                    token = pyperclip.paste()
                                    print(f"{random_email}:{traff_password} - {token}")
                                    save_file = open("save_accounts.txt", "a")
                                    save_file.write(f"\nEmail: {random_email} | Password: {traff_password} | Token: {token}")
                                    save_file.close()
                                    browser.get("https://payeer.com/en/auth/?register=yes")
                                    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div[1]/div/div[2]/form/div[5]/input"))).send_keys(random_email)
                                    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div[1]/div/div[2]/form/button[2]"))).click()
                                    # Wait for email arrive
                                    for _ in range(10):
                                        while True:
                                            try:
                                                with MailBox(imap_server).login(imap_username, imap_password, 'INBOX') as payeer_mailbox:
                                                    for payeer_msg in payeer_mailbox.fetch(AND(from_="support@payeer.com", seen=False)):
                                                        if "Verification code" in payeer_msg.subject:
                                                            verification_code = BeautifulSoup(payeer_msg.html, 'html.parser').find_all('span')
                                                            fixed_verification_code = verification_code[2].string
                                                            WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div[2]/div/div[2]/form/div[6]/div[1]/input"))).send_keys(fixed_verification_code)
                                                            WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div[2]/div/div[2]/form/div[6]/div[2]/button"))).click()

                                                            # Clear Texts

                                                                # Clear First Password
                                                            WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/div[5]/input"))).send_keys(Keys.CONTROL + "a")
                                                            WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/div[5]/input"))).send_keys(Keys.DELETE)
                                                            WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/div[5]/input"))).send_keys(traff_password)

                                                                # Clear Second Password
                                                            WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/div[6]/input"))).send_keys(Keys.CONTROL + "a")
                                                            WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/div[6]/input"))).send_keys(Keys.DELETE)
                                                            WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/div[6]/input"))).send_keys(traff_password)

                                                                # Clear Secret Code
                                                            WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/div[7]/input"))).send_keys(Keys.CONTROL + "a")
                                                            WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/div[7]/input"))).send_keys(Keys.DELETE)
                                                            WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/div[7]/input"))).send_keys(payeer_secret)

                                                            # Get Account name

                                                            account_name = WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/div[8]/input"))).get_attribute('value')
                                                            print(account_name)

                                                            # Click Button
                                                            WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/button[2]"))).click()

                                                            # Type Name
                                                            while True:
                                                                time.sleep(5)
                                                                try:
                                                                    if browser.find_elements(By.XPATH, "/html/body/div[2]/main/div/div[2]/form/div[7]/div/select"):
                                                                        with open("Data/name.txt") as name:
                                                                            names = name.readlines()
                                                                            random_name = random.choice(names)

                                                                        WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/div[5]/input"))).send_keys(random_name)

                                                                        # Type Last Name

                                                                        with open("Data/name.txt") as name:
                                                                            names = name.readlines()
                                                                            random_last_name = random.choice(names)

                                                                        WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/div[6]/input"))).send_keys(random_last_name)

                                                                        # Click Button

                                                                        WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[2]/form/button[2]"))).click()

                                                                        # Print Information's

                                                                        print(f"{random_name}:{random_last_name} | {account_name}")
                                                                        save_file = open("accounts.txt", "a")
                                                                        save_file.write(f"\nEmail: {random_email} | Password: {traff_password} | Payeer: {account_name} | Token: {token}")
                                                                        save_file.close()

                                                                        payeer_add_account_to_traff()

                                                                except Exception as payeer_step3_error:
                                                                    print(f"Payeer Step 3: {payeer_step3_error}")
                                                                    time.sleep(3)

                                                        else:
                                                            print("Nothing about account activation :sad_face2:")
                                                            time.sleep(3)

                                            except Exception as payeer_mail_error:
                                                print(f"Error: {payeer_mail_error}")

                        else:
                            print("Nothing about account activation :sad_face:")
                            time.sleep(3)
            except Exception as mail_error:
                print(f"Error: {mail_error}")
except Exception as error:
    print(f"Error: {error}")
    os.execl(sys.executable, sys.executable, *sys.argv)
