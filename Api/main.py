from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

app = Flask(__name__)

Url = "https://officegpt.chat"
XPATH_input = "/html/body/div[1]/div/div/div/main/article/div/div[3]/div/div/div[2]/div/textarea"
XPATH_output = "/html/body/div[1]/div/div/div/main/article/div/div[3]/div/div/div[1]/div[3]/span[2]"
Ask_Summary = "Summarize this text : "
Waiting_Period = 3
Max_Attempts = 20

def Open_Connection():
  options = ChromeOptions()
  options.add_argument("--headless")
  options.add_argument("--disable-gpu")
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  driver = webdriver.Chrome(options=options)
  driver.get(Url)
  return driver

def Send_Question(driver,Question):
    Textbox = driver.find_element(By.XPATH, XPATH_input)
    Textbox.send_keys(Question)
    Textbox.send_keys(Keys.RETURN)

def Get_Reply(driver):
    elements = None
    Attempts = 0
    while not elements:
        try: elements = WebDriverWait(driver, Waiting_Period).until(EC.presence_of_element_located((By.XPATH, XPATH_output)))
        except:
            Attempts += 1
            if Cancel_Task(Attempts): return Error_Json("Server is not responding")
    return Format_Reply(elements)

def Format_Reply(elements):
   HTML_Format = elements.get_attribute("outerHTML")
   HTML_Tags = re.compile('<.*?>')

   Summary = re.sub(HTML_Tags,'', HTML_Format)
   return jsonify({"Reply": Summary})

def Error_Json(ErrorText):
    return jsonify({"Eror": ErrorText})

def Cancel_Task(Attempts):
    return True if Attempts >= Max_Attempts else False


@app.route("/")
def Home():
    return jsonify({"Any question":"./your question " ,"Summarize text":"./summarize/your text" })

@app.route("/<Question>")
def Ask(Question):
  try:
    driver = Open_Connection()
    Send_Question(driver,Question)
    Reply = Get_Reply(driver)
    driver.close()
    return Reply
  except: 
    return Error_Json("Something went wrong")

@app.route("/summarize/<text>")
@app.route("/summarize/")
@app.route("/summarize")
def summarize(text = ""):
    return Ask((Ask_Summary + text)) if text else Error_Json("you most submit a value in the link")
  
if __name__ == '__main__':
  app.run(host='0.0.0.0')