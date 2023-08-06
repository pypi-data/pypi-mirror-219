from app_manager import AppManager, ModelInfo, AppStructure
from maker_manager import MakerManager

from pathlib import Path
from uuid import UUID

class ConvertService:
    def __init__(self, workspace: Path, input: Path, output: Path, dx_target_version: str, gpu_num: int) -> None:
        self.workspace: Path = workspace
        self.origin_app_path: Path = input
        self.final_app_path: Path = output

        # TODO: make image tag converter
        self.img_tag = 'snuailab/trt:8.5.2.2'

        self.app_manager = AppManager(self.workspace, self.origin_app_path)
        self.maker_manager = MakerManager(self.img_tag, gpu_num=gpu_num)

        self.convert_list: dict[UUID, Path] = {}

    def is_local_maker_installed(self) -> bool:
        return self.maker_manager.check_image_exist_at_local()
    
    def get_model_info(self) -> list[ModelInfo]:
        return self.app_manager.get_app_structure.models

    def add_convert_info(self, model_id: UUID, new_model_path: Path) -> None:
        self.convert_list[model_id] = new_model_path
    
    def convert_app(self, print_output: bool) -> None:
        for id, file_path in self.convert_list.items():
            model_info = self.app_manager.get_model_info_by_id(id)

            if not model_info:
                return
            
            onnx_config = model_info.to_onnx_config()

            engine_file_path = Path('/engine_file_path')
            self.maker_manager.convert_onnx_to_engine_at_local(input=file_path, output=engine_file_path, 
                                                      convert_config=onnx_config,
                                                      print_output=print_output)
            
            self.app_manager.replace_model(id, engine_file_path)

            # remove converted files
    
    def package_app(self) -> None:
        self.app_manager.package(self.final_app_path)
