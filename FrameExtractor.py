import os
import cv2 as cv


def ExtractFrames(videoPath, lotName, camera, skipCount):
    video = cv.VideoCapture(videoPath)
    path = os.path.join(os.getcwd(), lotName, camera)
    os.makedirs(path)

    print("Saving images to {}".format(path))

    frameNum = 0
    while video.isOpened():
        retval, frame = video.read()

        if retval is False:
            break
        if frameNum % skipCount == 0:
            cv.imwrite(os.path.join(path, lotName + "_" + camera + "_Frame" + str(frameNum) + ".png"), frame)

        frameNum += 1

    video.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    videoPath = input("Enter video file path: ")
    lot, camera, skipCount = input("Enter lot name, camera, and frame skip count: ").split()
    skipCount = int(skipCount)

    ExtractFrames(videoPath, lot, camera, skipCount)
