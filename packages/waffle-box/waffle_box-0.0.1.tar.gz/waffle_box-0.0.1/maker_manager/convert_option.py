from dataclasses import dataclass

@dataclass(frozen=True)
class ONNXConvConfigs:
    """ trt 엔진 변환을 위해 필요한 설정 값 정보

    # Attributes
    - precision
        - 모델의 precision
        - fp32, fp16, int8 중 하나
    
    """
    precision: str
