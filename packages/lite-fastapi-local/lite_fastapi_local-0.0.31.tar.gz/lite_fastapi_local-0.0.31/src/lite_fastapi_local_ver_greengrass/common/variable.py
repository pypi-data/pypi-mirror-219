class Common():
    def __init__(self):
        self.currnet_device_data = {}
        self.MACHINE_MAC = ""
        self.is_cctv_stop = False
        self.count_max = 0
        self.current_count = 0
        self.operating_status = "wait"
        self.use_inner_camera = False
        self.use_cctv_camera = False
        self.file_path = str()
        self.person_count = 0
        self.camera_inner_index = -1
        self.camera_cctv_index = -1
        self.lider_sensor_port = ""
        self.image_directory = ""
        self.uploading_videos = []
        self.returned_qr_code_list = []

    def get_current_device_data(self):
        return self.current_device_data
    
    def set_current_device_data(self, data):
        self.current_device_data = data

    def get_MACHINE_MAC(self):
        return self.MACHINE_MAC
    
    def set_MACHINE_MAC(self, mac):
        self.MACHINE_MAC = mac

    def get_is_cctv_stop(self):
        return self.is_cctv_stop
    
    def set_is_cctv_stop(self, bool):
        self.is_cctv_stop = bool
    
    def get_count_max(self):
        return self.count_max
    
    def set_count_max(self, count_max):
        self.count_max = count_max
    
    def get_current_count(self):
        return self.current_count
    
    def set_current_count(self, current_count):
        self.current_count = current_count

    def get_operating_status(self):
        return self.operating_status
    
    def set_operating_status(self, status):
        self.operating_status = status

    def get_use_inner_camera(self):
        return self.use_inner_camera
    
    def set_use_inner_camera(self, bool):
        self.use_inner_camera = bool

    def get_use_cctv_camera(self):
        return self.use_cctv_camera
    
    def set_use_cctv_camera(self, bool):
        self.use_cctv_camera = bool

    def get_file_path(self):
        return self.file_path
    
    def set_file_path(self, path):
        self.file_path = path

    def get_person_count(self):
        return self.person_count

    def set_person_count(self, count):
        self.person_count = count

    def get_camera_inner_index(self):
        return self.camera_inner_index

    def set_camera_inner_index(self, index):
        self.camera_inner_index = index
        
    def get_camera_cctv_index(self):
        return self.camera_cctv_index

    def set_camera_cctv_index(self, index):
        self.camera_cctv_index = index
        
    def get_lidar_sensor_port(self):
        return self.lider_sensor_port
    
    def set_lidar_sensor_port(self, port):
        self.lider_sensor_port = port
    
    def get_image_directory(self):
        return self.image_directory
    
    def set_image_directory(self, directory):
        self.image_directory = directory
        
    def get_uploading_videos(self):
        return self.uploading_videos
    
    def add_uploading_videos(self, uploading_video):
        self.uploading_videos.append(uploading_video)
        
    def delete_uploading_videos(self, uploading_video):
        self.uploading_videos.remove(uploading_video)
        
    def get_returned_qr_code_list(self):
        return self.returned_qr_code_list
    
    def add_returned_qr_code_list(self, qr_code):
        self.returned_qr_code_list.append(qr_code)
        
    def clear_returned_qr_code_list(self):
        self.returned_qr_code_list = []

common = Common()