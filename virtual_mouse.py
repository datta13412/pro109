import cv2
import math
import mediapipe as mp
from pynput.mouse import Button, Controller
import pyautogui

mouse=Controller()
cap = cv2.VideoCapture(0)
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
(screen_width, screen_height) = pyautogui.size()
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
tipIds = [4, 8, 12, 16, 20]
pinch=False

def countFingers(image, hand_landmarks, handNo=0):

	global pinch

	if hand_landmarks:
		# Get all Landmarks of the FIRST Hand VISIBLE
		landmarks = hand_landmarks[handNo].landmark
        
		fingers = []

		for lm_index in tipIds:
			# Get Finger Tip and Bottom y Position Value
			finger_tip_y = landmarks[lm_index].y 
			finger_bottom_y = landmarks[lm_index - 2].y

		
			if lm_index !=4:
				if finger_tip_y < finger_bottom_y:
					fingers.append(1)


				if finger_tip_y > finger_bottom_y:
					fingers.append(0)

		totalFingers = fingers.count(1)

	
		


def drawHandLanmarks(image, hand_landmarks):

  
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)



while True:
	success, image = cap.read()
	
	image = cv2.flip(image, 1)

	
	results = hands.process(image)

	hand_landmarks = results.multi_hand_landmarks

	drawHandLanmarks(image, hand_landmarks)

	countFingers(image, hand_landmarks)

	cv2.imshow("Media Controller", image)

	key = cv2.waitKey(1)
	if key == 27:
		break

cv2.destroyAllWindows()
