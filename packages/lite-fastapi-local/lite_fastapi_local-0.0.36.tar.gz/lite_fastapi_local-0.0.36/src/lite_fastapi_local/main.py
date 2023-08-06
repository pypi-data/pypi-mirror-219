from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse, Response, FileResponse
from fastapi_utils.tasks import repeat_every

import asyncio, json, subprocess, sys, os, time, shutil, threading, requests, uvicorn
import lite_fastapi_local.QR_CHK_dep as CHKF

from lite_fastapi_local.common.variable import common
from lite_fastapi_local.common.function import find_camera_index_list, save_cctv, find_camera_index, find_lidar_sensor_port_number, upload_video_to_s3
from lite_fastapi_local.settings import Logger, mqtt
from lite_fastapi_local.router import setupRouter, motorRouter, sensorRouter
from lite_fastapi_local.model.motorModel import motor
from lite_fastapi_local.model.ledModel import led


app = FastAPI()
app.include_router(setupRouter.router)
app.include_router(motorRouter.router)
app.include_router(sensorRouter.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

mqtt.init_app(app)

# aws_iot_subscribe('sdk/test/python', on_message_received)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    # mqtt.client.subscribe('tg/C8F09E12C7D8/event') #subscribing mqtt topic
    print('Connected: ', client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print('message: ', client, topic, payload, properties)
    last_topic = topic.split('/')[2]
    if last_topic == 'state':
        pass
    elif last_topic == 'event':
        data = json.loads(payload.decode())
        common.set_count_max(data['qr_valid_count_max'])
        common.set_current_count(data['qr_valid_count'])
    elif last_topic == 'sendVideo':
        filepath_date = data['date']
        video_name = data['video_name']
        uploading_videos = common.get_uploading_videos()
        if video_name in uploading_videos():
            return
        root_dir = 'Save_file'
        data = json.loads(payload.decode())
        upload_video_thread = threading.Thread(target=upload_video_to_s3, args=[f'{root_dir}/{filepath_date}/cctv/{video_name}'])
        upload_video_thread.start()
    elif last_topic == 'updateFunction':
        subprocess.call([r'update.bat'])

# @mqtt.subscribe('tg/+/state')
# async def message_to_topic(client, topic, payload, qos, properties):
#     data = json.loads(payload.decode())
#     if 'door' in data:
#         common.set_operating_status(data['door'])
    
#     if 'sol2' in data:
#         # if data['sol2'] == 'off'
#         #     led.turn_off_led()
#         common.set_operating_status(data['sol2'])

# @mqtt.subscribe('tg/+/event')
# async def message_to_topic(client, topic, payload, qos, properties):
#     data = json.loads(payload.decode())
#     common.set_count_max(data['qr_valid_count_max'])
#     common.set_current_count(data['qr_valid_count'])
#     mac = common.get_MACHINE_MAC()
#     if mac:
#         return
#     common.set_MACHINE_MAC(data['MAC'])
    
    # aws_iot_subscribe(f'tg/iot/{mac}/sendVideo', send_data_to_s3_topic)
    # print('get mac address!')
    
@mqtt.subscribe("tg/+/event")
async def message_to_topic(client, topic, payload, qos, properties):
    if common.get_MACHINE_MAC():
        return
    data = json.loads(payload.decode())
    mqtt.client.subscribe(f"tg/{data['MAC']}/#")
    common.set_MACHINE_MAC(data["MAC"])
    mqtt.client.unsubscribe("tg/+/event")
    print('get mac address!!')
    
@app.get('/', response_class=PlainTextResponse)
def read_root():
    common.clear_returned_qr_code_list()
    return 'THE GREET'

@app.get('/QR_READ', response_class=PlainTextResponse)
def QR_READ():
    #print(os.getcwd())
    scan_in = subprocess.run(args=[sys.executable,'QR_READ_dep.py'], capture_output=True, text=True)
    # Working_Dir CHK : cwd / , cwd= 'D:\\python\DEP_SEC'
    scan_out = scan_in.stdout
    print('LINE:'+scan_out[:len(scan_out)-1])
    return scan_out[:len(scan_out)-1]

@app.get('/QR_CHK/{scan_in}')   #int 자료형 차후 Modeling
def QR_CHK(scan_in):
    print(scan_in)

    result = json.loads(CHKF.QR_CHK(scan_in=scan_in))
    return result

@app.get('/QR_END', response_class=PlainTextResponse)   #QR_READ 종료
def QR_END():
    print(os.getcwd())
    subprocess.run(args=[sys.executable,'QR_END_dep.py'], capture_output=True, text=True)        
    return 'QR_END'

@app.get('/update')
def update_server():
    subprocess.call([r'update.bat'])
    
@app.get('/img')
def get_file():
    image_directory = common.get_image_directory
    if image_directory:
        return FileResponse(path=image_directory)
    content = {
        'code_number': 27,
        'code_name': 'no_image',
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)

@app.get('/cctvVideo')
def get_cctv_video_list():
    videos = {}
    root_dir = 'Save_file'
    folders = os.scandir(root_dir)
    for dir in folders:
        if dir.is_dir():
            videos[dir.name] = os.listdir(f'{root_dir}/{dir.name}/cctv')
    content = {
        'code_number': 10,
        'code_name': 'success',
        'videos': videos
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)

# @app.get('/cctvVideo/{video_name}')
# def upload_cctvVideo(video_name: str, date: str):
#     uploading_videos = common.get_uploading_videos()
#     print(uploading_videos)
#     if video_name in uploading_videos:
#         content = {
#             'code_number': 222,
#             'code_name': 'uploading'
#         }
#         return JSONResponse(status_code=status.HTTP_200_OK, content=content)
#     root_dir = 'Save_file'
#     s3 = s3_connection()
#     mac = common.get_MACHINE_MAC()
#     capture_image_thread = threading.Thread(target=upload_video_to_s3, args=['1234', f'{root_dir}/{date}/cctv/{video_name}', 'lite-image-storage-bucket', s3])
#     # upload_video_to_s3('1234', f'{root_dir}/{date}/cctv/{video_name}', 'lite-image-storage-bucket', s3)
#     capture_image_thread.start()
#     content = {
#         'code_number': 10,
#         'code_name': 'success'
#     }
#     return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    

@app.on_event('startup')
def startup_event():
    camera_index_list = find_camera_index_list('HD USB Camera')
    print(find_camera_index(camera_index_list))
    camera_inner_index, camera_cctv_index = find_camera_index(camera_index_list)
    
    port = find_lidar_sensor_port_number()
    if port:
        print('find lidar port!')
        common.set_lidar_sensor_port(port)
    else:
        print('fail to find lidar port...')
    
    common.set_camera_inner_index(camera_inner_index)
    common.set_camera_cctv_index(camera_cctv_index)
    
@app.on_event('startup')
@repeat_every(seconds=60 * 60 * 2)
def delete_old_log_file():
    # print('repeat!!')
    path = 'Save_file'
    current_time = time.time()
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_dir():
                # print(entry.name)
                directory = os.path.join(path, entry.name)
                if os.stat(directory).st_mtime < current_time - 3 * 86400:
                    shutil.rmtree(directory)
                    

# @app.on_event('shutdown')
# def restart_server():
#     subprocess.call([r'update.bat'])
@app.get('/account')
async def send_post_request(BANK_CD: str, SEARCH_ACCT_NO: str, ACNM_NO: str):
    url = 'http://54.180.21.162/coocon/account'
    data = {
        'BANK_CD': BANK_CD,
        'SEARCH_ACCT_NO': SEARCH_ACCT_NO,
        'ACNM_NO': ACNM_NO
    }
    response = requests.post(url, json=data)
    json_response = response.json()
    RESP = json_response['RESP_DATA'][0]['ACCT_NM']
    return RESP
    #return response.text
    
    
@app.get('/transfer')
async def send_post_request(RCV_ACCT_NO: str, RCV_BNK_CD: str):
    mac_address = common.get_MACHINE_MAC()
    returned_qr_code_list = common.get_returned_qr_code_list()
    url = 'http://54.180.21.162/coocon/transfer'
    data = {
        'RCV_BNK_CD': RCV_BNK_CD,
        'RCV_ACCT_NO': RCV_ACCT_NO,
        'TRSC_AMT': '914',
        'accountName': '',
        'classQr': returned_qr_code_list,
        'classNum': [
            '050',
            '051'
        ],
        'mac_address': mac_address
    }
    response = requests.post(url, json=data)
    return response.json()


def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)