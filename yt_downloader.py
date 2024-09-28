from pytubefix import YouTube
from pytubefix import Playlist
#from colorama import Fore, Back, Style
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
        print('Number of videos in playlist: %s' % len(playlist.video_urls))

        print("Downloading...")
        for video in playlist.videos:
            download(video, option)
    
    print("Download finished")



def download(video, type):
    if type == 1:
        try:
            #stream = video.streams.filter(only_audio=True).first() #Uncomment for mp4 ony audio format (faster download)
            stream = video.streams.first() #Comment for mp4 only audio format
            output = stream.download("./YouDownloads/audio/")
            convert_to_mp3(output) #Comment for mp4 only audio format
            print(f'Downloaded audio of: {video.title}')
        except Exception as e:
            print(f'ERROR downloading: {str(video.title)}:\n{str(e)}')
    else:
        try:
            stream = video.streams.get_highest_resolution()
            output = stream.download("./YouDownloads/video/")
            print(f'Downloading video of: {video.title}')
        except Exception as e:
            print(f'ERROR downloading: {str(video.title)}:\n{str(e)}')


def convert_to_mp3(file):
    #Cargamos el fichero .mp4
    clip = mp.VideoFileClip(file)
    #Lo escribimos como audio y `.mp3`
    clip.audio.write_audiofile(file.replace('mp4', 'mp3'), logger=None)
    clip.close()
    os.remove(file)


if __name__ == '__main__':
    main()
    
