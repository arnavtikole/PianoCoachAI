import librosa

def load_audio(audio_file):
    waveform, sample_rate = librosa.load(audio_file,sr = None,mono = True)
    return waveform,sample_rate

