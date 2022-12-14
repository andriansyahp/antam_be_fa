from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.utils import ChromeType
# from time import sleep
# from urllib.parse import quote
from io import BytesIO
import pywhatkit as kit 
import os

os.environ['DISPLAY'] = ':0'
os.environ['XAUTHORITY']='/run/user/1000/gdm/Xauthority'

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# class Speech(BaseModel):
#     speech: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = file.file.read()
    buffer = BytesIO(contents)
    df = pd.read_excel(buffer)
    buffer.close()
    file.file.close()
    # df = pd.read_excel(file.file, header=0)
    
    # options = Options()
    # options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # options.add_argument("--profile-directory=Default")
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), options=options)
    # delay = 30
    # driver.get('https://web.whatsapp.com')
    
    name_phone_dict = dict(zip(df['nama'].tolist(), df['no_telp'].tolist()))
    for _, (name, phone) in enumerate(name_phone_dict.items()):
        try:
            message = "Hi" + " " + name
            phone = "+" + str(phone)
            url = 'https://web.whatsapp.com/send?phone=' + str(phone) + '&text=' + message
            sent = False
            for i in range(3):
                if not sent:
                    # driver.get(url)
                    try:
                        # click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='compose-btn-send']")))
                        kit.sendwhatmsg_instantly(str(phone), f"Assalamu'alaikum {name}", 10, True, 1)
                    except Exception as e:
                        print(f"\nFailed to send message to: {str(phone)}, retry ({i+1}/3)")
                        print("Make sure your phone and computer is connected to the internet.")
                        print("If there is an alert, please dismiss it.")
                    else:
                        # sleep(1)
                        # click_btn.click()
                        sent=True
                        # sleep(3)
        except Exception as e:
            print('Failed to send message to ' + str(phone) + str(e))
        # print(k, v)
    # driver.close()
    
    
    
    return {"filename": file.filename}