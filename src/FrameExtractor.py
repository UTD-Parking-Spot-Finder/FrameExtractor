import os
import cv2 as cv


def ExtractFrames(videoPath, lotName, camera, skipCount):
    video = cv.VideoCapture(videoPath)
    path = os.path.join(os.getcwd(), lotName, camera)
    if not os.path.exists(path):
        os.makedirs(path)

    print("Saving images to {}".format(path))

    frameNum = 0
    while video.isOpened():
        video.set(cv.CAP_PROP_POS_FRAMES, frameNum * skipCount)
        retval, frame = video.read()
        if retval is False:
            break
        cv.imwrite(os.path.join(path, lotName + "_" + camera + "_Frame" + str(frameNum) + ".png"), frame)
        frameNum += 1

    video.release()


if __name__ == "__main__":
    videoPath = input("Enter video file path: ")
    lot = input("Enter lot name: ")
    camera = input("Enter camera number: ")
    skipCount = input("Enter frame skip count: ")
    skipCount = int(skipCount)

    ExtractFrames(videoPath, lot, camera, skipCount)
