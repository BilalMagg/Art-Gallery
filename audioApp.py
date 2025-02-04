import simpleaudio as sa
from pydub import AudioSegment

audio_file1 = './project/static/audios/audio1.wav'
audio_file2 = './project/static/audios/audio2.m4a'
audio_file3 = './project/static/audios/audio3.mp3'
audio1 = AudioSegment.from_file(audio_file1)
audio2 = AudioSegment.from_file(audio_file2)
audio3 = AudioSegment.from_file(audio_file3)


# wave_obj = sa.WaveObject.from_wave_file(audio_file)
# play_obj = wave_obj.play()

def playAudio(audio = audio1):
  play_obj = sa.play_buffer(audio.raw_data,num_channels=audio.channels,bytes_per_sample=audio.sample_width,sample_rate=audio.frame_rate)
  play_obj.wait_done()

# playAudio()


def change_speed(audio = audio1,speed=1.5):
  new_frame_rate = int (audio.frame_rate * speed)
  return audio._spawn(audio.raw_data, overrides = {"frame_rate": new_frame_rate}).set_frame_rate(audio.frame_rate)

faster_audio = change_speed(audio1,0.7)
# faster_audio.export("faster_audio.wav",format="wav")

# audio.reverse()
# audio.fade_in(5000).fade_out(2000)
# audio3.overlay(audio2,position= 2000) # audio2 starts 2s after audio3
# audio1[:3000] # extract only the first 3 sec
# audio1.export("audioConvertedToMP3.mp3",format="mp3") # convert the "wav" extension to "mp3" and export it 
# audio1[:3000]+audio2[:2000]+audio3 # concatenation

playAudio(audio1[:3000]+audio2[:2000]+audio3)