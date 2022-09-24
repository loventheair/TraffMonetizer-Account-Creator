from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys
import mysql.connector
import paramiko

while True:
    try:
        # Check if system have new account
        mydb = mysql.connector.connect(
            host="byte.rasbyte.net",
            user="admin_omer",
            password="@But@!ib$iriy3v200311",
            database="admin_omer"
        )
        try:
            mycursor = mydb.cursor()
        except Exception as db_error:
            print(f"MySQL Connection Error: {db_error}")

        sql = "SELECT COUNT(1) FROM traff_new WHERE need_new = 'False'"
        mycursor.execute(sql)

        if mycursor.fetchone()[0]:

            # Create browser and  go to website
            browser = webdriver.Firefox()
            browser.get("https://app.traffmonetizer.com")

            # Connect to mysql
            mydb = mysql.connector.connect(
                host="byte.rasbyte.net",
                user="admin_omer",
                password="@But@!ib$iriy3v200311",
                database="admin_omer"
            )
            try:
                mycursor = mydb.cursor()
            except Exception as db_error:
                print(f"MySQL Connection Error: {db_error}")

            # Get account information's from database
            sql = "SELECT * FROM traff_new"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            for informations in myresult:
                print(informations)


            # Login to Account and check balance
            WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/section/div[2]/zoog-auth/section/div/div/div[1]/zoog-sign-in/form/div[1]/div/input"))).send_keys(informations[2])
            WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/section/div[2]/zoog-auth/section/div/div/div[1]/zoog-sign-in/form/div[2]/div[1]/input"))).send_keys(informations[3])
            time.sleep(5)
            WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/section/div[2]/zoog-auth/section/div/div/div[1]/zoog-sign-in/form/button"))).click()
            time.sleep(5)
            browser.refresh()
            balance = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/section/div[2]/app-dashboard/div/div/div/div[2]/dashboard-current-balance/div/div/p"))).text
            new_balance = balance.replace("$", "")
            if int(new_balance) >= 10:
                try:
                    # Connect to mysql
                    mydb = mysql.connector.connect(
                        host="byte.rasbyte.net",
                        user="admin_omer",
                        password="@But@!ib$iriy3v200311",
                        database="admin_omer"
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
                        _stdin, _stdout, _stderr = client.exec_command("docker rm -f $(docker ps -qf 'name=TraffMonetizer_')")
                        print(_stdout.read().decode())
                        client.close()

                    # Connect to mysql
                    mydb = mysql.connector.connect(
                        host="byte.rasbyte.net",
                        user="admin_omer",
                        password="@But@!ib$iriy3v200311",
                        database="admin_omer"
                    )
                    try:
                        mycursor = mydb.cursor()
                    except Exception as db_error:
                        print(f"MySQL Connection Error: {db_error}")

                    # Get account information's from database
                    sql = "SELECT * FROM traff_new"
                    mycursor.execute(sql)
                    myresult = mycursor.fetchall()
                    for traff_acc in myresult:
                        print(traff_acc)


                    # Add account to old accounts list
                    sql = "INSERT INTO traff_old (token, need_new, email, password) VALUES (%s, %s, %s, %s)"
                    val = (f"{traff_acc[0]}", f"{traff_acc[1]}", f"{traff_acc[2]}", f"{traff_acc[3]}")
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print(mycursor.rowcount, "record inserted.")

                    # replace new account need alert with True
                    #                    sql = "update traff_new set need_new=replace(need_new,'False','True');"
                    #                    mycursor.execute(sql)
                    #                    mydb.commit()
                    #                    print(mycursor.rowcount, "record inserted.")

                    # Delete old record
                    sql = "DELETE FROM traff_new WHERE need_new = 'True'"
                    mycursor.execute(sql)
                    mydb.commit()
                    print(mycursor.rowcount, "record(s) deleted")

                except Exception as error:
                    print(f"Error: {error}")
                    os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                print("Balance not equals to 10$")
                time.sleep(600)
                os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            time.sleep(60)
            os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as error:
        print(f"Error: {error}")
        os.execl(sys.executable, sys.executable, *sys.argv)