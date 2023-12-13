import cv2
from gaze_tracking import GazeTracking
from gaze_tracking.eye_tracking import NoseTracking, BlinkTracking
from gaze_tracking.output_text import Text
from gaze_tracking.face_cursor_control import MouseController


nose = NoseTracking()
eyes = BlinkTracking()
gaze = GazeTracking()
mouse = MouseController
webcam = cv2.VideoCapture(0)

calibration = False
coordinates = None
opening = False
face_cursor_control = None
border = True
check = [False, False]

while True:
    _, frame = webcam.read()
    flag = False
    check = eyes._check_blink()

    gaze.refresh(frame)
    nose.refresh(frame)
    if calibration:
        eyes.refresh(frame)

    frame = gaze.annotated_frame()

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    nose_coord = nose.nose_coords()
    real_coordinates = [left_pupil, right_pupil, nose_coord]

    Text.printOnVideo(frame, left_pupil, right_pupil, nose_coord, calibration, opening, border, coordinates)

    cv2.imshow("Demo", frame)

    if eyes.has_required_blinks_in_timeout():
        opening = not opening
        print("Blinked three times within the specified timeout!")
        print(opening)
        if check[0] and check[1]:
            # print(check)
            flag = True
            mouse.click(flag)

    if cv2.waitKey(1) == 13:
        coordinates = [left_pupil, right_pupil, nose_coord]
        print("Left pupil -", coordinates[0], "\nRight pupil -", coordinates[1], "\nNose -", coordinates[2])
        if coordinates[0] and coordinates[1] and coordinates[2]:
            calibration = True

    if cv2.waitKey(5) == 9:
        border = not border

    if calibration:
        mouse.move_mouse(real_coordinates, coordinates)

    if cv2.waitKey(10) == 27:
        break

webcam.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
