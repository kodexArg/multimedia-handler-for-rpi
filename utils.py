import subprocess
from pathlib import Path

BASE_PATH = Path(__file__).parent.resolve()
VIDEOS_PATH = BASE_PATH / 'static' / 'videos'
CONVERTER_PATH = BASE_PATH / 'static' / 'converter'
STATIC_PATH = BASE_PATH / 'static'


""" ToDo: it can be replaced for any piece of code that converts a simple JPG to MP4 that last a giving number of seconds"""

def ffmpeg(
    ff_input_file,
    ff_output_file,
    ff_time,
    ff_vcodec='libx264',
    ff_vfilter='scale=iw/2:-1'
):

    ff_cmd:str = (
        f'ffmpeg -loop 1 -i {ff_input_file} '
        f'-t {ff_time} '
        f'-vcodec {ff_vcodec} '
        f'-vf \"{ff_vfilter}\" '
        f'{ff_output_file} -y '
        )

    print('\n' * 5)
    print(ff_cmd)
    print('\n' * 2)
    subprocess.call(ff_cmd, shell=True)
    print('\n' * 5)
    
    return True
