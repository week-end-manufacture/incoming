# src_dir의 파일들을 확장자 별로 정해진 작업에 따라 변환후, dst_dir에 같은 상대경로에 파일을 생성, 복사하는 파이선기반 프로그램
#   e.g. data/src_dir/dir/a/b/c.txt 를 복사할 때, data/dst_dir/dir/a/b/c.txt로 복사한다.
#   e.g. 실행시 src_dir/ 내 모든 파일들을 iso8601 날짜와 시간 포맷으로 dir을 생성하고, 그 디렉토리를    생성하여 파일을 복사 처리하는 과정을 거친다.
# CLI: brew로 설치하여 사용할 수 있도록 한다.
# (미정) GUI는 백엔드 파이선, 프론트엔드 자바스크립트로 webUI 구현. docker 컨테이너로 실행하여 유저가 브라우저로 접속하여 사용할 수 있도록 한다.
# 유저가 설정한 확장자(user_ext)별로 파일을 처리하여 dst_dir에 같은 상대경로로 복사하고 이외의 확장자는 처리과정 없이 복사한다.
# 각 확장자별 예시 처리과정은 다음과 같다.
#   '.png', '.tiff' 파일들은 pillow 라이브러리를 이용하여 손실 압축하여 '.jpg'로 변환하여 dst_dir에 저장한다.
#   '.mkv', '.mov' 파일은 handbrakecli를 이용하여 정해진 프리셋값으로 인코딩후 '.mp4' 하여 dst_dir에 저장한다.
# 각 모듈 이용하여 유저가 설정한 확장자별로 처리과정을 추가할 수 있도록 한다.
# 프로그램 관련 설정(변수등)'.json' 파일에 설정값을 저장하고 특정 확장자에 대한 처리과정 모듈 추가및 연결하여 사용할 수 있도록 한다.
#   e.g. 각종 확장자, 모듈은 json으로 유저가 확장가능하게 하고 로드하여 사용할 수 있도록 한다.
#   src_dir_path와 dst_dir_path는 유저가 설정가능하다. 
#   src_dir_path = '/Users/username/Downloads'
#   dst_dir_path = '/Users/username/Documents'
#   설정값은 프로그램 실행시 인자로 받아서 사용한다.
#   e.g. incomingdir.py --src_dir_path '/Users/username/Downloads' --dst_dir_path '/Users/username/Documents' --user_ext {'.png': 'pillow', '.tiff': 'pillow', '.mkv': 'handbrakecli', '.mov': 'handbrakecli'}
#   설정값이 없을 경우 기본값을 사용한다.
#   e.g. incomingdir.py
# 1. file.py 모듈 data/src/src_dir 


def main():
    settings = load_settings()
    src_path = settings.get('src_path')
    dst_path = settings.get('dst_path')

    print("IncomingDir")
    if src_path == dst_path:
        print("src_path와 dst_path는 같을 수 없습니다.")
        return

if __name__ == "__main__":
    main()