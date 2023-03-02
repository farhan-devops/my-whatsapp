from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import filedialog
from tkinter import *
import pyperclip
from time import sleep
import sys

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()

def get_num():
    #Get the file path of numbers
    num_file = filedialog.askopenfilename(initialdir="C:/Users", title="Select the number list")
    
    if not num_file:
        print("Sorry, You have not selected any numbers.")
        exit()
    
    n = open(num_file, "r", encoding="utf-8")
    number_list = n.read().splitlines()
    n.close()
    number_list = [i for i in number_list if i] # remove empty lines from the list

    num_of_contacts = len(number_list)
    
    print(f"The total Numbner of contacts is: {num_of_contacts}")

    return(number_list)

def get_msg():
    #Get the file path of message
    msg_file = filedialog.askopenfilename(initialdir="C:/Users", title="Select the message")

    if not msg_file:
        print("No message is selected")
        message = "BSOFT"

    else:
        m = open(msg_file, "r", encoding="utf-8")
        message = m.read()
        m.close()
        print(message)
        
    return(message)

def get_image():
    img_name = filedialog.askopenfilename(initialdir="C:/Users", title="Select image")

    if not img_name:
        img_name = ""

    return(img_name)

contacts_list = get_num()

msg = get_msg()
pyperclip.copy(msg)

image = get_image()

driver.get("https://web.whatsapp.com/")

sleep(5)

confirm = Tk()
confirm.title("BSOFT - Auto Whatsapp")
confirm.geometry("500x180")
confirm.configure(bg="gray")
confirm.eval('tk::PlaceWindow . center')

def close_win():
    confirm.destroy()

msg = Label(confirm, text="After logging in to whatsapp.web, please click on Ok to confirm", bg="gray")
msg.pack(pady=30)
btn = Button(confirm, text="Ok", width=9, font=("Arial", 12), bg="#2856d4", fg="white", command=close_win)
btn.pack(pady=30)

confirm.mainloop()

success_list = 0
failed_num = []

for number in contacts_list:
    try:

        print(f"sending message to {number}")

        url = 'https://web.whatsapp.com/send?phone=' + number
        driver.get(url)

        msg_box = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')))
        msg_box.send_keys(Keys.CONTROL + "v")
        
        sleep(5)

        send = driver.find_element(By.XPATH, "//button[@data-testid='compose-btn-send']")
        send.click()

        sleep(5)

        if image != "":

            attach_btn = driver.find_element(By.XPATH, "//div[@title='Attach']")
            attach_btn.click()

            sleep(2)

            image_input = driver.find_element(By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
            image_input.send_keys(image)

            sleep(5)

            image_send = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']")))
            image_send.click()

            sleep(10)

        success_list += 1
    
    except:
        print(f"{number} does not have whatsapp")
        failed_num.append(number)
        continue

driver.close()
print(f"Sucessfully send messages to {success_list} contacts")
print("Failed to send messages to the following numbers:")
print(*failed_num, sep = "\n")
sys.exit("Thank you")