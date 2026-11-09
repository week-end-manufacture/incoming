# cadv

`cadv` is the C implementation of the legacy `incoming` program. It keeps the
legacy command-line options and reads the same configuration layout:

```text
~/.config/incoming/settings.json
~/.config/incoming/preset/preset.json
~/.config/incoming/handbrake_preset.json
```

The settings and selected preset files must exist and be readable; otherwise the
program reports the failing path and exits. Source files and generated output
files are also checked before they are processed or reported.

Build:

```sh
make
```

Run:

```sh
./cadv -i INPUT -o OUTPUT
./cadv --dummy -i INPUT -o OUTPUT
./cadv --unlink -i INPUT -o OUTPUT
```

With `--unlink`, successfully processed source files are deleted. Empty
subdirectories beneath the configured source directory are then removed; the
configured source directory itself is preserved.

At the end of each run, a report is written to
`~/.config/log/report_YYYYMMDD_HHMMSS.txt` by default. When
`custom_log_file_path` is set, the report is written to that directory. The report lists each
successfully outgoing file's input/output format, input/output size, processing
time, total processing time, and average processing time.

If the process receives `SIGTERM` or `SIGINT`, it stops after the active
external conversion is terminated and reaped, writes a partial report for the
files completed so far, and exits with a non-zero status.

The image and video paths invoke the same class of external tools used by the
legacy program: ImageMagick (`magick` or `convert`) for images, HandBrakeCLI
for the default video path, and `ffmpeg` when that path is selected. ZIP,
RAR, and 7z archives use the corresponding system extractor.
