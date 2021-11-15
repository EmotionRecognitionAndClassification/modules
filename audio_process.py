import os
import librosa
import nlpaug
import noisereduce as nr
import soundfile as sf
import nlpaug.augmenter.audio as naa
from pydub import AudioSegment
import webrtcvad
vad = webrtcvad.Vad()

from voice_detect import wave_sliceing

class audio:
    
    def __init__(self,filePath,writePath):
        self.filePath = filePath
        self.writePath = writePath
        
    def check_audio_format(self):
        fn=os.path.splitext(os.path.basename(self.filePath))[0]
        en=os.path.splitext(os.path.basename(self.filePath))[1]
        
        if en == ".wav":
            return True
            
        else:
            return False
            
    def convert_audio_format(self):
        fn=os.path.splitext(self.filePath)[0]
        en=os.path.splitext(self.filePath)[1][1:]
        src = fn+'.wav'
        
        sound = AudioSegment.from_file(self.filePath, en)
        sound.export(src, 'wav') 
        #os.remove(self.filePath)
        
        return src
    
    def voice_frame_append(self):
        # this fun append all voice frames withen a audio file
        # if given audio is slient then returns no voice 
        
        clip = wave_sliceing(self.filePath)
        try :
            clip.voise_segments()
            return True
        except:
            return False
    
    def read_audio(self):
        #naming convention of files --> start with male../ female..
        
        fn=os.path.splitext(os.path.basename(self.filePath))[0]
       
        if fn[:4] == "male":
            label = 'male'
        elif fn[:6] == "female":
            label = 'female'
        else:
            label = 'check file naming convention'
            
        
        wav, sr = librosa.load(self.filePath, sr=48000)
        return label,wav,sr
    
    
    
    def process(self):
        
        audio_format = self.check_audio_format()
        if audio_format == False:
            self.filePath = self.convert_audio_format()
        
        audio_clip = self.voice_frame_append()
        
        if audio_clip == False:
            return "Sorry ! No voice in given file"
            
        else:
            label,wav,sr = self.read_audio()
        
        #aug = naa.LoudnessAug(factor=(2, 5))
        #wav = aug.augment(wav)
        
        wav = nr.reduce_noise(y=wav, sr=sr)
        
        #onset_env = librosa.onset.onset_strength(wav, sr=sr)
        #tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
        
        sf.write(self.writePath, wav, sr)
        return self.writePath,label
   
        
        