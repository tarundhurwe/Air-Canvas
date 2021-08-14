import cv2
import numpy as np
import time
import math

def air_canvas(low, up):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    ls_red = []
    ls_blue = []
    ls_green = []

    red = (0, 0, 255)
    blue = (255, 0, 0)
    green = (0, 255, 0)

    color = green
    pTime = 0
    while True:
        ret, frame = cap.read()
        if ret == None:
            break
        
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (700,500))
        blur = cv2.GaussianBlur(frame, (9,9), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        # blank_image2 = 255 * np.ones(shape=[800, 700, 1], dtype=np.uint8)
        img = np.zeros((500,700, 3), dtype = np.uint8)
        img.fill(255)

        cv2.rectangle(frame, (0, 0), (100, 50), (245, 155, 255), -1)
        cv2.putText(frame, "Clear all", (10, 35), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 20, 255), 4)

        cv2.rectangle(frame, (110, 0), (270, 50), red, -1)
        cv2.putText(frame, "Red", (120, 35), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 4)
        
        cv2.rectangle(frame, (280, 0), (440, 50), green, -1)
        cv2.putText(frame, "Green", (290, 35), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 4)

        cv2.rectangle(frame, (450, 0), ( 610, 50), blue, -1)
        cv2.putText(frame, "Blue", (460, 35), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 4)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, f'FPS:{int(fps)}', (550, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 4)
        cv2.putText(frame, "X - Exit", (550, 140), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 4)

        lower = np.array([low[0], low[1], low[2]])
        upper = np.array([up[0], up[1], up[2]])

        mask = cv2.inRange(hsv, lower, upper)
        contour, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(frame, contour, -1, (0, 255, 0), 2)
        mask2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        if contour:
            c = max(contour, key = cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            # cv2.rectangle(frame, (x,y), (x+w, y+h), color, 4)
            cv2.circle(frame, (x,y), 20, color, 2)
            cv2.circle(img, (x,y), 20, color, 2)
            # cv2.rectangle(frame, (x, y), (x+2, y+2), color, 3)


            if (x > 170 and x < 330)and (y > 0 and y< 50):
                color = red
            
            if (x > 340 and x < 500) and (y > 0 and y < 50):
                color = green
            
            if (x > 510 and x < 670) and (y > 0 and y < 50):
                color = blue

            if x < 100 and y < 50:
                ls_red.clear()
                ls_blue.clear()
                ls_green.clear()
        
        if contour:
            if color == red:
                ls_red.append((x, y))
            
            if color == green:
                ls_green.append((x, y))
            
            if color == blue:
                ls_blue.append((x,y))
                
        
    
        if len(ls_green) > 0:
            for i in range(len(ls_green)):
                if ls_green[i][1] > 60:
                    try:
                        d = math.sqrt(math.pow((ls_green[i+1][0] - ls_green[i][0]), 2) + math.pow((ls_green[i+1][1] - ls_green[i][1]),2))
                        if d < 20:
                            cv2.line(frame, (ls_green[i][0], ls_green[i][1]), (ls_green[i+1][0], ls_green[i+1][1]), green, 2)
                            cv2.line(img, (ls_green[i][0], ls_green[i][1]), (ls_green[i+1][0], ls_green[i+1][1]), green, 2)
                        else:
                            cv2.circle(frame,(ls_green[i][0], ls_green[i][1]), 1, green,2)
                            cv2.circle(img,(ls_green[i][0], ls_green[i][1]), 1, green,2)
                    except:
                        cv2.circle(frame,(ls_green[i][0], ls_green[i][1]), 1, green,2)
                        cv2.circle(img,(ls_green[i][0], ls_green[i][1]), 1, green,2)

        if len(ls_red) > 0:
            for i in range(len(ls_red)):
                if ls_red[i][1] > 60:
                    try:
                        d = math.sqrt(math.pow((ls_red[i+1][0] - ls_red[i][0]), 2) + math.pow((ls_red[i+1][1] - ls_red[i][1]),2))
                        if d < 20:
                            cv2.line(frame, (ls_red[i][0], ls_red[i][1]), (ls_red[i+1][0], ls_red[i+1][1]), red, 2)
                            cv2.line(img, (ls_red[i][0], ls_red[i][1]), (ls_red[i+1][0], ls_red[i+1][1]), red, 2)
                        else:
                            cv2.circle(frame,(ls_red[i][0], ls_red[i][1]), 1, red,2)
                            cv2.circle(img,(ls_red[i][0], ls_red[i][1]), 1, red,2)
                    except:
                        cv2.circle(frame,(ls_red[i][0], ls_red[i][1]), 1, red,2)
                        cv2.circle(img,(ls_red[i][0], ls_red[i][1]), 1, red,2)

        if len(ls_blue) > 0:
            for i in range(len(ls_blue)):
                if ls_blue[i][1] > 60:
                    try:
                        d = math.sqrt(math.pow((ls_blue[i+1][0] - ls_blue[i][0]), 2) + math.pow((ls_blue[i+1][1] - ls_blue[i][1]),2))
                        if d < 20:
                            cv2.line(frame, (ls_blue[i][0], ls_blue[i][1]), (ls_blue[i+1][0], ls_blue[i+1][1]), blue, 2)
                            cv2.line(img, (ls_blue[i][0], ls_blue[i][1]), (ls_blue[i+1][0], ls_blue[i+1][1]), blue, 2)
                        else:
                            cv2.circle(frame,(ls_blue[i][0], ls_blue[i][1]), 1, blue,2)
                    except:
                        cv2.circle(frame,(ls_blue[i][0], ls_blue[i][1]), 1, blue,2)
                        cv2.circle(img,(ls_blue[i][0], ls_blue[i][1]), 1, blue,2)

        # blank_image2 = cv2.cvtColor(blank_image2, cv2.COLOR_GRAY2BGR)
        stack = np.hstack((img, frame))
        # stack = np.hstack((frame, frame))
        # vstack = np.hstack((frame,mask2))
        cv2.imshow("Image", stack)

        if cv2.waitKey(10) == ord('x'):
            # cv2.imwrite("aircanvas.png", img)
            ls_blue.clear()
            ls_green.clear()
            ls_red.clear()
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # low = list(map(int, input().split(' ')))
    # up = list(map(int, input().split(' ')))
    air_canvas([82, 117, 119], [161, 243, 185])