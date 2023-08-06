from maker_manager import MakerManager, ONNXConvConfigs

from pathlib import Path

class PullService:
    def __init__(self, dx_target_version: str) -> None:
        # Docker Hub
        self.dh_id: str = ''
        self.dh_pw: str = ''

        # TODO: make image tag converter
        self.img_tag = 'snuailab/trt:8.5.2.2'

        self.maker_manager = MakerManager(self.img_tag, gpu_num=0)
    
    def is_local_maker_installed(self) -> bool:
        return self.maker_manager.check_image_exist_at_local()
    
    def set_login_info(self, id: str, pw: str) -> None:
        self.dh_id = id
        self.dh_pw = pw
    
    def pull_image_to_local(self, print_output: bool) -> None:
        self.maker_manager.pull_image_at_local(print_output=print_output)