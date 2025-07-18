import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import numpy as np

# Create mask with rounded corners
def rounded_mask(img, radius=30):
    rows, cols = img.shape[:2]
    mask = np.zeros((rows, cols), dtype=np.uint8)
    cv2.rectangle(mask, (radius, 0), (cols - radius, rows), 255, -1)
    cv2.rectangle(mask, (0, radius), (cols, rows - radius), 255, -1)
    cv2.circle(mask, (radius, radius), radius, 255, -1)
    cv2.circle(mask, (cols - radius, radius), radius, 255, -1)
    cv2.circle(mask, (radius, rows - radius), radius, 255, -1)
    cv2.circle(mask, (cols - radius, rows - radius), radius, 255, -1)

    masked = cv2.bitwise_and(img, img, mask=mask)
    return masked


cap = cv2.VideoCapture(0) #we gave the id zero here
cap.set(3,640)
cap.set(4,480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0] #[Ai, player]

while True:
    imgBG = cv2.imread("Resources/BG.png")  # this will be a static background
    success, img = cap.read() #this success tells if it worked(T/F)

    imgScaled = cv2.resize(img,(0,0), None,0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    imgScaled = rounded_mask(imgScaled)

    #find hands here
    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            timer = time.time()- initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer>3:
                stateResult = True
                timer = 0
                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if (fingers == [0, 1, 1, 0, 0] or fingers == [0, 0, 1, 1, 0]):
                        playerMove = 3

                    randomNumber = random.randint(1,3)
                    imgAI = cv2.imread(f"Resources/{randomNumber}.png", cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))


                    #player wins

                    # Player Wins
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # AI Wins
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1


                    print(playerMove)

    imgBG[234:654, 795:1195] = imgScaled
    # imgBG[235:655, 795:1195] = imgScaled

    if stateResult :
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv2.imshow("BG", imgBG)
    # cv2.imshow("Image", img)
    # cv2.imshow("Scaled", imgScaled)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False