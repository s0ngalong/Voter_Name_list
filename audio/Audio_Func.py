import  os, winsound
#play audio for respective events.
#async allows it to play in the background and still process code.
#play this sound forever and wait for an event to trigger to stop the music.
def BMusic(w):
    winsound.PlaySound(f'{os.getcwd()}/Audio/Bmusic.wav', winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
    w.wait()
    winsound.PlaySound(None, winsound.SND_PURGE)

#the rest is just sounds for more events.
def FullStop():
    winsound.PlaySound(f'{os.getcwd()}/Audio/ErrorSound.wav', winsound.SND_FILENAME)

def AccessGrant():
    winsound.PlaySound(f'{os.getcwd()}/Audio/Start_Acl.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
