import cv2
import numpy as np

def nothing(x):
    pass

def hsv_color_picker():
    cap  = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow("Trackbars")

    cv2.createTrackbar("Lower - H", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("Lower - S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("Lower - V", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("Upper - H", "Trackbars", 179, 179, nothing)
    cv2.createTrackbar("Upper - S", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("Upper - V", "Trackbars", 255, 255, nothing)

    while True:
        ret, frame = cap.read()
        if ret == None:
            break
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (500,400))

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        l_h = cv2.getTrackbarPos("Lower - H", "Trackbars")
        l_s = cv2.getTrackbarPos("Lower - S", "Trackbars")
        l_v = cv2.getTrackbarPos("Lower - V", "Trackbars")
        u_h = cv2.getTrackbarPos("Upper - H", "Trackbars")
        u_s = cv2.getTrackbarPos("Upper - S", "Trackbars")
        u_v = cv2.getTrackbarPos("Upper - V", "Trackbars")

        lower = np.array([l_h, l_s, l_v])
        upper = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(hsv, lower, upper)
        mask3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        cv2.putText(frame, "press 'X' after selecting", (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(frame, "hsv value", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        stack = np.hstack((frame, mask3))
        cv2.imshow("Trackbars", stack)

        if cv2.waitKey(1) == ord('x'):
            # print(f"lower {lower[0]}, {lower[1]}, {lower[2]}\n upper {upper}")
            break

    cap.release()
    cv2.destroyAllWindows()
    return lower, upper

if __name__ == "__main__":
    l, u = hsv_color_picker()
    print(l, u)
