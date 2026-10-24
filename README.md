# incoming

`incoming`은 지정한 입력 디렉터리(또는 단일 파일)를 재귀적으로 스캔하여
이미지와 동영상은 변환하고, 압축 파일은 풀고, 그 밖의 파일은 그대로
출력 디렉터리로 복사하는 POSIX C 프로그램입니다.

- 현재 버전: **1.0.0**
- 구현 언어: C11
- 라이선스: [MIT](./LICENSE)
- 저장소: <https://github.com/week-end-manufacture/incoming>

## 주요 기능

- 입력 디렉터리의 하위 디렉터리를 재귀적으로 처리
- 이미지 변환: ImageMagick `magick` 사용, `convert`로 재시도
- 동영상 변환: HandBrakeCLI와 HandBrake 프리셋 사용
- 압축 해제: ZIP, RAR, 7z
- 알 수 없는 확장자의 파일은 변환하지 않고 그대로 복사
- 변환 결과의 확장자와 이미지 품질 설정
- 처리 결과를 더미 파일로 미리 확인하는 `--dummy` 모드
- 성공적으로 변환·복사된 원본을 삭제하는 `--unlink` 옵션
- 처리 로그 저장 및 파일별 진행률 출력

> 주의: 현재 C 구현은 이미지·동영상·압축 파일을 확장자로 분류합니다.
> 파일 내용(mime type)을 검사하지 않으므로 확장자가 올바르게 지정되어 있어야
> 합니다.

## 지원 파일 형식

### 이미지

기본 이미지 확장자는 다음과 같습니다.

`.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.tif`

이미지는 기본적으로 같은 파일 이름을 유지하면서 `.jpg`로 변환됩니다.
예를 들어 `photo.png`는 출력 디렉터리의 `photo.jpg`가 됩니다.

### 동영상

기본 동영상 확장자는 다음과 같습니다.

`.asf`, `.avi`, `.flv`, `.mkv`, `.mov`, `.mp4`, `.mpeg`, `.ts`, `.webm`,
`.wmv`, `.m4v`, `.mpg`, `.mts`, `.m2ts`, `.vob`, `.evo`

동영상은 기본적으로 `.mp4`로 변환되며, HandBrake 프리셋에 따라 인코딩됩니다.

### 압축 파일

- `.zip`: `unzip`
- `.rar`: `unrar`
- `.7z`: `7z`

압축 파일은 출력 디렉터리가 아니라 **입력 파일이 있는 디렉터리**에
`파일이름_zip`, `파일이름_rar`, `파일이름_7z` 디렉터리를 만들고 그 안에 풉니다.

### 기타 파일

지원 목록에 없는 일반 파일은 변환하지 않고 입력 디렉터리 구조를 유지한 채
출력 디렉터리로 복사합니다.

## 요구 사항

### 운영체제

POSIX API를 사용하므로 macOS 또는 Linux 계열 환경을 권장합니다.
`--settings` 옵션은 macOS의 `open` 명령을 사용해 설정 디렉터리를 열도록
구현되어 있습니다.

### 빌드 도구

- C11을 지원하는 컴파일러(`cc`, `clang`, 또는 `gcc`)
- `make`

### 실행 시 외부 명령

필요한 명령은 처리하려는 파일 형식에 따라 다릅니다.

| 기능 | 명령 |
| --- | --- |
| 이미지 변환 | `magick` 또는 `convert` (ImageMagick) |
| 동영상 변환 | `HandBrakeCLI` |
| ZIP 해제 | `unzip` |
| RAR 해제 | `unrar` |
| 7z 해제 | `7z` |

Homebrew를 사용하는 macOS에서는 다음과 같이 설치할 수 있습니다.

```sh
brew install imagemagick handbrake p7zip
```

`unzip`은 macOS에 기본 포함되어 있습니다. RAR 파일을 처리하려면 별도로
`unrar` 실행 파일을 설치해야 합니다.

## 설치

### 소스에서 빌드

```sh
git clone https://github.com/week-end-manufacture/incoming.git
cd incoming/src
make
```

빌드가 완료되면 `src/incoming` 실행 파일이 생성됩니다.

설치 경로를 지정하여 설치할 수도 있습니다.

```sh
cd src
make
sudo make install PREFIX=/usr/local
```

`PREFIX`를 지정하지 않으면 Makefile의 기본값에 따라 설치 명령이
`$(PREFIX)/bin`을 사용합니다. 시스템별 기본값을 명확히 하려면
`PREFIX=/usr/local`처럼 직접 지정하는 것을 권장합니다.

### Homebrew Formula

저장소에는 [Formula/incoming.rb](./Formula/incoming.rb)가 포함되어 있습니다.
Formula는 C 프로그램을 빌드하고 ImageMagick, HandBrake, p7zip을 의존성으로
설치합니다.

```sh
brew install --build-from-source Formula/incoming.rb
```

Formula를 통해 설치한 경우 예제 설정 파일은 Homebrew의 `share/incoming`
아래에 설치됩니다. 첫 실행 전에 다음과 같이 사용자 설정 디렉터리로
복사하십시오.

```sh
mkdir -p ~/.config/incoming
cp -R "$(brew --prefix)/share/incoming/config/"* ~/.config/incoming/
```

## 설정

프로그램은 실행할 때 다음 파일을 읽습니다.

```text
~/.config/incoming/settings.json
```

설정 파일이 없거나 아래 세 필수 키가 없으면 실행이 실패합니다.

- `src_dir_path`
- `dst_dir_path`
- `default_preset_path`

가장 간단한 설정 예시는 다음과 같습니다.

```json
{
  "src_dir_path": "/Users/you/Incoming",
  "dst_dir_path": "/Users/you/Outgoing",
  "default_preset_path": ".config/incoming/preset/preset.json"
}
```

`default_preset_path`가 `/`로 시작하면 절대 경로로 사용하고, 그렇지 않으면
`$HOME`을 앞에 붙인 경로로 해석합니다.

### 이미지·동영상 프리셋

기본 프리셋은 `default_preset_path`가 가리키는 JSON 파일입니다. `-p` 옵션을
사용하면 다음 디렉터리의 프리셋으로 기본 프리셋을 덮어씁니다.

```text
~/.config/incoming/preset/<이름>.json
```

현재 C 구현이 읽는 프리셋 키는 다음과 같습니다.

| 키 | 형식 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `image_process_toggle` | boolean | `true` | 이미지 변환 여부 |
| `video_process_toggle` | boolean | `true` | 동영상 변환 여부 |
| `output_ext` | string | `.jpg` | 이미지 출력 확장자 |
| `output_video_ext` | string | `.mp4` | 동영상 출력 확장자 |
| `remove_all_exif_data` | boolean | `false` | ImageMagick `-strip`으로 EXIF 제거 |
| `remove_only_gps_exif_data` | boolean | `false` | 현재 구현에서는 값만 읽고 별도 처리는 하지 않음 |
| `HandBrake_presets_path` | string | 없음 | HandBrake 프리셋 JSON 경로 |

이미지 품질은 코드 기본값 `85`를 사용합니다. 현재 구현은 설정 JSON의
`output_quality` 값을 읽지 않습니다.

HandBrake 프리셋 경로가 상대 경로이면 `$HOME`을 앞에 붙여 해석합니다.
제공된 예제 파일은 다음 위치에 있습니다.

```text
src/config/handbrake_preset.json
```

### 설정 디렉터리 열기

```sh
incoming --settings
```

이 옵션은 `~/.config/incoming` 디렉터리를 macOS의 `open` 명령으로 엽니다.
설정 파일을 먼저 읽기 때문에 설정 파일이 없는 초기 상태에서는 먼저 예제
설정을 복사해야 합니다.

## 사용법

```text
incoming [options]
```

| 옵션 | 설명 |
| --- | --- |
| `-i PATH`, `--src_dir_path PATH` | 입력 디렉터리 또는 단일 입력 파일 |
| `-o PATH`, `--dst_dir_path PATH` | 출력 디렉터리 |
| `-p NAME`, `--user_preset NAME` | `~/.config/incoming/preset/NAME.json` 사용 |
| `-s`, `--settings` | 설정 디렉터리 열기 |
| `-d`, `--dummy` | 실제 변환·복사 대신 더미 파일 생성 |
| `-u`, `--unlink` | 성공적으로 처리된 원본 삭제 |
| `-v`, `--version` | 버전 출력 |
| `-h`, `--help` | 도움말 출력 |

명령줄의 `-i`, `-o`, `-p` 값은 설정 파일보다 우선합니다.

### 일반적인 실행

```sh
incoming -i "/Users/you/Incoming" -o "/Users/you/Outgoing"
```

입력·출력 경로를 생략하면 설정 파일의 값을 사용합니다.

```sh
incoming
```

### 프리셋 선택

```sh
incoming -p travel
```

위 명령은 `~/.config/incoming/preset/travel.json`을 사용합니다.

### 먼저 결과 구조만 확인

```sh
incoming --dummy -i "/Users/you/Incoming" -o "/Users/you/Outgoing"
```

`--dummy`는 각 대상 파일에 실제 변환 결과 대신 `ic-dummy`라는 내용의
파일을 생성합니다. 입력 파일은 변경하지 않습니다.

### 처리 후 원본 삭제

```sh
incoming --unlink -i "/Users/you/Incoming" -o "/Users/you/Outgoing"
```

이미지 변환, 동영상 변환, 일반 파일 복사가 성공한 경우에만 원본을
삭제합니다. 압축 해제 성공 상태와 더미 파일 상태는 원본 삭제 대상으로
취급되지 않습니다. 중요한 파일은 반드시 백업한 뒤 사용하십시오.

### 단일 파일 처리

```sh
incoming -i "/Users/you/Incoming/photo.png" -o "/Users/you/Outgoing"
```

단일 파일을 입력하면 해당 파일만 처리합니다.

## 처리 흐름과 출력 구조

1. 설정과 선택한 프리셋을 읽습니다.
2. 입력 경로를 확인하고 출력 디렉터리를 생성합니다.
3. 입력 디렉터리라면 하위 디렉터리를 재귀적으로 스캔합니다.
4. 이미지 작업을 먼저 수행하고, 이어서 동영상·압축·기타 파일을 처리합니다.
5. 입력 크기와 출력 크기를 요약해 출력합니다.

입력 디렉터리와 출력 디렉터리가 같으면 원본 디렉터리 이름 앞에 `[IC]`를
붙인 경로를 출력 디렉터리로 사용합니다. 예를 들어 입력이
`/Users/you/Incoming`이면 출력은 `/Users/you/[IC]Incoming`이 됩니다.

일반 파일과 변환 결과는 입력 디렉터리의 상대적인 하위 경로를 유지합니다.
출력 파일의 확장자는 프리셋의 출력 확장자로 바뀝니다.

## 로그와 오류 확인

로그 파일은 다음 위치에 추가 기록됩니다.

```text
~/.config/incoming/log/ic_log.log
```

일반 진행 상황과 오류 메시지는 표준 오류에도 출력됩니다. 입력 경로가
유효하지 않거나 출력 디렉터리를 만들 수 없으면 비정상 종료합니다.
외부 명령이 설치되지 않았거나 변환에 실패한 파일은 로그에 오류 또는
경고로 기록되며, 프로그램은 가능한 다음 파일의 처리를 계속합니다.

## 개발

```sh
cd src
make
./incoming --help
make clean
```

기본 빌드 옵션은 다음과 같습니다.

```text
cc -std=c11 -O2 -Wall -Wextra -Wpedantic
```

다른 컴파일러나 옵션을 사용하려면 `make` 변수로 지정할 수 있습니다.

```sh
make CC=clang CFLAGS="-std=c11 -O0 -g -Wall -Wextra -Wpedantic"
```

## 알려진 제한 사항

- JSON 파서는 범용 JSON 파서가 아니라 필요한 키를 문자열 검색으로 읽습니다.
  복잡한 JSON 형식이나 이스케이프된 문자열은 주의해서 사용해야 합니다.
- 경로 최대 길이는 4096바이트입니다.
- 동영상 인코더는 현재 코드에서 HandBrakeCLI를 사용하도록 고정되어 있습니다.
- `ffmpeg` 관련 설정은 예제 프리셋에 남아 있지만 현재 C 구현의 동영상 처리
  경로에서는 사용되지 않습니다.
- `process_hidden_files_toggle`, `open_dst_dir_when_done` 등 레거시 설정의
  일부 키는 현재 C 구현에서 적용되지 않습니다.
- EXIF는 전체 제거 옵션만 실제 ImageMagick 명령에 반영됩니다. GPS만 제거하는
  옵션은 현재 저장만 되고 동작에는 영향을 주지 않습니다.
- 디렉터리 내 숨김 파일은 현재 기본 설정상 처리 대상에 포함됩니다.

## 기여

버그 제보와 기능 제안은 [Issues](https://github.com/week-end-manufacture/incoming/issues)에
남겨 주세요. 변경 사항은 작은 단위로 작성하고, 빌드와 관련 동작을 확인한 뒤
Pull Request를 제출해 주세요.

## 감사의 글

- [ImageMagick](https://imagemagick.org/)
- [HandBrake](https://handbrake.fr/)
- [FFmpeg](https://ffmpeg.org/)
- [Homebrew](https://brew.sh/)
