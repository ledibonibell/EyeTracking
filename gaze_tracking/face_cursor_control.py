import pyautogui


class MouseController:

    def click(self):
        if self:
            pyautogui.click()

    def move_mouse(self, initial_coordinates):
        initial_left_eye, initial_right_eye, initial_nose = initial_coordinates
        real_left_eye, real_right_eye, real_nose = self

        if real_nose is not None and real_left_eye is not None and real_right_eye is not None:
            real_x = (real_nose[0] + (real_left_eye[0] + real_right_eye[0]) / 2) / 2
            real_y = (real_nose[1] + (real_left_eye[1] + real_right_eye[1]) / 2) / 2

            center_x = (initial_nose[0] + (initial_left_eye[0] + initial_right_eye[0]) / 2) / 2
            center_y = (initial_nose[1] + (initial_left_eye[1] + initial_right_eye[1]) / 2) / 2

            delta_x = center_x - real_x
            delta_y = real_y - center_y

            if abs(delta_x) > 2 and abs(delta_y) > 2:
                current_x, current_y = pyautogui.position()
                new_x, new_y = current_x + delta_x, current_y + delta_y
                pyautogui.moveTo(new_x, new_y)

