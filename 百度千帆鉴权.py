import requests
import json


def main():
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=MHxGnqfX4grPAOkoaAi0w75R&client_secret=QIteInbvmGr5PsffdG55ea5ZRG081IRY"
    
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
       
    if response.status_code == 401:  
        print(f'网络访问出错')
    

if __name__ == '__main__':
    main()
