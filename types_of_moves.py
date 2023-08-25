from body_part_angle import BodyPartAngle
from utils import *

accuracy_him = 0
accuracy_goat = 1
accuracy_legend = 2
accuracy_allstar = 3
accuracy_league = 4

area_right_side_const = 143.0
area_right_arms_const = 132.6


def calculate_accuracy_rating(number):
    if number >= 80.0:
        return accuracy_him
    if number >= 60.0:
        return accuracy_goat
    if number >= 40.0:
        return accuracy_legend
    if number >= 20.0:
        return accuracy_allstar
    return accuracy_league


class TypeOfMove(BodyPartAngle):
    def __init__(self, landmarks):
        super().__init__(landmarks)

    def kobe_fade(self, accuracy, accuracy_number, r_area_arms, r_area_side):
        from utils import detection_body_part

        r_arm_angle = self.angle_of_the_right_arm()
             
        left_elbow = detection_body_part(self.landmarks, "LEFT_ELBOW")
        right_elbow = detection_body_part(self.landmarks, "RIGHT_ELBOW")
        nose = detection_body_part(self.landmarks, "NOSE")
        avg_elbow_y = (left_elbow[1] + right_elbow[1]) / 2
        

        if nose[1] > right_elbow[1] and r_arm_angle > 160:
            r_area_arms = self.angle_of_the_right_area_arms()
            r_area_side = self.angle_of_the_right_area_side()
            r_arms_diff = abs(r_area_arms - area_right_arms_const)
            r_side_diff = abs(r_area_side - area_right_side_const)

            avg = (r_arms_diff + r_side_diff) * 0.5
            accuracy_number = calculate_accuracy_rating(avg)

            print(nose[1], right_elbow[1], r_arm_angle)
            
            return accuracy, accuracy_number, r_area_arms, r_area_side

    def calculate_exercise(self, move_type, context):

        if "accuracy" not in context:
            context["accuracy"] = 0.0
        if "accuracy_num" not in context:
            context["accuracy_num"] = accuracy_league
        if "r_area_side" not in context:
            context["r_area_side"] = 0.0
        if "r_area_arms" not in context:
            context["r_area_arms"] = 0.0

        accuracy = context["accuracy"]
        num = context["accuracy_num"]
        r_area_arms = context["r_area_arms"]
        r_area_side = context["r_area_side"]

        if move_type == "kobe-fade":
            accuracy, num, r_area_arms, r_area_side = self.kobe_fade(accuracy, num, r_area_arms, r_area_side)

        context["accuracy"] = accuracy
        context["accuracy_num"] = num
        context["r_area_arms"] = r_area_arms
        context["r_area_side"] = r_area_side
        return context
