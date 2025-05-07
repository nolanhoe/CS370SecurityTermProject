import cv2
import numpy as np
import datetime
from playsound3 import playsound

import smtplib          # Import for sending email
import os               # Import for file path handling
from email.mime.multipart import MIMEMultipart # Import for creating multi-part email
from email.mime.text import MIMEText           # Import for email body text
from email.mime.image import MIMEImage       # Import for attaching images


# Email configuration
SENDER_EMAIL = "nhoefooba@gmail.com"       
SENDER_PASSWORD = "bfzc sire orkw kagc"
RECIPIENT_EMAIL = "nhoefooba@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_alert_email(screenshot_path):
    print(f"SCREENSHOT PATH: {screenshot_path}")
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = "Motion Detected Alert!"

        body = f"Motion was detected by the camera at {str(datetime.datetime.now())[:19]}.\nSee the attached screenshot."
        msg.attach(MIMEText(body, 'plain'))

        for imageItem in screenshot_path:
            if os.path.exists(imageItem):
                with open(imageItem, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(imageItem))
                    msg.attach(img) 
            else: 
                print(f"Warning: Screenshot file not found at {imageItem}")

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
        server.quit()

        print(f"Email alert sent successfully with screenshot: {screenshot_path}")

    except Exception as e:
        print(f"Failed to send email: {e}")



def record():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FPS, 30.0)
    picturelist = []
    t1 = 0
    result1 = 0
    result2 = 0
    i = 0
    cooldown = 75
    while(cam.isOpened()):
        ret, frame = cam.read()
        mean = np.mean(frame)
        result1 = abs(mean - t1)
        if (cooldown == 5 or cooldown == 10 or cooldown == 20):
            picturelist.append(frame)
            if cooldown == 20:
                try:
                    # Generates a timestamped filename 
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    filenames = [f"motion_screenshot_1_{timestamp}.jpg", f"motion_screenshot_2_{timestamp}.jpg", f"motion_screenshot_3_{timestamp}.jpg"]

                    # Save the screenshot
                    for i in range(3):
                        cv2.imwrite(filenames[i], picturelist[i])
                    print(f"Screenshot saved: {filenames[0]}")
                    print(f"Screenshot saved: {filenames[1]}")
                    print(f"Screenshot saved: {filenames[2]}")
                    # Send the email 
                    print("Were Here")
                    send_alert_email(filenames)

                except Exception as e:
                    print(f"Error saving screenshot or sending email: {e}")
                #write all images to email
                picturelist = []
            
        if (cooldown >= 75):
            if ((result1 > 0.75 or result2 > 0.75) and (cooldown >= 100)):
                print(f"Motion detected at {str(datetime.datetime.now())[:19]}")
                

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                cooldown = 0
                playsound("strider.wav", block=False)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        result2 = result1
        t1 = mean
        cooldown += 1
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    record()