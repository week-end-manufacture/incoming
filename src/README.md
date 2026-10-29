# cadv

`cadv` is the C implementation of the legacy `incoming` program. It keeps the
legacy command-line options and reads the same configuration layout:

```text
~/.config/incoming/settings.json
~/.config/incoming/preset/preset.json
~/.config/incoming/handbrake_preset.json
```

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

At the end of each run, a report is written to
`~/.config/incoming/log/report_YYYYMMDD_HHMMSS.txt`. The report lists each
successfully outgoing file's input/output format, input/output size, processing
time, total processing time, and average processing time.

The image and video paths invoke the same class of external tools used by the
legacy program: ImageMagick (`magick` or `convert`) for images, HandBrakeCLI
for the default video path, and `ffmpeg` when that path is selected. ZIP,
RAR, and 7z archives use the corresponding system extractor.
