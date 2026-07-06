import cv2

from ultralytics import YOLO

from email_alert import email_alert

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#cap = cv2.VideoCapture("uploads/people.mp4")
#cap = cv2.VideoCapture("uploads/Crowd.mp4")

people_count = 0


def generate_frames():

    global people_count

    while True:

        success, frame = cap.read()

        if not success:
            break

        results = model(frame)

        count = 0

        for r in results:

            boxes = r.boxes

            for box in boxes:

                cls = int(box.cls[0])

                conf = float(box.conf[0])

                if cls == 0 and conf > 0.5:

                    count += 1

                    x1,y1,x2,y2 = map(int,box.xyxy[0])

                    cv2.rectangle(
                        frame,
                        (x1,y1),
                        (x2,y2),
                        (0,255,0),
                        2
                    )

                    cv2.putText(
                        frame,
                        "Person",
                        (x1,y1-5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0,255,0),
                        2
                    )

        people_count = count

        cv2.putText(
            frame,
            f"People : {count}",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            2
        )

        if count > 4:
            email_alert.send_email(count)
        else:
            email_alert.reset()

        ret, buffer = cv2.imencode(".jpg",frame)

        frame = buffer.tobytes()

        yield(
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n'
        )






