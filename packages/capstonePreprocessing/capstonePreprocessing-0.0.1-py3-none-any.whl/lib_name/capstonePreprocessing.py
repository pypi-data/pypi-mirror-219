import cv2
import mediapipe as mp
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
# from fastdtw import fastdtw
import numpy as np


def preprocess(file_path: str):
    """
    Given the path of the video calculate angle time series during the pose

    Parameters:
        file_path : Path to the video file

    Returns:
        df(Pandas.dataframe):Dataframe consisting of 8 angles for each frame
    """
    print(file_path)
    return calculate_angles(file_path)


def calcAngle(x):
    """
    Given the coordinated(x,y) calculate the angel formed by them

    Parameters:
        x(List[(x,y)]) : List of 3 pairs of x and y coordinates

    Returns:
        angle(float): Angle made by the 3 coordinates(c1, c2, c3) at c2
    """
    a = np.array(x[0])
    b = np.array(x[1])
    c = np.array(x[2])

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle
    return angle


def calculate_angles(path):
    """
    Given the path of the video calculate angle time series during the pose

    Parameters:
        path : Path to the video file

    Returns:
        df(Pandas.dataframe):Dataframe consisting of 8 angles for each frame
    """
    cap = cv2.VideoCapture(path)
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    lst = []

    angledict = {'leftWES': [], 'leftESH': [], 'leftSHK': [], 'leftHKA': [], 'rightWES': [], 'rightESH': [],
                 'rightSHK': [], 'rightHKA': []}
    with mp_pose.Pose(
            smooth_landmarks=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break
            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # frame_height, frame_width = image.shape[:2]

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            # image.flags.writeable = False
            results = pose.process(image)

            # Declaring aliases
            landmarks = results.pose_landmarks.landmark
            setOfJoints = mp_pose.PoseLandmark

            # Storing the coordinates as a pair of x and y values
            leftWrist = [landmarks[setOfJoints.LEFT_WRIST].x, landmarks[setOfJoints.LEFT_WRIST].y]
            leftElbow = [landmarks[setOfJoints.LEFT_ELBOW].x, landmarks[setOfJoints.LEFT_ELBOW].y]
            leftShoulder = [landmarks[setOfJoints.LEFT_SHOULDER].x, landmarks[setOfJoints.LEFT_SHOULDER].y]
            leftHip = [landmarks[setOfJoints.LEFT_HIP].x, landmarks[setOfJoints.LEFT_HIP].y]
            leftKnee = [landmarks[setOfJoints.LEFT_KNEE].x, landmarks[setOfJoints.LEFT_KNEE].y]
            leftAnkle = [landmarks[setOfJoints.LEFT_ANKLE].x, landmarks[setOfJoints.LEFT_ANKLE].y]
            rightWrist = [landmarks[setOfJoints.RIGHT_WRIST].x, landmarks[setOfJoints.RIGHT_WRIST].y]
            rightElbow = [landmarks[setOfJoints.RIGHT_ELBOW].x, landmarks[setOfJoints.RIGHT_ELBOW].y]
            rightShoulder = [landmarks[setOfJoints.RIGHT_SHOULDER].x, landmarks[setOfJoints.RIGHT_SHOULDER].y]
            rightHip = [landmarks[setOfJoints.RIGHT_HIP].x, landmarks[setOfJoints.RIGHT_HIP].y]
            rightKnee = [landmarks[setOfJoints.RIGHT_KNEE].x, landmarks[setOfJoints.RIGHT_KNEE].y]
            rightAnkle = [landmarks[setOfJoints.RIGHT_ANKLE].x, landmarks[setOfJoints.RIGHT_ANKLE].y]

            #  Creating a dictionary to calculate different angles
            angleDict = {'leftWES': (leftWrist, leftElbow, leftShoulder),
                         'leftESH': (leftElbow, leftShoulder, leftHip),
                         'leftSHK': (leftShoulder, leftHip, leftKnee),
                         'leftHKA': (leftHip, leftKnee, leftAnkle),
                         'rightWES': (rightWrist, rightElbow, rightShoulder),
                         'rightESH': (rightElbow, rightShoulder, rightHip),
                         'rightSHK': (rightShoulder, rightHip, rightKnee),
                         'rightHKA': (rightHip, rightKnee, rightAnkle)}

            # Processing the angle dict to calculate different angles
            for angle in angleDict:
                x = calcAngle(angleDict[angle])
                angledict[angle].append(x)

    cap.release()
    cv2.destroyAllWindows()
    df = pd.DataFrame(angledict)
    # print(df.head())
    return df
