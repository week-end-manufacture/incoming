# CLI manual
샘플파일 기반 설명
- 파일 링크 첨부
```bash
 demo
 ├── input
 │   ├── Lorem.txt
 │   ├── archive-got-3images.7z
 │   ├── archive-got-3images.rar
 │   ├── archive-got-3images.zip
 │   ├── lena.png
 │   └── video.mkv
 └── output
```

## 1 `$ incoming`(안전옵션을 넣을까..렌덤생성 두자리 숫자 인풋받고 실행되는 토클옵션)
You can just command like this. 
```bash
$ incoming # If you set values in `ic_settings.json`
```
Condition: If `src_dir_path` and `dst_dir_path` values are set in the `ic_settings.json` file.
- `ERROR_00`: THERE IS NO "IN"/"OUT" PATHS OR SETTINGS VALUE. Please Add option `-s,` `-settings` to open `ic_settings.json` or input both paths.
    - Fix: 
        ```bash
        $ incoming -s
        $ incoming --settings
        ```
        - Open `ic_settings.json` file. 
        - Set the values of `src_dir_path` and `dst_dir_path`. 
        - Put absolute path of your IN/OUT. 

## 2. `$ incoming -i 'src' -o 'dst'`(상대경로 작동가능한가?)
Yes, It's not much different from other apps.
```bash
$ incoming -i "./demo/input" -o "./demo/output"
```
- Condition: 
    - You have to put both `-i`, `-o` options. 
    - The path should be wrapped with `"path"` or `'path'`. 

 It is possible to input an absolute path or execute it from the current working path to the relative path on the terminal. In the case of a single file, you can enter the file name and extension directly into the `-i` option within the working directory.

You can use it in the following way. 
```bash
# demo e.g.
# Set your working directory "~/ic-demo/demo/input"
$ incoming -i "video.mkv" -o "../output"
```
- `ERROR_01`: SYNTEX ERROR. One of the options '-i' and '-o' is empty. Check the command you entered.

## 3 `$ incoming -i 'src' -o 'dst' -p "preset_name"` 



<!-- 다른데 옮겨야할꺼 -->

## Configure Structure
| `ic_settings.json` | `ic_preset.json` | `Handbrake_preset.json` |
|-:|:-:|-|
|1 <----------|-------- 2 <-------|------------ 3|

```json
// ic_settings.json
"default_preset_path":"./config/ic-preset/ic_preset.json",
// ic_preset.json
"HandBrake_presets_path": "./config/handbrake_preset.json",
```

 <details>
<summary>details</summary>

<!-- summary 아래 한칸 공백 두어야함 -->
### 접은 제목
접은 내용
</details>


.
`-- input
    |-- Lorem.txt
    |-- archive-got-3images.rar
    |-- lena.png
    `-- video.mkv

2 directories, 4 files

.
|-- input
|   |-- Lorem.txt
|   |-- archive-got-3images.rar
|   |-- lena.png
|   |-- outgoing_archive
|   |   `-- archive-got-3images_rar
|   |       `-- archive-got-3images
|   |           `-- image
|   |               |-- _DSC8453.jpeg
|   |               |-- _DSC8455.jpeg
|   |               `-- _DSC8457.jpeg
|   `-- video.mkv
|-- log
|   `-- ic_log.log
`-- output
    |-- lena.jpg
    |-- outgoing_archive
    |   `-- archive-got-3images_rar
    |       `-- archive-got-3images
    |           `-- image
    |               |-- _DSC8453.jpg
    |               |-- _DSC8455.jpg
    |               `-- _DSC8457.jpg
    `-- video.mp4

12 directories, 13 files