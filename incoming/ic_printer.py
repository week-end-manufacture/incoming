import sys


def print_process_start(src_dir_path,
                        dst_dir_path,
                        preset_path,
                        image_process_toggle,
                        filtered_image_ext_dict,
                        image_output_ext,
                        image_output_quality,
                        video_process_toggle,
                        filtered_video_ext_dict,
                        output_video_ext,
                        HandBrake_presets_path):
    sys.stdout.write(f'\n⚙️ Process start \
                        \n- incoming:  [{src_dir_path}] \
                        \n- outgoing:  [{dst_dir_path}] \
                        \n- preset:    [{preset_path}] \
                        \n\t- image process: {image_process_toggle} \
                        \n\t\t{filtered_image_ext_dict} \
                        \n\t\t==> {image_output_ext} (with PIL quality = {image_output_quality}) \
                        \n\t- video process: {video_process_toggle} \
                        \n\t\t{filtered_video_ext_dict} \
                        \n\t\t==> {output_video_ext} (with HandBrakeCLI and preset [{HandBrake_presets_path}])')
    
    sys.stdout.write('\n\n')
    sys.stdout.flush()

def print_job_done(space=0, carriage=False, backspace=0):
    if (carriage):
        sys.stdout.write('\r' + (' ' * space) + '╰─ DONE' + (' ' * backspace) + '\n')
        sys.stdout.flush()
    else:
        sys.stdout.write('\n' + (' ' * space) + '╰─ DONE\n\n')
        sys.stdout.flush()

def print_video_process_init():
    sys.stdout.write('🎬 Video Process\n')
    sys.stdout.flush()

def print_progressbar(iteration,
                      total,
                      prefix='',
                      suffix='',
                      length=30,
                      fill='█'):
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        sys.stdout.write(f'\r{prefix} [{bar}] {percent}% {suffix}')
        sys.stdout.flush()

def print_loader(idx):
    loadd = {0: '\\', 1: '|', 2: '/', 3: '-'}

    return loadd[idx]


