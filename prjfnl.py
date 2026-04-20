import cv2
import time
import math
import numpy as np
import mediapipe as mp
import pyautogui as pyg


pyg.PAUSE = 0
pyg.FAILSAFE = False

wCam, hCam = 640, 480       
frameR_X = 200              
frameR_Y = 150              

# sens
smooth_fast = 3             
smooth_slow = 30           
sniper_trigger_dist = 65    

clk_dst = 20             
rls_dst = 35           
drag_delay = 0.8           
scroll_speed = 20        

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False, 
    max_num_hands=1,
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.5
)
mpDraw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)  
cap.set(3, wCam)
cap.set(4, hCam)
wScr, hScr = pyg.size()

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

dragging = False            
pinch = 0        
volume_cooldown = 0 
frozen_x, frozen_y = 0, 0   
paused = False             

print(f"System Ready. Press 'P' to PAUSE/RESUME.")

while True:
    success, img = cap.read()
    if not success: break

    img = cv2.flip(img, 1) 
    
   
    if paused:
        
        cv2.putText(img, "SYSTEM PAUSED", (150, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        cv2.putText(img, "Press 'P' to Resume", (180, 300), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        
        cv2.putText(img, "Project by Adithya,Mithun,Sobith", (270, 460), cv2.FONT_HERSHEY_PLAIN, 1.3, (255, 255, 0), 1)
    
    else:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(imgRGB)
        
        cv2.rectangle(img, (frameR_X, frameR_Y), (wCam - frameR_X, hCam - frameR_Y), (0, 255, 255), 2)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                lmList = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


                if len(lmList) != 0:
                    x1, y1 = lmList[8][1:]   # Index
                    x_thumb, y_thumb = lmList[4][1:] 
                    x_pinky, y_pinky = lmList[20][1:] 

                    fingers = []
                    if lmList[4][0] < lmList[3][0]: fingers.append(1) 
                    else: fingers.append(0)
                    for id in [8, 12, 16, 20]:
                        if lmList[id][2] < lmList[id-2][2]: fingers.append(1)
                        else: fingers.append(0)

                    dist_index = math.hypot(x1 - x_thumb, y1 - y_thumb)
                    dist_pinky = math.hypot(x_thumb - x_pinky, y_thumb - y_pinky)

                   
                    if fingers[1] == 1 and fingers[2] == 0:
                        
                        

                        if dist_index < clk_dst:
                            if pinch == 0:
                                pinch = time.time()
                                frozen_x, frozen_y = plocX, plocY 
                            
                            cv2.line(img, (x1, y1), (x_thumb, y_thumb), (0, 255, 0), 3)

                            if (time.time() - pinch > drag_delay):
                                if not dragging:
                                    pyg.mouseDown()
                                    dragging = True
                                
                                x3 = np.interp(x1, (frameR_X, wCam - frameR_X), (0, wScr))
                                y3 = np.interp(y1, (frameR_Y, hCam - frameR_Y), (0, hScr))
                                clocX = plocX + (x3 - plocX) / smooth_fast
                                clocY = plocY + (y3 - plocY) / smooth_fast
                                pyg.moveTo(clocX, clocY)
                                plocX, plocY = clocX, clocY

                                cv2.putText(img, "DRAGGING", (150, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                            else:
                                cv2.putText(img, "LOCKED", (150, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

                       
                        elif dist_index > rls_dst:
                            if pinch > 0:
                                if dragging:
                                    pyg.mouseUp()
                                    dragging = False
                                else:
                                    pyg.click()
                                pinch = 0

                            
                            else:
                                if dist_index < sniper_trigger_dist:
                                    current_smooth = smooth_slow
                                    cv2.circle(img, (x1, y1), 15, (0, 255, 255), cv2.FILLED) 
                                else:
                                    current_smooth = smooth_fast
                                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED) 

                                x3 = np.interp(x1, (frameR_X, wCam - frameR_X), (0, wScr))
                                y3 = np.interp(y1, (frameR_Y, hCam - frameR_Y), (0, hScr))
                                
                                clocX = plocX + (x3 - plocX) / current_smooth
                                clocY = plocY + (y3 - plocY) / current_smooth
                                pyg.moveTo(clocX, clocY)
                                plocX, plocY = clocX, clocY

                  
                    if fingers[1] == 1 and fingers[2] == 1:
                        if y1 < hCam / 2 - 50: 
                            pyg.scroll(scroll_speed)
                            cv2.putText(img, "SCROLL UP", (150, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                        elif y1 > hCam / 2 + 50: 
                            pyg.scroll(-scroll_speed)
                            cv2.putText(img, "SCROLL DOWN", (150, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

                    
                    if dist_pinky < 20:
                        if dragging: pyg.mouseUp(); dragging = False; pinch = 0
                        if time.time() - volume_cooldown > 0.5:
                            pyg.rightClick()
                            volume_cooldown = time.time()
                            cv2.circle(img, (x_pinky, y_pinky), 15, (0, 0, 255), cv2.FILLED)

                  
                    if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 and not dragging:
                        x_wrist, y_wrist = lmList[0][1:]
                        x_mid, y_mid = lmList[9][1:]
                        angle = int(math.degrees(math.atan2(y_wrist - y_mid, x_wrist - x_mid)))
                        
                        if time.time() - volume_cooldown > 0.25:
                            if angle < 50: pyg.press("volumeup"); volume_cooldown = time.time()
                            elif angle > 130: pyg.press("volumedown"); volume_cooldown = time.time()

        else:
            if dragging: pyg.mouseUp(); dragging = False; pinch = 0

   
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    
    if not paused:
        cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
       
    
    cv2.imshow("AI Mouse by Adi,mithun and saabi", img)
    
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    elif key == ord('p'):      
        paused = not paused
        if paused: print("PAUSED")
        else: print("RESUMED")