import cv2


class Text(object):

    def printOnVideo(self, left, right, nose, calibration, opening, border, coordinates):
        if calibration:
            cv2.putText(self, "Left pupil:  " + str(left), (15, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)
            cv2.putText(self, "Right pupil: " + str(right), (15, 55), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)
            cv2.putText(self, "Nose: " + str(nose), (15, 80), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

            if border:
                cv2.circle(self, coordinates[0], 1, (0, 255, 255), -1)
                cv2.circle(self, coordinates[0], 4, (0, 255, 255), 1)

                cv2.circle(self, coordinates[1], 1, (0, 255, 255), -1)
                cv2.circle(self, coordinates[1], 4, (0, 255, 255), 1)

                cv2.circle(self, coordinates[2], 1, (0, 255, 255), -1)
                cv2.circle(self, coordinates[2], 4, (0, 255, 255), 1)

            if opening:
                cv2.putText(self, "Click is open", (20, 460), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 1)
            else:
                cv2.putText(self, "Click is close", (20, 460), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 1)

        else:
            cv2.putText(self, "Calibration is taking place, press Enter when ready", (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 1)
            cv2.putText(self, "Calibration is taking place, press Enter when ready", (20, 460), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 2551), 1)
