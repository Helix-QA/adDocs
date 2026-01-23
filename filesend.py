import requests
import sys

path = sys.argv[1]
nameFile = sys.argv[2]

TOKEN = "7117726988:AAFJFXz3rF7XyNXK23vtcy6MQG1E9x3DmRc"
CHAT_ID = "-1002167629740"
FILE_PATH = rf"{path}\{nameFile}"

url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
with open(FILE_PATH, 'rb') as file:
    response = requests.post(url, data={"chat_id": CHAT_ID}, files={"document": file})
print(response.json())