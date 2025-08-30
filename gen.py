import numpy as np
import matplotlib.pyplot as plt
import librosa

audio_file = 'C:/Users/GOWTHAM/OneDrive/Desktop/GEN AI Projects/jersey.mp3'
y, sr = librosa.load(audio_file, sr=None)

print(f"Audio Time series shape: {y.shape}")
print(f"Sampling rate: {sr}")

## We Got 11871360 audio samples from the numpy array
## The number of samples per second of the above song is 48000

# Audio Features Extraction 

# Mel- Frequency Cepstral coefficients

mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
print(f"MFCC Shape: {mfccs.shape}")                             


#Visualize the MFCCs

plt.figure(figsize=(10,4))
librosa.display.specshow(mfccs, x_axis = 'time')
plt.colorbar()
plt.title('MFCC')
plt.tight_layout()
plt.show()

# CHROMA FEATURES

chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
print(f"Chroma Features Shape: {chroma_stft.shape}")     

#Visualize the chroma features

plt.figure(figsize=(10,4))
librosa.display.specshow(chroma_stft, x_axis= 'time', y_axis= 'chroma')
plt.colorbar()
plt.title('Chroma Features')
plt.tight_layout()
plt.show()

# Visualize the sound Spectrum

# Extract spectral contrast
spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
print(f"Spectral Contrast Shape: {spectral_contrast.shape}")

# Visualize spectral contrast
plt.figure(figsize=(10, 4))
librosa.display.specshow(spectral_contrast, x_axis='time')
plt.colorbar()
plt.title('Spectral Contrast')
plt.tight_layout()
plt.show()

# Visualize the tempo beats 

tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
print(f"Estimated Tempo: {tempo} BPM")

# Visualize beats on the waveform
plt.figure(figsize=(10, 4))
times = librosa.times_like(y, sr=sr)
plt.plot(times, y)
plt.vlines(times[beats], -1, 1, color='r', alpha=0.5, linestyle='--')
plt.title('Waveform with Beat Markers')
plt.show()

### FEATURE ENGINEERING TECHNIQUES

# Lets find out the mean values of the MFCCs

mfccs_mean = np.mean(mfccs, axis=1)
print(f"Mean MFCCs: {mfccs_mean}")

## Natural Language Processing

