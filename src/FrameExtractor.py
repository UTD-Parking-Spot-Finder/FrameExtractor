import os
import fnmatch
import json
import numpy as np
import cv2 as cv

pts2 = np.float32([[0, 0], [300, 0], [0, 600], [300, 600]])


def ExtractFrames(videoPath, lotName, camera, skipCount, jsonPath):
    video = cv.VideoCapture(videoPath)
    path = os.path.join(os.getcwd(), lotName, camera)

    with open(jsonPath) as f:
        spotData = json.load(f)
    spots = spotData["spots"]

    if not os.path.exists(path):
        os.makedirs(path)
    frameNum = int(len(fnmatch.filter(os.listdir(path), '*.png')) / len(spots))

    print("Starting frame number:", frameNum)
    print("Saving images to {}".format(path))
    localFrameNum = 0
    while video.isOpened():
        video.set(cv.CAP_PROP_POS_FRAMES, localFrameNum * skipCount)
        retval, frame = video.read()
        if retval is False:
            break
        getSpotsFromFrame(frame, path, lotName, camera, frameNum, spots)
        localFrameNum += 1
        frameNum += 1
    video.release()


def getSpotsFromFrame(frame, path, lotName, camera, frameNum, spots):
    for i in range(0, len(spots)):
        s = spots[i]
        arr = []
        id = s["spotID"]
        arr.append(s["topLeft"])
        arr.append(s["topRight"])
        arr.append(s["bottomRight"])
        arr.append(s["bottomLeft"])

        pts1 = np.float32(arr)
        matrix = cv.getPerspectiveTransform(pts1, pts2)
        result = cv.warpPerspective(frame, matrix, (300, 600))
        outputName = (lotName + "_" + camera + "_frame_" + str(frameNum) + "_spot_" + str(id) + ".png").replace(" ", "_")
        cv.imwrite(os.path.join(path, outputName.lower()), result)


if __name__ == "__main__":
    videoPath = input("Enter video file path: ")
    lot = input("Enter lot name: ")
    camera = input("Enter camera number: ")
    skipCount = input("Enter frame skip count: ")
    jsonPath = input("Enter json file path: ")
    skipCount = int(skipCount)

    ExtractFrames(videoPath, lot, camera, skipCount, jsonPath)
