from maker_manager import ONNXConvConfigs

from dataclasses import dataclass
from typing import List
from uuid import UUID
from pathlib import Path

@dataclass(frozen=True)
class ModelInfo:
    """ 모델 정보
    
    모델의 기본 정보를 저장한다. (변경 불가)

    # Attributes
    - id: UUID
        - model.json에 기술되어 있는 모델의 uuid
    - name: str
        - model.json에 기술되어 있는 모델의 이름
    - precision: str
        - 모델의 precision
        - fp32, fp16, int8 중 하나
    - path: Path
        - 모델 폴더 경로

    """
    id: UUID
    name: str
    precision: str
    path: Path

    def to_onnx_config(self) -> ONNXConvConfigs:
        """ ONNX 파일을 trt 엔진 파일로 변환하는데 필요한 정보

        ONNX 파일을 trt 엔진 파일로 변환하는데 
        필요한 설정 값을 모델 정보에서 얻는다.

        """
        return ONNXConvConfigs(precision=self.precision)

@dataclass(frozen=True)
class AppStructure:
    """ App 구조 정보

    App의 구조 정보를 저장한다. (변경 불가)

    # Attributes
    - id: UUID
        - app.json에 기술되어 있는 App의 UUID
    - models: List[ModelInfo]
        - App이 모델 정보 리스트
    - path: Path
        - App을 압축 푼 경로

    """
    id: UUID
    models: List[ModelInfo]
    path: Path

    def find_model_by_id(self, id: UUID) -> ModelInfo | None:
        """ id 값으로 모델을 찾는다.

        # Parameters
        - id
            - 찾는 모델의 uuid
        
        # Returns
        - ModelInfo
            - 입력한 id와 일치하는 모델
        - None
            - 입력한 id와 일치하는 모델을 찾지 못했을 때
        """
        for m in self.models:
            if m.id == id:
                return m
        
        return None

    def find_model_by_name(self, name: str) -> ModelInfo | None:
        """ 이름으로 모델을 찾는다.

        # Parameters
        - name
            - 찾는 모델의 이름
        
        # Returns
        - ModelInfo
            - 입력한 이름과 일치하는 모델
        - None
            - 입력한 이름과 일치하는 모델을 찾지 못했을 때
        """
        for m in self.models:
            if m.name == name:
                return m
        
        return None
