import cv2, os, time, boto3, json, serial, threading, requests
import numpy as np

from datetime import datetime
from pygrabber.dshow_graph import FilterGraph
from skimage.metrics import structural_similarity as ssim
from serial.tools import list_ports

from lite_fastapi_local.common.variable import common
# from settings import trigger_lambda, s3_connection


# aws
def update_cctv_list():
    mac_address = common.get_MACHINE_MAC()
    url = f"https://44qasvgllj.execute-api.ap-northeast-2.amazonaws.com/test_run/macAddress/{mac_address}"
    payload = json.dumps(get_cctv_video_list())
    requests.request("PUT", url, data=payload)
    
def send_not_opened_collection_box_image_to_s3(filename):
    mac_address = common.get_MACHINE_MAC()
    current_datetime = datetime.now().strftime("%Y-%m-%d")
    url = f'https://44qasvgllj.execute-api.ap-northeast-2.amazonaws.com/test_run/macAddress/{mac_address}/bucket/lite-image-storage-bucket/image/{filename}?datetime={current_datetime}'
    image = open(filename, 'rb')
    image_data = image.read()
    image.close()
    
    headers = {
        'Content-Type': 'image/jpeg'
    }
    response = requests.request("PUT", url=url, data=image_data, headers=headers)
    print(response.status_code)
    
def upload_multi_image_to_s3(image_name_list: dict):
    mac_address = common.get_MACHINE_MAC()
    current_datetime = datetime.now().strftime("%Y-%m-%d")
    url = f'https://44qasvgllj.execute-api.ap-northeast-2.amazonaws.com/test_run/macAddress/{mac_address}/bucket/lite-image-storage-bucket/image?datetime={current_datetime}'
    image_number = 1
    image_files = {}
    for image in image_name_list:
        with open(image, 'rb') as f:
            image_files[image.split('/')[4]] = f
    
    headers = {
        'Content-Type': 'multipart/form-data'
    }
    response = requests.request("PUT", url=url, files=image_files, headers=headers)
    print(response.status_code)
    
def upload_video_to_s3(video_name, current_datetime):
    mac_address = common.get_MACHINE_MAC()
    common.add_uploading_videos(video_name)
    print('uploading...')
    try:
        video = open(f'./Save_file/{current_datetime}/cctv/{video_name}', 'rb')
        headers = {
            'Content-Type': 'video/mp4'
        }
        url = f'https://44qasvgllj.execute-api.ap-northeast-2.amazonaws.com/test_run/macAddress/{mac_address}/bucket/lite-image-storage-bucket/media/{video_name}?datetime={current_datetime}'
        response = requests.request("PUT", url=url, data=video, headers=headers)
        print(response.status_code)
        print('uploaded!!!')
    except Exception as e:
        print(e)
    finally:
        common.delete_uploading_videos(video_name)

######################################################################################################################
def create_directory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
def find_camera_index_list(name: str):
    devices = FilterGraph().get_input_devices()
    index_list = []
    for index in range(len(devices)):
        if devices[index] == name:
            index_list.append(index)
        
    if index_list:
        return index_list
    return [0, 1]

def find_camera_index(index_list: list):
    cap = cv2.VideoCapture(index_list[0], cv2.CAP_DSHOW)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    if int(height) == 360:
        return (index_list[0], index_list[1])
    return (index_list[1], index_list[0])

def find_lidar_sensor_port_number():
    ports = list(list_ports.comports())
    for port in ports:
        string_port = str(port)
        if "Prolific" in string_port:
            return string_port[:4]
    return None

def save_cctv():
    common.set_use_cctv_camera(True)
    camera_cctv_index = common.get_camera_cctv_index()
    cctv_cap = cv2.VideoCapture(camera_cctv_index, cv2.CAP_DSHOW)
    cctv_cap.set(cv2.CAP_PROP_POS_FRAMES, 15)

    frame_width = int(cctv_cap.get(3))
    frame_height = int(cctv_cap.get(4))
    
    date_time_string = common.get_file_path()
    size = (frame_width, frame_height)
    result = cv2.VideoWriter(f'./Save_file/{date_time_string}/cctv/up_cctv_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.mp4', 
                            cv2.VideoWriter_fourcc(*'avc1'),
                            30, size)
    print("cctv start!!")
    while True:
        # 프레임 읽기
        ret, frame = cctv_cap.read()

        # 프레임이 제대로 읽혔는지 확인
        if not ret:
            print("Error: failed to capture frame")
            break
        result.write(frame)

        operating_status = common.get_operating_status()
        if operating_status =="closing":
            print("cctv end!!")
            break
    common.set_use_cctv_camera(False)

    # 작업 완료 후, 리소스 반환
    cctv_cap.release()
    cv2.destroyAllWindows()
    
    update_cctv_list()

def capture_image():
    common.set_use_inner_camera(True)
    # s3 = s3_connection()
    RESIZE_IMG = 256  #클수록 제외되는 가장자리 면적 증가 recommend:256
    is_first  = True
    up_score = 0
    is_ready = False
    ssim_score = 1
    is_opened = False
    is_opening = False
    data_name_list = []
    camera_inner_index = common.get_camera_inner_index()
    up_cap = cv2.VideoCapture(camera_inner_index, cv2.CAP_DSHOW)
    person_count = common.get_person_count()
    mac_address = common.get_MACHINE_MAC()
    date_time_string = common.get_file_path()
    while True:
        up_ret, up_frame = up_cap.read()
        if up_ret == False:
            break

        ### pre-process ###
        up_image = cv2.resize(up_frame, dsize=(RESIZE_IMG,RESIZE_IMG)) 
        operating_status = common.get_operating_status()
        if operating_status == "on" and is_opened == False:
            if ssim_score < 0.97:
                is_opening = True
            else:
                if is_opening == True:
                    print("opened")
                    is_opened = True
        if is_first == True:
            i = 0
            bf_up =  cv2.cvtColor(up_image, cv2.COLOR_BGR2GRAY)
            closed_image = cv2.cvtColor(up_image, cv2.COLOR_BGR2GRAY)
            is_first = False
            print("start!!")
        else:            
            if is_opened == True:
                (up_score, up_diff) = ssim(cv2.cvtColor(up_image, cv2.COLOR_BGR2GRAY), closed_image, full=True)
                if up_score > 0.95:
                    data = {
                        "mac_address": mac_address
                    }
                    up_filename = f'/Save_file/{date_time_string}/box/up_img_did_not_open_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.jpg'
                    cv2.imwrite(up_filename,up_frame)
                    send_not_opened_collection_box_image_to_s3(up_filename)
                is_opened = "clear"
            (up_score, up_diff) = ssim(cv2.cvtColor(up_image, cv2.COLOR_BGR2GRAY), bf_up, full=True)
            ssim_score = up_score
            print(ssim_score)
            bf_up =  cv2.cvtColor(up_image, cv2.COLOR_BGR2GRAY)            
            if (up_score)<0.95 and is_ready == True:
                i +=1
                if i > 1:
                    is_ready = False

            if i>1:
                up_ret, up_frame = up_cap.read()
                up_filename = f'./Save_file/{date_time_string}/product/up_img_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")}.jpg'
                data_name_list.append(up_filename)
                cv2.imwrite(up_filename,up_frame)
                print(i)
                if i < 8:
                    i += 1
                else:
                    if len(data_name_list) < 10:
                        common.set_image_directory(data_name_list[0])
                    i = 0
                    
            if up_score > 0.98:
                is_ready = True 

        operating_status = common.get_operating_status()
        if operating_status =="closing":
            print("end!!")
            break
    common.set_use_inner_camera(False)
    up_cap.release()                    
    cv2.destroyAllWindows()
    if data_name_list:
        upload_multi_image_to_s3(data_name_list)  
    
def get_cctv_video_list():
    videos = {}
    root_dir = 'Save_file'
    folders = os.scandir(root_dir)
    for dir in folders:
        if dir.is_dir():
            videos[dir.name] = os.listdir(f'{root_dir}/{dir.name}/cctv')
    return videos