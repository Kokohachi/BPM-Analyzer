from pydub import AudioSegment
from tqdm import tqdm
import os
import librosa
import numpy as np

import matplotlib.pyplot as plt

if os.name == 'nt':
    import ctypes
 
    # https://docs.microsoft.com/en-us/windows/console/setconsolemode?redirectedfrom=MSDN
    ENABLE_PROCESSED_OUTPUT = 0x0001
    ENABLE_WRAP_AT_EOL_OUTPUT = 0x0002
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    MODE = ENABLE_PROCESSED_OUTPUT + ENABLE_WRAP_AT_EOL_OUTPUT + ENABLE_VIRTUAL_TERMINAL_PROCESSING
 
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)
    kernel32.SetConsoleMode(handle, MODE)

#Set Colour Variables
red="\033[31m"
blue="\033[34m"
cyan="\033[36m"
yellow="\033[33m"
green="\033[32m"
purple="\033[35m"
bold="\033[1m"
end="\033[0m"

def cut_sound_file(filename, number):
    filesuffix = filename.split(".")[-1]
    sound = AudioSegment.from_file(filename, format=filesuffix)
    sec=sound.duration_seconds
    print(f"{yellow}Total Time(s) : ",end, sec)
    seq=sec/int(number) 
    seq=round(seq)
    start=1
    for i in range(seq):
        ends=start+10
        sound_part = sound[start*1000:ends*1000]
        sound_part.export(f"output/{i}.wav", format="wav")
        print(f"{yellow}{i}.wav --> {green}OK!")
        start = ends
    return(seq)

def analyze_bpm(seq):
    print(cyan+"BPM")
    for i in range(seq):
        duration = 10
        x_sr = 200
        bpm_min, bpm_max = 30, 300
        filepath = f"output/{i}.wav"
        # 楽曲の信号を読み込む

        y, sr = librosa.load(filepath)

        # ビート検出用信号の生成
        # リサンプリング & パワー信号の抽出
        x = np.abs(librosa.resample(y, sr, x_sr)) ** 2
        x_len = len(x)

        # 各BPMに対応する複素正弦波行列を生成
        M = np.zeros((bpm_max, x_len), dtype=complex)
        for bpm in range(bpm_min, bpm_max): 
            thete = 2 * np.pi * (bpm/60) * (np.arange(0, x_len) / x_sr)
            M[bpm] = np.exp(-1j * thete)

        # 各BPMとのマッチング度合い計算
        #（複素正弦波行列とビート検出用信号との内積）
        x_bpm = np.abs(np.dot(M, x))

        # BPM　を算出
        bpm = np.argmax(x_bpm)
        print(f"{yellow}{i}.wav --> BPM : ",end, bpm)
        
        
print(
f"""
{yellow}== {end}BPM-Analyzer{yellow} -----------------------------------------------------------
    {yellow}BPM-Analyzer/ BPM解析ツール{end}
    {cyan}Version:{end} 0.1.0
    {cyan}Developed by:{end}ここはち(@Kokohachi)
    {cyan}Repository:{end}https://github.com/Kokohachi/BPM-Analyzer
{yellow}-------------------------------------------------------------------------------{end}
""".strip()
)

file = os.path.exists("output")
if file == True:
    print(f"{yellow}Output Directory -> {green}{file}{end}")

if file == False:
        #保存先ディレクトリの作成
    print(f"{yellow}Output Directory -> {red}{file}{end}")
    os.mkdir("output")
    print(f"{green}Output Directory Created.{end}")

filename = input(f'{yellow}Filename -> {end}')
sequence = input(f'{yellow}Separate by -> {end}')
qqq=cut_sound_file(filename, sequence)
print(f"{yellow}Sequence(s)->{end}{qqq}")
analyze_bpm(qqq)