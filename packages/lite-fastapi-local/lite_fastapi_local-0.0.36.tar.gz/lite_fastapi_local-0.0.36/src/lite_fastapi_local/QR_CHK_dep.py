import time
import json
import requests


url = "https://9dp6syjuif.execute-api.ap-northeast-2.amazonaws.com/220623/qr_chk/?scan_in="

payload={}
headers = {}


def QR_CHK(scan_in:str):

    start = time.perf_counter()
    response = requests.request("GET", url+scan_in, headers=headers, data=payload)
    end = time.perf_counter()
    
    print(response)
    print(response.text)
    
    if response.status_code != 200:
        result = False
        
    else:
        print(type(response.text))    
        result =json.loads(json.loads(response.text))
        #print(result)
        #print(type(result))
        
        deposit = result['DEPOSIT']
        count = result['RESULT']
        #print(type(count))    
        #print(type(deposit))
        
    res = {'RESULT': count, 'DEPOSIT':deposit, 'DURATION':end - start}
    
    #print(res)    
    #print(type(res))
    return json.dumps(res)


#test code - DynamoDB에 속성유무 확인
#QR_CHK(scan_in='KRAB2010122061000016')
#res = QR_CHK(scan_in='asdfgrgdf344123456sdffs')
#print(res)
