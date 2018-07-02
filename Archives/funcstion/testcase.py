# def tkinter_prompt():
#     global userentry, pwentry
#
#     def printtext():
#         username = userentry.get()
#         password = pwentry.get()
#         print "Username: " + username + "| Password: " + password
#
#     root = Tk()
#     root.title('Login Prompt')
#
#     Label(root, text="UserName").grid(row=0)
#     Label(root, text="Password").grid(row=1)
#
#     userentry = Entry(root)
#     userentry.grid(row=0, column=1)
#     pwentry = Entry(root, show="*")
#     pwentry.grid(row=1, column=1)
#
#     okbutton = Button(root, text='Login', command=printtext)
#     okbutton.grid(row=2, column=1)
#     root.mainloop()
# def sm9_cancel():
#     # cancel fro display
#     userinfo = WebDriverWait(firefoxdriver.driver, 10)
#     userinfo.until(ec.presence_of_element_located(
#         (By.XPATH, '//button[@aria-label="Exit Record without Saving (Alt+F3)"]'))).click()
#     WebDriverWait(firefoxdriver.driver, 40).until(
#         ec.presence_of_element_located((By.XPATH, '//iframe[contains(@title,"Display Which")]')))
#     time.sleep(2)
#     firefoxdriver.driver.switch_to.frame(
#         firefoxdriver.driver.find_element_by_xpath('//iframe[contains(@title,"Display Which")]'))
#     time.sleep(2)
#
#
# def sm9_refresh():
#     userinfo = WebDriverWait(firefoxdriver.driver, 10)
#     userinfo.until(ec.presence_of_element_located(
#         (By.XPATH, '//button[@aria-label="Refresh"]'))).click()
#     WebDriverWait(firefoxdriver.driver, 40).until(
#         ec.presence_of_element_located((By.XPATH, '//iframe[contains(@title,"Incident Queue:")]')))
#     time.sleep(2)
#     firefoxdriver.driver.switch_to.frame(
#         firefoxdriver.driver.find_element_by_xpath('//iframe[contains(@title,"Incident Queue:")]'))
#     time.sleep(2)