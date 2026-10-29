# incoming

`incoming` is a POSIX C program that recursively scans an input directory (or
a single file), converts images and videos, extracts archives, and copies other
files to an output directory.

- Version: **1.0.4**
- Implementation: C11
- License: [MIT](./LICENSE)
- Repository: <https://github.com/week-end-manufacture/incoming>

## Features

- Recursively process input directories and their subdirectories
- Convert images with ImageMagick `magick`, retrying with `convert`
- Convert videos with HandBrakeCLI and a HandBrake preset
- Extract ZIP, RAR, and 7z archives
- Copy files with unknown extensions without conversion
- Configure output extensions and image quality
- Preview the output structure with `--dummy`
- Delete successfully converted or copied source files with `--unlink`
- Write processing logs and display per-file progress

> **Note:** The C implementation classifies files by extension. It does not
> inspect MIME types, so file extensions must be correct.

## Supported File Types

### Images

The default image extensions are:

`.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.tif`

Images are converted to `.jpg` by default while keeping the original base name.
For example, `photo.png` becomes `photo.jpg` in the output directory.

### Videos

The default video extensions are:

`.asf`, `.avi`, `.flv`, `.mkv`, `.mov`, `.mp4`, `.mpeg`, `.ts`, `.webm`,
`.wmv`, `.m4v`, `.mpg`, `.mts`, `.m2ts`, `.vob`, `.evo`

Videos are converted to `.mp4` by default and encoded according to the
configured HandBrake preset.

### Archives

- `.zip`: `unzip`
- `.rar`: `unrar`
- `.7z`: `7z`

Archives are extracted in the directory containing the source archive, not in
the output directory. The program creates a directory named
`<filename>_zip`, `<filename>_rar`, or `<filename>_7z`.

### Other Files

Files with unsupported extensions are copied without conversion while
preserving their relative directory structure.

## Requirements

### Operating System

The program uses POSIX APIs and is intended for macOS or Linux-like systems.
The `--settings` option uses macOS's `open` command to open the configuration
directory.

### Build Tools

- A C11-compatible compiler (`cc`, `clang`, or `gcc`)
- `make`

### Runtime Commands

The required commands depend on the file types being processed.

| Feature | Command |
| --- | --- |
| Image conversion | `magick` or `convert` (ImageMagick) |
| Video conversion | `HandBrakeCLI` |
| ZIP extraction | `unzip` |
| RAR extraction | `unrar` |
| 7z extraction | `7z` |

On macOS with Homebrew:

```sh
brew install imagemagick handbrake p7zip
```

`unzip` is included with macOS. RAR processing requires an `unrar` executable
to be installed separately.

## Installation

### Build from Source

```sh
git clone https://github.com/week-end-manufacture/incoming.git
cd incoming/src
make
```

The executable is created at `src/incoming`.

To install it to a system directory:

```sh
cd src
make
sudo make install PREFIX=/usr/local
```

Because the Makefile installs to `$(PREFIX)/bin`, explicitly setting
`PREFIX` is recommended when choosing a system-wide installation path.

### Homebrew Formula

The repository includes [Formula/incoming.rb](./Formula/incoming.rb). The
Formula builds the C program and declares ImageMagick, HandBrake, and p7zip as
dependencies.

```sh
brew install --build-from-source Formula/incoming.rb
```

When installed through the Formula, example configuration files are placed
under Homebrew's `share/incoming` directory. Copy them before the first run:

```sh
mkdir -p ~/.config/incoming
cp -R "$(brew --prefix)/share/incoming/config/"* ~/.config/incoming/
```

## Configuration

At startup, the program reads:

```text
~/.config/incoming/settings.json
```

Execution fails if the file is missing or does not contain these required keys:

- `src_dir_path`
- `dst_dir_path`
- `default_preset_path`

Minimal example:

```json
{
  "src_dir_path": "/Users/you/Incoming",
  "dst_dir_path": "/Users/you/Outgoing",
  "default_preset_path": ".config/incoming/preset/preset.json"
}
```

If `default_preset_path` starts with `/`, it is treated as an absolute path.
Otherwise, `$HOME` is prepended.

### Image and Video Presets

The default preset is the JSON file referenced by `default_preset_path`.
The `-p` option overrides it with a preset from:

```text
~/.config/incoming/preset/<name>.json
```

The C implementation reads these preset keys:

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `image_process_toggle` | boolean | `true` | Enable image conversion |
| `video_process_toggle` | boolean | `true` | Enable video conversion |
| `process_hidden_files_toggle` | boolean | `true` | Include files and directories whose names start with `.` |
| `image_process.output_ext` | string | `.jpg` | Image output extension |
| `video_process.output_video_ext` | string | `.mp4` | Video output extension |
| `remove_all_exif_data` | boolean | `false` | Remove EXIF with ImageMagick `-strip` |
| `remove_only_gps_exif_data` | boolean | `false` | Read but not applied by the current implementation |
| `HandBrake_presets_path` | string | none | HandBrake preset JSON path |

Image quality uses the code default of `85`. The current implementation does
not read `output_quality` from the JSON configuration.

The `output_ext` inside `video_process.ffmpeg` is an ffmpeg-specific setting
and is not used as the image output extension.

If the HandBrake preset path is relative, `$HOME` is prepended. An example
preset is included at:

```text
src/config/handbrake_preset.json
```

### Open the Configuration Directory

```sh
incoming --settings
```

This opens `~/.config/incoming` with macOS's `open` command. Because the
program loads the configuration before handling this option, copy the example
configuration first when setting up a new installation.

## Usage

```text
incoming [options]
```

| Option | Description |
| --- | --- |
| `-i PATH`, `--src_dir_path PATH` | Input directory or single input file |
| `-o PATH`, `--dst_dir_path PATH` | Output directory |
| `-p NAME`, `--user_preset NAME` | Use `~/.config/incoming/preset/NAME.json` |
| `-s`, `--settings` | Open the configuration directory |
| `-d`, `--dummy` | Create dummy files instead of converting or copying |
| `-u`, `--unlink` | Delete successfully processed source files |
| `-v`, `--version` | Print the version |
| `-h`, `--help` | Print help |

Command-line values for `-i`, `-o`, and `-p` take precedence over the
configuration file.

### Basic Processing

```sh
incoming -i "/Users/you/Incoming" -o "/Users/you/Outgoing"
```

If the input and output paths are omitted, the values from the configuration
file are used:

```sh
incoming
```

### Select a Preset

```sh
incoming -p travel
```

This uses `~/.config/incoming/preset/travel.json`.

### Preview the Output Structure

```sh
incoming --dummy -i "/Users/you/Incoming" -o "/Users/you/Outgoing"
```

`--dummy` creates a file containing `ic-dummy` instead of producing the real
conversion or copy result. Source files are not modified.

### Delete Sources after Processing

```sh
incoming --unlink -i "/Users/you/Incoming" -o "/Users/you/Outgoing"
```

Source files are deleted only after successful image conversion, video
conversion, or ordinary file copying. Successfully extracted archives and
dummy files are not considered eligible for deletion. Back up important files
before using this option.

### Process a Single File

```sh
incoming -i "/Users/you/Incoming/photo.png" -o "/Users/you/Outgoing"
```

Only the specified file is processed.

## Processing Flow and Output Layout

1. Load the configuration and selected preset.
2. Validate the input path and create the output directory.
3. Recursively scan the input directory, if the input is a directory.
4. Process images first, followed by videos, archives, and other files.
5. Print a summary of incoming and outgoing sizes.

If the input and output directories are the same, the program uses a directory
with `[IC]` prepended to the original directory name. For example, an input
directory of `/Users/you/Incoming` produces `/Users/you/[IC]Incoming`.

Ordinary files and conversion results retain their relative paths under the
input directory. Output extensions are changed according to the selected
preset.

## Logs and Errors

The log file is appended at:

```text
~/.config/incoming/log/ic_log.log
```

Progress and error messages are also written to standard error. The program
exits unsuccessfully when the input path is invalid or the output directory
cannot be created.

If an external command is missing or a file conversion fails, the program
records an error or warning and continues with other files when possible.

## Development

```sh
cd src
make
./incoming --help
make clean
```

The default compiler options are:

```text
cc -std=c11 -O2 -Wall -Wextra -Wpedantic
```

Override the compiler or flags through Make variables:

```sh
make CC=clang CFLAGS="-std=c11 -O0 -g -Wall -Wextra -Wpedantic"
```

## Known Limitations

- The JSON reader is not a general-purpose JSON parser; it searches for the
  required keys as strings. Complex JSON formatting and escaped strings should
  be used with care.
- Paths are limited to 4096 bytes.
- The video encoder is currently fixed to HandBrakeCLI in the C implementation.
- `ffmpeg` settings remain in the example preset, but are not used by the
  current C video-processing path.
- Some legacy settings, including `open_dst_dir_when_done`, are not applied by
  the C implementation.
- Only the remove-all-EXIF option is passed to ImageMagick. The GPS-only option
  is currently read but does not affect processing.
- Hidden files in directories are included by default. Set
  `process_hidden_files_toggle` to `false` in the selected preset to skip
  hidden files and directories.

## Contributing

Report bugs and request features through
[Issues](https://github.com/week-end-manufacture/incoming/issues). Keep
changes focused, verify the build and relevant behavior, and submit a pull
request.

## Acknowledgments

- [ImageMagick](https://imagemagick.org/)
- [HandBrake](https://handbrake.fr/)
- [FFmpeg](https://ffmpeg.org/)
- [Homebrew](https://brew.sh/)
