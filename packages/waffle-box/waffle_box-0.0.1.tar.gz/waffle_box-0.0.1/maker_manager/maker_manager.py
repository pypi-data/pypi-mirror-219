from convert_option import ONNXConvConfigs

from pathlib import Path

class MakerManager:
    """ Waffle Maker Manager

    ONNX 파일을 TensorRT 엔진 파일로 변환하는 Waffle Maker를 관리하는 클래스.
    이미지 다운로드, 모델 파일 변환 등의 기능을 제공한다.

    # Attributes
    - img_tag: str
        - 실행할 이미지 태그
    - gpu_num: int
        - 컨테이너를 동작할 gpu 번호
    - container_name: str
        - 만약 동작 중 예기치못한 오류가 있을 경우 
        컨테이너를 종료시키기 위해 실행시킨 컨테이너 이름을
        저장한다.
    
    """
    def __init__(self, img_tag: str, gpu_num: int) -> None:
        """ 
        # Parameters
        - img_tag: str
            - 실행할 이미지 태그
        - gpu_num: str
            - 컨테이너를 동작할 gpu 번호

        # Raises
        - DockerDaemonError
            - Docker daemon에 접속 불가

        """
        self.img_tag = img_tag
        self.gpu_num = gpu_num

        self.container_name: str = ''
    
    def check_image_exist_at_local(self) -> bool:
        """ 로컬에 이미지가 설치되어 있는지 확인한다.

        MakerManager를 생성할 때 입력한 이미지 태그가 로컬에 존재하는지 확인한다.

        """
        return True

    def pull_image_at_local(self, print_output: bool, id: str = '', pw: str = '') -> None:
        """ 로컬에 이미지를 다운받는다.

        MakerManager를 생성할 때 입력한 이미지 태그를 로컬에 다운받는다.
        만약 id와 pw를 입력했다면 docker hub에 로그인을 한 후 다운받는다.

        # Parameters
        - id: str
            - docker hub id
            - 빈값이라면 로그인을 하지 않는다.
        - pw: str
            - docker hub password
            - 빈값이라면 로그인을 하지 않는다.

        # Raises
        - LoginError
            - id 혹은 pw가 잘못됨
        - AlreadExistError
            - 이미 이미지가 설치되어 있음

        """
        pass

    def convert_onnx_to_engine_at_local(self, input: Path, output: Path, 
                                        convert_config: ONNXConvConfigs, 
                                        print_output: bool) -> None:
        """ 입력한 모델 파일을 trt 엔진으로 변환

        입력한 모델을 컨테이너 내부에서 TensorRT 엔진으로 변환한다.
        변환한 모델은 output path에 저장한다.

        # Parameters
        - input: Path
            - 변환할 모델 경로
        - output: Path
            - 변환한 모델 저장 경로
        - convert_config: ONNXConvConfigs
            - trtexec를 실행할 때 필요한 설정값들
        - print_output: bool
            - container 출력 결과 표시 여부
        
        # Raises
        - IOError
            - input 파일일 존재하지 않음
            - output 파일이 이미 존재함
        - ConvertError
            - 변환 실패

        """
        pass
    
    def __del__(self) -> None:
        """ 실행중인 컨테이너 정리

        만약 컨테이너 실행 중 예기치 못한 종료를 하게 되었을 때
        실행중이던 컨테이너를 회수한다.
        
        """
        if self.container_name:
            pass