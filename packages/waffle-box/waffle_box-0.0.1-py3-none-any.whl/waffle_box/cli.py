import typer
from typing_extensions import Annotated

app = typer.Typer()

# subcommand에 option 값 전달을 위한 dictionary
options = {
    'dx_target_version': '1.6.2',
    'gpu_num': 0,
}

@app.command('convert')
def cli_make_new_app(input: Annotated[str, typer.Argument(help="Base app file.")], 
                     output: Annotated[str, typer.Option('-O', help="Output app file.")], 
                     queit: Annotated[bool, typer.Option(help="Do not print anything.")] = False):
    """
    Make a new app from base app with input models.
    """
    print(f'waffle box convert: dx_version {options["dx_target_version"]}, input-{input}, output-{output}')
    # 1. input, output 검증
    # 2. 이미지 확인
    # 2.1 이미지가 없다면 사용자에게 안내하고 종료
    # 3. input app parsing
    # 4. 사용자에게 input app에서 교체할 모델 질의
    # 5. 모델 변환
    # 6. App packaging

@app.command('bake')
def cli_convert_onnx_to_engine(input: Annotated[str, typer.Argument(help="ONNX model input file.")], 
                               output: Annotated[str, typer.Option('-O', help='TensorRT engine output file.')], 
                               queit: Annotated[bool, typer.Option(help="Do not print anything.")] = False):
    """
    Convert ONNX file to TensorRT engine file.
    """
    print(f'waffle box bake: dx_version {options["dx_target_version"]}, input-{input}')

@app.command('pull')
def cli_pull_waffle_maker_image(login: Annotated[bool, typer.Option(help="Login to docker hub.")] = False, 
                                queit: Annotated[bool, typer.Option(help="Do not print anything.")] = False):
    """
    Pull waffle maker image.
    """
    print(f'waffle box pull maker image for dx version {options["dx_target_version"]}')

@app.callback()
def main(dx_target_version: Annotated[str, typer.Option('--dx-version', 
                                                        help='Target Autocare-D version.')] = '1.6.2',
         gpu_num: Annotated[int, typer.Option('-G', help='GPU number to use.')] = 0):
    if dx_target_version:
        options['dx_target_version'] = dx_target_version
    
    options['gpu_num'] = gpu_num

if __name__ == '__main__':
    app()
