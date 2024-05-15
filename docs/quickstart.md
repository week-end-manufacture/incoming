---
layout: default
title: Quick Start
nav_order: 2
---
# Quick Start
 `src_dir_path`and `dst_dir_path` is `""`(empty) at first. 
```bash
$ incoming --opensettings
```
This command will open ./config/`ic_settings.json`
## Check requirements
```bash
> incoming -v
> incoming --version
```
Check installation of `incoming` also check `HandbrakeCLI`, `unrar`, `FFmpeg`(optional)
## Start
```bash
> incoming
```
Starting incoming program. Depending on the setting value of `ic_settings.json` files
```bash
> incoming --opensettings
```

```bash
> incoming -i "your/source/path" -o "your/destination/path"
```