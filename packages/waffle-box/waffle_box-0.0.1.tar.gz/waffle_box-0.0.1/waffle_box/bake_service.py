from maker_manager import MakerManager, ONNXConvConfigs

from pathlib import Path

class BakeService:
    def __init__(self, workspace: Path, input: Path, output: Path, dx_target_version: str, gpu_num: int) -> None:
        self.workspace: Path = workspace
        self.origin_model_path: Path = input
        self.final_model_path: Path = output

        # TODO: make image tag converter
        self.img_tag = 'snuailab/trt:8.5.2.2'

        self.maker_manager = MakerManager(self.img_tag, gpu_num=gpu_num)
    
    def is_local_maker_installed(self) -> bool:
        return self.maker_manager.check_image_exist_at_local()
    
    def convert_model(self, print_output: bool, precision: str) -> None:
        onnx_config = ONNXConvConfigs(precision=precision)
        self.maker_manager.convert_onnx_to_engine_at_local(input=self.origin_model_path, 
                                                  output=self.final_model_path,
                                                  convert_config=onnx_config, 
                                                  print_output=print_output)
