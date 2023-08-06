from app_structure import ModelInfo, AppStructure

from pathlib import Path
from uuid import UUID

class AppManager:
    """ Base App을 파싱하고 새로운 App을 생성

    Base App을 파싱 후 모델을 교체해 새로운 App을 생성한다.

    # Attributes
    - workspace: Path
        - 작업할 경로
        - 일반적으로 ~/.waffle_box
    - app_structure: AppStructure
        - 작업할 App의 구조

    """
    def __init__(self, workspace: Path, app_path: Path) -> None:
        """
        # Parameters
        - workspace: Path
            - 작업할 경로
        - app_path: Path
            - Base 앱 경로
        
        # Raises
        - IOError
            - workspace를 생성할 수 없음
        - AppParsingError
            - App parsing error
        """
        self.workspace: Path = workspace

        self.app_structure: AppStructure
    
    def replace_model(self, model_id: UUID, new_model: Path) -> None:
        """ 모델의 trt 엔진 파일을 교체한다.

        입력한 id에 해당하는 모델의 trt 엔진 파일을 새로운 trt 엔진 파일로 교체한다.

        # Parameters
        - model_id
        - new_model

        # Raises
        - IOError
            - 기존 모델의 엔진 파일이 존재하지 않음
            - 새로운 모델 파일이 존재하지 않음

        """
        pass

    def package(self, output: Path) -> None:
        """ 새로운 App으로 생성한다.

        엔진 파일 교체가 끝나면 새로운 App으로 패키징한다.

        # Parameters
        - output
            - App 저장 경로
        
        # Raises
        - IOError
            - output 파일이 이미 존재함
            - output 경로에 접근 권한 없음
        """
        pass

    def get_app_structure(self) -> AppStructure:
        """ App 구조를 반환한다.
        """
        return self.app_structure
    
    def get_model_info_by_id(self, id: UUID) -> ModelInfo | None:
        """ App의 모델 정보를 id로 찾는다.

        App의 모델 정보를 id로 찾는다. 
        만약 없다면 None을 리턴한다.

        """
        return self.app_structure.find_model_by_id(id)
    
    def get_model_info_by_name(self, name: str) -> ModelInfo | None:
        """ App의 모델 정보를 이름으로 찾는다.

        App의 모델 정보를 이름으로 찾는다.
        만약 없다면 None을 리턴한다.
        """
        return self.app_structure.find_model_by_name(name)
    