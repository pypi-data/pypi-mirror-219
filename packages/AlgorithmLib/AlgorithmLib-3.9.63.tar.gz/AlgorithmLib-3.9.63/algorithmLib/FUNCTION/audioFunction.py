import wave
import sys,os
from os import  path
sys.path.append(path.dirname(__file__))
sys.path.append(os.path.dirname(path.dirname(__file__)))
from moviepy.editor import AudioFileClip
from commFunction import get_rms,get_ave_rms,get_one_channel_data,get_file_duration,get_data_array
from formatConvert import pcm2wav
import numpy as np
import scipy.signal as signal
import math

def get_wav_from_mp4(mp4file):
    """
    Parameters
    ----------
    mp4file

    Returns
    -------

    """
    suffix = os.path.splitext(mp4file)[-1]
    if suffix != '.mp4':
        raise TypeError('wrong format! not mp4 file!' + str(suffix))
    my_audio_clip = AudioFileClip(mp4file)
    newFileName = mp4file[:-4] + '.wav'
    my_audio_clip.write_audiofile(newFileName)
    return newFileName


def isSlience(Filename =None,section=None,channels=1, bits=16, sample_rate=16000):
    """
    Parameters
    ----------
    Filename 支持 wav 和 pcm 和MP4

    Returns
    -------

    """
    suffix = os.path.splitext(Filename)[-1]

    if suffix == '.mp4':
        Filename = get_wav_from_mp4(Filename)
    if suffix == '.pcm':
        Filename = pcm2wav(Filename,channels,bits,sample_rate)
    if suffix == '.wav':
        pass
    lenth,fs = get_file_duration(Filename)
    data = get_one_channel_data(Filename)
    if section is None:
        startTime = 0
        endTime = lenth
    else:
        startTime = section[0]
        endTime = section[1]
    if startTime > lenth or startTime > endTime:
        raise TypeError('start point is larger than the file lenth :' + str(suffix))
    if endTime > lenth:
        endTime = lenth
    ins = data[int(startTime*fs):int(endTime*fs)]

    dBrmsValue = get_rms(ins)#20*math.log10(get_rms(ins)/32767+ 1.0E-6)
    print(dBrmsValue)
    if dBrmsValue > -70:
        return False
    else:
        for n in range(len(ins)//480):
            curdata = ins[480*n:480*(n+1)]
            dBrmsValue = get_rms(curdata)#20 * math.log10(get_rms(curdata) / 32767 + 1.0E-6)
            print(dBrmsValue)
            if dBrmsValue > -60:
                return False
        return True
    pass


def audioFormat(wavFileName=None):
    """
    wavFileName：输入文件 wav，mp4
    Returns
    -------
    refChannel:通道数
    refsamWidth：比特位 2代表16bit
    refsamplerate：采样率
    refframeCount：样点数
    """
    suffix = os.path.splitext(wavFileName)[-1]
    if suffix != '.wav' and suffix != '.mp4':
        raise TypeError('wrong format! not wav/mp4 file!' + str(suffix))
    if suffix == '.mp4':
        wavFileName = get_wav_from_mp4(wavFileName)
    wavf = wave.open(wavFileName, 'rb')
    refChannel,refsamWidth,refsamplerate,refframeCount = wavf.getnchannels(),wavf.getsampwidth(),wavf.getframerate(),wavf.getnframes()
    return refChannel,refsamWidth*8,refsamplerate,refframeCount

def get_rms_level(wavFileName=None,rmsMode='total',section=None):
    """
    wavFileName：输入文件 wav，mp4
    Returns
    -------
    refChannel:通道数
    refsamWidth：比特位 2代表16bit
    refsamplerate：采样率
    refframeCount：样点数
    """
    suffix = os.path.splitext(wavFileName)[-1]
    if suffix != '.wav':
        raise TypeError('wrong format! not wav file!' + str(suffix))

    lenth,fs = get_file_duration(wavFileName)
    data = get_one_channel_data(wavFileName)
    if section == None:
        startTime = 0
        endTime = lenth
    else:
        startTime = section[0]
        endTime = section[1]
    if startTime > lenth or startTime > endTime:
        raise TypeError('start point is larger than the file lenth :' + str(suffix))
    if endTime > lenth:
        endTime = lenth
    curdata = data[int(startTime*fs):int(endTime*fs)]
    if rmsMode == 'total':
        return get_rms(curdata)
    if rmsMode == 'average':
        return get_ave_rms(curdata)
    return None



def calculate_band_energy(audio_signal, sample_rate, num_bands):
    # Perform FFT on audio signal
    fmin,fmax = 100,sample_rate/2 - 100
    freq_points = np.linspace(0, sample_rate/2, num_bands+1)

    # Compute center frequencies of each band
    center_freqs = freq_points[:-1] + np.diff(freq_points)/2
    # Compute bandwidth of each band
    bandwidths = np.diff(freq_points)

    # Compute lower and upper frequency limits of each band
    lower_freqs = center_freqs - bandwidths/2
    upper_freqs = center_freqs + bandwidths/2

    # Clip lower and upper frequency limits to specified range
    lower_freqs = np.clip(lower_freqs, fmin, fmax)
    upper_freqs = np.clip(upper_freqs, fmin, fmax)
    # Define bandpass filter for each frequency band
    b, a = signal.butter(4, [lower_freqs[0], upper_freqs[-1]], 'bandpass', fs=sample_rate)
    band_filters = [signal.butter(4, [lower_freqs[i], upper_freqs[i]], 'bandpass', fs=sample_rate) for i in range(num_bands)]

    # Apply each bandpass filter to the FFT signal
    band_signals = [signal.filtfilt(band_filters[i][0], band_filters[i][1], audio_signal.astype(np.float32)) for i in range(num_bands)]


    # Calculate energy for each frequency band
    band_energy = [ get_rms(band_signals[i]) for i in range(num_bands)]
    return band_energy,upper_freqs

def find_index(lst):
    last_elem = lst[-1]
    for i, elem in reversed(list(enumerate(lst))):
        if elem - last_elem > 6:
            return i
    return -1
def get_effective_spectral(audiofile):
    audio_file, sample_rate, ch = get_data_array(audiofile)

    # Calculate energy for each frequency band
    band_energy, upper_freqs = calculate_band_energy(audio_file, sample_rate, 40)
    final_index = find_index(band_energy)

    # Print energy values for each band
    return upper_freqs[final_index]

def find_max_energy_frequency(file_path):
    # 加载声音文件
    data,rate,ch = get_data_array(file_path)
    # 去均值，去掉直流分量
    data = data - np.mean(data)
    # 计算FFT（快速傅里叶变换）
    n = len(data)
    if n % 2 == 1:
        data = np.append(data, 0)
        n += 1
    X = np.fft.rfft(data)
    X = X[:n//2+1]
    # 计算频域能量
    energy = np.abs(X)**2
    # 找到能量最大的频率
    f = np.linspace(0, rate / 2, len(X))
    max_energy_index = np.argmax(energy)
    max_energy_frequency = f[max_energy_index]

    return max_energy_frequency

def cal_pitch(ref_path,file_path,pitchlogMode=1):
    src_fs = find_max_energy_frequency(ref_path)
    ds_fs = find_max_energy_frequency(file_path)
    assert pitchlogMode == 0 or pitchlogMode == 1
    result = 0
    if pitchlogMode == 1:
        result = math.log(ds_fs/src_fs, 2) * 12
    if pitchlogMode == 0:
        result = ds_fs/src_fs
    return result


if __name__ == '__main__':
    ref = '8_final_speech.wav'
    #print(isSlience(ref,section=[0,20]),)
    #print(audioFormat(ref))
    print(get_effective_spectral(ref))