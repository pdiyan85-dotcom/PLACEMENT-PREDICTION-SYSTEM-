def generate_recommendations(
    CGPA,
    Attendance,
    Aptitude,
    Technical,
    Communication,
    Projects,
    Internships,
    Certifications,
    Coding
):
    recommendations = []

    if CGPA < 7:
        recommendations.append("Improve your CGPA through regular academic study.")

    if Attendance < 75:
        recommendations.append("Improve your attendance.")

    if Aptitude < 60:
        recommendations.append("Practice aptitude and logical reasoning questions.")

    if Technical < 60:
        recommendations.append("Improve your technical skills and programming knowledge.")

    if Communication < 60:
        recommendations.append("Improve your communication and interview skills.")

    if Projects < 2:
        recommendations.append("Build more practical projects.")

    if Internships < 1:
        recommendations.append("Try to gain internship or practical work experience.")

    if Certifications < 1:
        recommendations.append("Consider completing relevant technical certifications.")

    if Coding < 60:
        recommendations.append("Practice coding problems regularly.")

    if len(recommendations) == 0:
        recommendations.append("Excellent profile! Keep improving your skills and prepare for interviews.")

    return recommendations