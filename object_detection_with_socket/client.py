#-*-coding:utf-8-*-
import numpy as np
import cv2
from config import cfg
from utils import SocketAgent

colors = np.random.uniform(0, 255, size=(91, 3))

def draw_result(img, detected):
    font = cv2.FONT_HERSHEY_SIMPLEX
    for res in detected:
        xmin,ymin,xmax,ymax = res["bbox"]
        cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), colors[res["class_idx"]], 2)
        cv2.putText(img, res["class_name"], (int(xmin), int(ymin)+10), font, 0.5, colors[res["class_idx"]], 2, cv2.LINE_AA)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("img")
    counter = 0
    while True:
        ret, img = cap.read()
        if not ret:
            continue

        img = cv2.resize(img, (512, 512))
        sent_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        """setup for socket & send & get"""
        agent = SocketAgent(cfg.server_ip, cfg.port)
        agent.send(sent_img)
        response = agent.get()
        """finished"""

        print("response:")
        print(response)
        draw_result(img, response["data"])
        cv2.imshow("img", img)
        key = cv2.waitKey(0) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
