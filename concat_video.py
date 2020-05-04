import conf
from moviepy.editor import *
import numpy
import os
import sys
import fnmatch
import re


videoFileExtension = '.mp4'


def walklevel(some_dir, level=0):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def get_video_folder_path(videoFolderName):
    pathRoot = 'D:/Tiktok/'
    print('Getting videos {} from {}'.format(videoFolderName, pathRoot))
    return pathRoot + videoFolderName + '/'


def find_all_videos(searchPattern='video*', videoFolder='C:/'):
    foundVideoName = []
    # Look for mininum video ID
    for root, dirs, files in walklevel(videoFolder):
        for name in sorted(files):
            if fnmatch.fnmatch(name, searchPattern):
                print('Files named {} found.'.format(name))
                foundVideoName.append(name)
    extractedId = extract_id_from_name(foundVideoName)
    print(extractedId)
    convertedId = list(map(int, extractedId))
    print(convertedId)
    convertedId.sort()
    print('FOUND {} videos'.format(len(convertedId)))
    
    global videoFileExtension
    videosDirList = []

    # Remove * wildcard from searchpattern to get video name
    getVideoName = re.compile('(\*)')
    videoNameRoot = getVideoName.sub('', searchPattern)
    videoFolderPath = str(os.path.dirname(videoFolder)) + '/' + videoNameRoot
    
    # Piece up all the videos videotogether
    for idx, files in enumerate(convertedId):
        print(convertedId[idx])
        videosDirList.append(videoFolderPath + str(convertedId[idx]) + videoFileExtension)
    print(videosDirList)

    return videosDirList


def extract_id_from_name(filesList):
    global videoFileExtension
    listId = []
    # Look for coherent number in the file name
    findNumber = re.compile('([0-9]+)')
    findExtension = re.compile(videoFileExtension)
    for name in filesList:
        # Remove file extension
        modifiedName = findExtension.sub('', name)
        # Split names into list of several elements
        splittedList = findNumber.split(modifiedName)
        # The first element is string 'video', take the second elem
        listId.append(splittedList[1])
    return listId


def get_clip(videosList):
    clipList = []
    for idx, items in enumerate(videosList):
        clipList.append(VideoFileClip(videosList[idx]))
    return clipList


def main():
    path = get_video_folder_path(sys.argv[1])
    videosDirList = find_all_videos('video*', path)
    allClip = get_clip(videosDirList)
    final_clip = concatenate_videoclips(allClip)
    txt = TextClip("ILTiktok", fontsize=30, color='white')
    txt = txt.set_position((0.1,0.8), relative='True').set_duration(
        final_clip.duration)

    video = CompositeVideoClip([final_clip, txt])

    video.write_videofile('{}.mp4'.format(sys.argv[1]), fps=30, codec='libx264')


if __name__ == '__main__':
    main()






#
# fileName = "D:/Tiktok/@granlegacysings/video0.mp4"
# fileName2 = "D:/Tiktok/@granlegacysings/video1.mp4"
#
# clip1 = VideoFileClip(fileName)
# clip2 = VideoFileClip(fileName2)
# txt = TextClip("@Tiktok_School", fontsize=40, color='white')
#
#
# final_clip = concatenate_videoclips([clip1, clip2], method='compose')
# clipDuration = final_clip.duration
# txt = txt.set_pos('bottom').set_duration(clipDuration)
# video = CompositeVideoClip([final_clip, txt])
# video.write_videofile("videotogether.mp4", fps=30)
# # clip.reader.close()
# # clip.audio.reader.close_proc()
