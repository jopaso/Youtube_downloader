from pytubefix import YouTube
from pytubefix import Playlist
from colorama import init, Fore, Back, Style
from tqdm import tqdm
import moviepy.editor as mp
import os


def main():
    vop = 0
    
    while (vop not in [1,2]):
        vop = int(input("What do you want to download?:\n1- Video\n2- Playlist\n> "))

    link = input("\npaste the url: \n> ")
    option = 0
    while (option not in [1,2]):
            option = int(input("\nWhat format do you want?:\n1- Audio\n2- Video\n> "))

    if vop == 1:      
        print("Downloading...\n")
        download(YouTube(link), option)
    else:
        playlist = Playlist(link)
        print('\nNumber of videos in playlist: %s' % len(playlist.video_urls))
        print("Downloading...")
        for video in tqdm(playlist.videos, desc='progress'):
            download(video, option)
    
    print("\nDownload finished")



def download(video, type):
    init() #init colorama
    if type == 1:
        #Comment the one you don't want and uncomment the one you want
        
        download_audio_mp3(video)
        #download_audio_mp4(video) #Faster BUT not compatible with only mp3 reproductors       
    else:
        download_video(video)

    print(Style.RESET_ALL)

def convert_to_mp3(file):
    #Load .mp4 file
    clip = mp.VideoFileClip(file)
    #write it as .mp3
    clip.audio.write_audiofile(file.replace('mp4', 'mp3'), logger=None)
    clip.close()
    os.remove(file)

def download_video(video):
    try:
        stream = video.streams.get_highest_resolution()
        output = stream.download("./YouDownloads/video/")
        print(Fore.GREEN + f'\rDownloaded video of: {video.title}')
    except Exception as e:
        print(Fore.REED + f'ERROR downloading: {str(video.title)}:\n{str(e)}')

def download_audio_mp3(video):
    try:
        stream = video.streams.first() 
        output = stream.download("./YouDownloads/audio/")
        convert_to_mp3(output)
        print(Fore.GREEN + f'\rDownloaded audio of: {video.title}')
    except Exception as e:
        print(Fore.REED + f'ERROR downloading: {str(video.title)}:\n{str(e)}')
    

def download_audio_mp4(video):
    try:
        stream = video.streams.filter(only_audio=True).first() #Uncomment for mp4 ony audio format (faster download)
        stream.download("./YouDownloads/audio/")
        print(Fore.GREEN + f'\rDownloaded audio of: {video.title}')
    except Exception as e:
        print(Fore.REED + f'ERROR downloading: {str(video.title)}:\n{str(e)}')
    
    
        


if __name__ == '__main__':
    main()
    
