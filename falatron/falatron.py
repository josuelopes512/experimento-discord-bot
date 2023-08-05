import os
import base64
import cloudscraper
from urllib.parse import quote

class Falatron:
    def __init__(self, cf_clearance = None) -> None:
        self.scraper = cloudscraper.create_scraper()
        self.cf_clearance = cf_clearance if cf_clearance else os.getenv("FALATRON_CF_CLEARANCE")
        self.base_url = "https://falatron.com"
        
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Content-Length": "28",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://falatron.com",
            "Referer": "https://falatron.com/",
            "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188",
            "X-Requested-With": "XMLHttpRequest"
        }
    
    def request_audio(self, texto, voice="Pica Pau"):
        encoded_text = quote(texto)
        encoded_voice = quote(voice)
        cookie = f"category=Todas%20as%20vozes; voice={encoded_voice}; text={encoded_text}; cf_clearance={self.cf_clearance}"
        
        data = {
            "voz": voice,
            "texto": texto
        }
        
        headers = self.headers.copy()
        headers.update({"Cookie": cookie})
        url = f"{self.base_url}/tts"
        
        response = self.scraper.post(url, headers=headers, data=data)
        
        if response.ok:
            print("Request successful!")
            print(response.text)
            
            data_result = response.json()
            data_result.update({"cookie": cookie})
            
            return data_result
        else:
            print("Request failed!")
            print(response.status_code, response.reason)
        
        return {}
    
    def get_audio(self, task_id, cookie):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Referer": "https://falatron.com/",
            "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188",
            "X-Requested-With": "XMLHttpRequest"
        }
        headers.update({"Cookie": cookie})
        
        url = f"{self.base_url}/tts/{task_id}"
        response = self.scraper.get(url, headers=headers)
    
        if response.ok:
            data_json_res = response.json()
            
            if 'status' in data_json_res and data_json_res['status'] in ('Pendente', 'failed') or 'undefined' in data_json_res["voice"]:
                print(data_json_res['status'])
                return self.get_audio(task_id, cookie)
            
            print("Request get_voice successful!")
            
            return {"task_id": task_id, "audio": data_json_res["voice"]}
        else:
            print("Request failed!")
            print(response.status_code, response.reason)
        
        return {}
    
    def save_audio(self, uuid_name, b64file):
        if not os.path.exists("audios"):
            os.makedirs("audios")
        
        with open(f"./audios/{uuid_name}.mp3", "wb") as f:
            data = b64file.replace("data:audio/mp3;base64,", "") if "data:audio/mp3;base64," in b64file else b64file
            decode_string = base64.b64decode(data)
            f.write(decode_string)
