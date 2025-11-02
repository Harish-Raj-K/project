# main.py

from model.classifier import predict_student_level

def analyze_student(course, text):
    """
    Analyzes a student's skill level for a specific course.

    Parameters:
        course (str): The selected course name. One of:
                      ["Python", "GEN AI", "Data Science", "Full Stack"]
        text (str): Combined response from the student's answers.

    Returns:
        int: Predicted skill level (1 = Beginner, 2 = Intermediate, 3 = Advanced)
    """
    return predict_student_level(course, text)
