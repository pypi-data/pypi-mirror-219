import cv2
import cv2.aruco as aruco
import numpy as np

class ArucoScanner:

    def __init__(self, img):
        self.img = img

    def findAruco(self, size, totalMarkers=250, draw=True):
        imgGray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        key = getattr(aruco, f'DICT_{size}X{size}_250')
        arucoDict = aruco.Dictionary_get(key)
        arucoParam = aruco.DetectorParameters_create()
        bboxs, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
        #print(bboxs)
        if draw:
            aruco.drawDetectedMarkers(self.img, bboxs)
        return[bboxs, ids]

    def augmentAruco(self, bbox, id, imgAug, text, drawId=True):
        tl = bbox[0][0][0], bbox[0][0][1]
        tr = bbox[0][1][0], bbox[0][1][1]
        br = bbox[0][2][0], bbox[0][2][1]
        bl = bbox[0][3][0], bbox[0][3][1]

        #print(tl)

        h, w, c = imgAug.shape
        pts1 = np.array([tl, tr, br, bl])
        pts2 = np.float32([[0,0],[w,0], [w,h], [0,h]])
        matrix, _ = cv2.findHomography(pts2, pts1)
        imgOut = cv2.warpPerspective(imgAug, matrix, (self.img.shape[1], self.img.shape[0]))
        cv2.fillConvexPoly(self.img, pts1.astype(int), (0,0,0))
        imgOut = self.img + imgOut
        cv2.putText(imgOut, text, (int(tl[0]), int(tl[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        return imgOut


