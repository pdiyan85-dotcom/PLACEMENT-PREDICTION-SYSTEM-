from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from matplotlib import text
from pydantic import BaseModel
import pandas as pd
import numpy as np
import os
import joblib
import io
import re
from pypdf import PdfReader
from docx import Document

# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="Placement Prediction API",
    description="API for predicting student placement status",
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# MODEL PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "MODELS",
    "placement_model.pkl"
)

PREPROCESSOR_PATH = os.path.join(
    BASE_DIR,
    "MODELS",
    "preprocessor.pkl"
)


# ============================================================
# LOAD MODEL AND PREPROCESSOR
# ============================================================

try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)

    print("Model loaded successfully!")
    print("Preprocessor loaded successfully!")

except Exception as e:
    model = None
    preprocessor = None

    print("Error loading model/preprocessor:")
    print(e)


# ============================================================
# INPUT DATA MODEL
# ============================================================

class StudentData(BaseModel):

    age: int
    gender: str
    cgpa: float
    branch: str
    college_tier: str

    internships_count: int
    projects_count: int
    certifications_count: int

    coding_skill_score: float
    aptitude_score: float
    communication_skill_score: float
    logical_reasoning_score: float

    hackathons_participated: int
    github_repos: int
    linkedin_connections: int

    mock_interview_score: float
    attendance_percentage: float
    backlogs: int

    extracurricular_score: float
    leadership_score: float

    volunteer_experience: str

    sleep_hours: float
    study_hours_per_day: float

# ============================================================
# RESUME ASSESSMENT DATA
# ============================================================

class ResumeAssessmentData(BaseModel):

    # Information extracted from resume
    cgpa: float
    internships_count: int
    projects_count: int
    certifications_count: int
    github_repos: int = 0

    # Information provided by student
    attendance_percentage: float
    backlogs: int
    coding_skill_score: float
    aptitude_score: float
    communication_skill_score: float
    logical_reasoning_score: float
    mock_interview_score: float
    hackathons_participated: int

# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Placement Prediction API is running successfully!",
        "status": "online"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "preprocessor_loaded": preprocessor is not None
    }

# ============================================================
# RESUME-BASED PLACEMENT PREDICTION
# ============================================================

@app.post("/predict-resume-placement")
def predict_resume_placement(data: ResumeAssessmentData):

    try:

        # ----------------------------------------------------
        # Create complete student data
        # ----------------------------------------------------
        #
        # These values are used ONLY when the information
        # cannot be obtained from the resume/assessment form.
        # They are not claimed to be extracted from the resume.
        #

        student_data = {

            # Resume / student information
            "age": 22,
            "gender": "Other",
            "cgpa": data.cgpa,
            "branch": "IT",
            "college_tier": "Tier 2",

            # Resume information
            "internships_count": data.internships_count,
            "projects_count": data.projects_count,
            "certifications_count": data.certifications_count,

            # Assessment information
            "coding_skill_score": data.coding_skill_score,
            "aptitude_score": data.aptitude_score,
            "communication_skill_score": data.communication_skill_score,
            "logical_reasoning_score": data.logical_reasoning_score,

            # Resume / assessment information
            "hackathons_participated": data.hackathons_participated,
            "github_repos": data.github_repos,
            "linkedin_connections": 0,

            "mock_interview_score": data.mock_interview_score,
            "attendance_percentage": data.attendance_percentage,
            "backlogs": data.backlogs,

            # Information not available from resume form
            "extracurricular_score": 0,
            "leadership_score": 0,
            "volunteer_experience": "No",

            # These are required by the current trained model
            # because the model was trained with these features.
            "sleep_hours": 7,
            "study_hours_per_day": 3
        }


        # ----------------------------------------------------
        # Convert to DataFrame
        # ----------------------------------------------------

        df = pd.DataFrame([student_data])


        # ----------------------------------------------------
        # Create engineered features
        # ----------------------------------------------------

        df = create_engineered_features(df)


        # ----------------------------------------------------
        # Transform data using saved preprocessor
        # ----------------------------------------------------

        transformed_data = preprocessor.transform(df)


        # ----------------------------------------------------
        # Make prediction
        # ----------------------------------------------------

        prediction = model.predict(transformed_data)[0]


        # ----------------------------------------------------
        # Get probabilities
        # ----------------------------------------------------

        probabilities = model.predict_proba(transformed_data)[0]

        not_placed_probability = float(probabilities[0])
        placed_probability = float(probabilities[1])


        # ----------------------------------------------------
        # Placement status
        # ----------------------------------------------------

        if int(prediction) == 1:

            placement_status = "Placed"

        else:

            placement_status = "Not Placed"


        # ----------------------------------------------------
        # Generate recommendations
        # ----------------------------------------------------

        recommendations = []


        if data.cgpa < 7:
            recommendations.append(
                "Improve your CGPA through consistent academic preparation."
            )

        if data.internships_count == 0:
            recommendations.append(
                "Consider gaining internship or practical industry experience."
            )

        if data.projects_count < 2:
            recommendations.append(
                "Build more practical projects and add them to your portfolio."
            )

        if data.certifications_count == 0:
            recommendations.append(
                "Consider completing relevant technical certifications."
            )

        if data.coding_skill_score < 60:
            recommendations.append(
                "Improve coding skills through regular problem-solving practice."
            )

        if data.aptitude_score < 60:
            recommendations.append(
                "Practice aptitude and quantitative reasoning questions."
            )

        if data.communication_skill_score < 60:
            recommendations.append(
                "Work on communication and interview presentation skills."
            )

        if data.logical_reasoning_score < 60:
            recommendations.append(
                "Practice logical reasoning and analytical problems."
            )

        if data.mock_interview_score < 60:
            recommendations.append(
                "Practice mock interviews to improve interview readiness."
            )

        if data.backlogs > 0:
            recommendations.append(
                "Focus on clearing backlogs and maintaining academic consistency."
            )

        if len(recommendations) == 0:

            recommendations.append(
                "Maintain your current preparation and continue developing "
                "technical and interview skills."
            )


        # ----------------------------------------------------
        # Return result
        # ----------------------------------------------------

        return {

            "success": True,

            "prediction": int(prediction),

            "placement_status": placement_status,

            "placed_probability": round(
                placed_probability * 100, 2
            ),

            "not_placed_probability": round(
                not_placed_probability * 100, 2
            ),

            "recommendations": recommendations,

            "message": "Resume assessment prediction completed successfully."
        }


    except Exception as e:

        return {

            "success": False,

            "message": "Resume prediction failed.",

            "error": str(e)
        }
    
# ============================================================
# FEATURE ENGINEERING
# ============================================================

def create_engineered_features(data):

    # Overall skill score
    data["overall_skill_score"] = (
        data["coding_skill_score"]
        + data["aptitude_score"]
        + data["communication_skill_score"]
        + data["logical_reasoning_score"]
    ) / 4


    # Experience score
    data["experience_score"] = (
        data["internships_count"]
        + data["projects_count"]
        + data["hackathons_participated"]
    )


    # Portfolio score
    data["portfolio_score"] = (
        data["projects_count"]
        + data["github_repos"]
        + data["certifications_count"]
    )


    # Interview readiness
    data["interview_readiness"] = (
        data["mock_interview_score"]
        + data["communication_skill_score"]
        + data["logical_reasoning_score"]
    ) / 3


    # Academic risk
    data["academic_risk"] = (
        data["backlogs"]
        + (10 - data["cgpa"])
    )


    # Engagement score
    data["engagement_score"] = (
        data["attendance_percentage"]
        + data["extracurricular_score"]
        + data["leadership_score"]
    ) / 3


    # Study profile
    data["study_profile"] = (
        data["study_hours_per_day"]
        * data["attendance_percentage"]
        / 100
    )


    return data


# ============================================================
# RECOMMENDATIONS
# ============================================================

def generate_recommendations(data):

    recommendations = []


    if data["cgpa"] < 7:
        recommendations.append(
            "Focus on improving your CGPA and academic performance."
        )


    if data["internships_count"] < 2:
        recommendations.append(
            "Try to gain more internship or practical work experience."
        )


    if data["projects_count"] < 2:
        recommendations.append(
            "Build more practical projects to strengthen your portfolio."
        )


    if data["coding_skill_score"] < 70:
        recommendations.append(
            "Improve your coding and problem-solving skills."
        )


    if data["aptitude_score"] < 70:
        recommendations.append(
            "Practice quantitative, logical and aptitude questions."
        )


    if data["communication_skill_score"] < 70:
        recommendations.append(
            "Work on your communication and interview skills."
        )


    if data["mock_interview_score"] < 70:
        recommendations.append(
            "Practice more mock interviews before placement drives."
        )


    if data["attendance_percentage"] < 75:
        recommendations.append(
            "Try to maintain better attendance."
        )


    if data["backlogs"] > 0:
        recommendations.append(
            "Clear your backlogs as soon as possible."
        )


    if data["github_repos"] < 3:
        recommendations.append(
            "Add more quality projects to your GitHub profile."
        )


    if len(recommendations) == 0:

        recommendations.append(
            "Your profile looks strong. Continue improving your technical and interview skills."
        )


    return recommendations


# ============================================================
# PREDICT PLACEMENT
# ============================================================

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        if not file.filename:
            return {
                "success": False,
                "error": "No file selected."
            }

        file_extension = file.filename.lower().split(".")[-1]

        if file_extension not in ["pdf", "docx"]:
            return {
                "success": False,
                "error": "Only PDF and DOCX files are supported."
            }

        file_content = await file.read()

        if file_extension == "pdf":
            pdf_file = io.BytesIO(file_content)
            reader = PdfReader(pdf_file)

            text = ""

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        elif file_extension == "docx":
            doc_file = io.BytesIO(file_content)
            document = Document(doc_file)

            text = ""

            for paragraph in document.paragraphs:
                text += paragraph.text + "\n"

        text = text.strip()

        if not text:
            return {
                "success": False,
                "error": "Could not extract text from the resume."
            }

        return {
            "success": True,
            "filename": file.filename,
            "message": "Resume uploaded and text extracted successfully.",
            "resume_text": text
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

        # ----------------------------------------------------
        # Convert input into dictionary
        # ----------------------------------------------------

        student_data = student.model_dump()


        # ----------------------------------------------------
        # Convert dictionary into DataFrame
        # ----------------------------------------------------

        df = pd.DataFrame([student_data])


        # ----------------------------------------------------
        # Create engineered features
        # ----------------------------------------------------

        df = create_engineered_features(df)


        # ----------------------------------------------------
        # Process data
        # ----------------------------------------------------

        processed_data = preprocessor.transform(df)


        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        prediction = model.predict(processed_data)[0]


        # ----------------------------------------------------
        # Probability
        # ----------------------------------------------------

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(processed_data)[0]

            not_placed_probability = float(probabilities[0])
            placed_probability = float(probabilities[1])

        else:

            not_placed_probability = None
            placed_probability = None


        # ----------------------------------------------------
        # Placement status
        # ----------------------------------------------------

        if prediction == 1:

            placement_status = "Placed"

        else:

            placement_status = "Not Placed"


        # ----------------------------------------------------
        # Recommendations
        # ----------------------------------------------------

        recommendations = generate_recommendations(student_data)


        # ----------------------------------------------------
        # Return result
        # ----------------------------------------------------

        return {

            "success": True,

            "prediction": int(prediction),

            "placement_status": placement_status,

            "placed_probability": round(
                placed_probability * 100, 2
            ) if placed_probability is not None else None,

            "not_placed_probability": round(
                not_placed_probability * 100, 2
            ) if not_placed_probability is not None else None,

            "recommendations": recommendations

        }


    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }


# ============================================================
# RUN INFORMATION
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "APP.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

    # ============================================================
# RESUME INFORMATION EXTRACTION
# ============================================================

from pydantic import BaseModel
import re


class ResumeText(BaseModel):
    resume_text: str

def extract_resume_information(text):
    """
    Extract structured information from resume text.
    Only extracts information actually found in the resume.
    """

    import re

    # ------------------------------------------------------------
    # EMPTY TEXT
    # ------------------------------------------------------------

    if not text:
        return {
            "name": None,
            "email": None,
            "phone": None,
            "cgpa": None,
            "internships_count": 0,
            "projects_count": 0,
            "certifications_count": 0,
            "github_repos": 0,
            "github_url": None,
            "linkedin": None,
            "technical_skills": [],
            "degree": None,
            "branch": None
        }

    # ------------------------------------------------------------
    # CLEAN TEXT
    # ------------------------------------------------------------

    text = text.replace("\x00", " ")

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    clean_text = " ".join(lines)
    lower_text = clean_text.lower()

    # ------------------------------------------------------------
    # NAME
    # ------------------------------------------------------------

    name = None

    # Common resume section headings that should never be treated
    # as a person's name.
    name_excluded_words = {
        "resume",
        "curriculum vitae",
        "cv",
        "profile",
        "professional summary",
        "summary",
        "objective",
        "experience",
        "professional experience",
        "education",
        "technical skills",
        "skills",
        "projects",
        "project experience",
        "internships",
        "certifications",
        "contact",
        "contact information"
    }

    # Check the first several lines of the resume.
    # Usually the candidate's name is near the top.
    for candidate_line in lines[:15]:

        candidate = candidate_line.strip()

        # Skip empty lines
        if not candidate:
            continue

        candidate_lower = candidate.lower().strip()

        # Skip known headings
        if candidate_lower in name_excluded_words:
            continue

        # Skip lines containing email, URLs or phone numbers
        if re.search(
            r"@|https?://|www\.|linkedin\.com|github\.com|"
            r"\+?\d[\d\s().-]{7,}",
            candidate,
            re.IGNORECASE
        ):
            continue

        # Skip lines containing too many digits
        if len(re.findall(r"\d", candidate)) > 2:
            continue

        # A person's name normally contains alphabetic characters,
        # spaces, dots, apostrophes or hyphens.
        if not re.fullmatch(
            r"[A-Za-zÀ-ÖØ-öø-ÿ.'-]+(?:\s+[A-Za-zÀ-ÖØ-öø-ÿ.'-]+){1,5}",
            candidate
        ):
            continue

        # Avoid long sentences such as professional summaries.
        words = candidate.split()

        if len(words) < 2 or len(words) > 6:
            continue

        # Avoid obvious resume section/content lines.
        excluded_terms = [
            "developer",
            "engineer",
            "specialist",
            "application",
            "full-stack",
            "full stack",
            "software",
            "artificial intelligence",
            "machine learning",
            "technical skills",
            "professional summary"
        ]

        if any(term in candidate_lower for term in excluded_terms):
            continue

        # This is our best candidate.
        name = candidate
        break

    # ------------------------------------------------------------
    # EMAIL
    # ------------------------------------------------------------

    email = None

    email_match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        clean_text
    )

    if email_match:
        email = email_match.group(0)

    # ------------------------------------------------------------
    # PHONE
    # ------------------------------------------------------------

    phone = None

    phone_match = re.search(
        r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",
        clean_text
    )

    if phone_match:
        phone = phone_match.group(0)

    # ------------------------------------------------------------
    # CGPA
    # ------------------------------------------------------------

    cgpa = None

    cgpa_patterns = [
        r"\b(?:cgpa|c\.g\.p\.a|gpa)\s*[:\-]?\s*(\d+(?:\.\d+)?)",
        r"(\d+(?:\.\d+)?)\s*/\s*10\s*(?:cgpa|gpa)?",
        r"\bcumulative\s+gpa\s*[:\-]?\s*(\d+(?:\.\d+)?)"
    ]

    for pattern in cgpa_patterns:

        match = re.search(
            pattern,
            clean_text,
            re.IGNORECASE
        )

        if match:

            try:

                value = float(match.group(1))

                if 0 <= value <= 10:
                    cgpa = value
                    break

            except ValueError:
                pass

        # ------------------------------------------------------------
    # LINKEDIN
    # ------------------------------------------------------------

    linkedin = None

    linkedin_patterns = [
        r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9._%/-]+",
        r"(?:www\.)?linkedin\.com/in/[A-Za-z0-9._%/-]+"
    ]

    for pattern in linkedin_patterns:

        linkedin_match = re.search(
            pattern,
            clean_text,
            re.IGNORECASE
        )

        if linkedin_match:

            linkedin = linkedin_match.group(0)

            if not linkedin.lower().startswith("http"):
                linkedin = "https://" + linkedin

            linkedin = linkedin.rstrip(".,);]")

            break


    # ------------------------------------------------------------
    # GITHUB
    # ------------------------------------------------------------

    github_url = None

    github_patterns = [
        r"https?://(?:www\.)?github\.com/[A-Za-z0-9._-]+",
        r"(?:www\.)?github\.com/[A-Za-z0-9._-]+"
    ]

    for pattern in github_patterns:

        github_match = re.search(
            pattern,
            clean_text,
            re.IGNORECASE
        )

        if github_match:

            github_url = github_match.group(0)

            if not github_url.lower().startswith("http"):
                github_url = "https://" + github_url

            github_url = github_url.rstrip(".,);]")

            break


    # This means a GitHub profile was detected.
    # It does NOT mean the resume contains this many repositories.
    github_repos = 1 if github_url else 0

    # ------------------------------------------------------------
    # DEGREE
    # ------------------------------------------------------------

    degree = None

    degree_patterns = [
        r"\bB\.?\s*Sc\.?\s*IT\b",
        r"\bB\.?\s*Sc\.?\b",
        r"\bB\.?\s*Tech\b",
        r"\bB\.?\s*E\.?\b",
        r"\bBCA\b",
        r"\bMCA\b",
        r"\bM\.?\s*Sc\.?\b",
        r"\bM\.?\s*Tech\b",
        r"\bMBA\b",
        r"\bBBA\b"
    ]

    for pattern in degree_patterns:

        match = re.search(
            pattern,
            clean_text,
            re.IGNORECASE
        )

        if match:
            degree = match.group(0)
            break

    # ------------------------------------------------------------
    # BRANCH
    # ------------------------------------------------------------

    branch = None

    branch_patterns = {
        "IT": [
            r"\binformation technology\b",
            r"\bB\.?\s*Sc\.?\s*IT\b",
            r"\bIT\b"
        ],

        "CSE": [
            r"\bcomputer science\b",
            r"\bcomputer engineering\b",
            r"\bCSE\b"
        ],

        "ECE": [
            r"\belectronics and communication\b",
            r"\belectronics\b",
            r"\bECE\b"
        ],

        "EEE": [
            r"\belectrical and electronics\b",
            r"\belectrical engineering\b",
            r"\bEEE\b"
        ],

        "Mechanical": [
            r"\bmechanical engineering\b",
            r"\bmechanical\b"
        ],

        "Civil": [
            r"\bcivil engineering\b",
            r"\bcivil\b"
        ]
    }

    for branch_name, patterns in branch_patterns.items():

        for pattern in patterns:

            if re.search(
                pattern,
                clean_text,
                re.IGNORECASE
            ):

                branch = branch_name
                break

        if branch:
            break

        # ------------------------------------------------------------
    # INTERNSHIPS
    # ------------------------------------------------------------

    internship_count = len(
        re.findall(
            r"\binternships?\b",
            lower_text
        )
    )

        # ------------------------------------------------------------
    # PROJECTS
    # ------------------------------------------------------------

    project_count = 0

    # Use the original extracted text because PDF/DOCX line
    # structure is important for identifying individual projects.
    resume_lines = [
        re.sub(r"\s+", " ", line).strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # Find the PROJECTS section heading.
    # This works with headings such as:
    # PROJECTS
    # PROJECT EXPERIENCE
    # ACADEMIC PROJECTS
    # PERSONAL PROJECTS
    # FEATURED PRODUCTION AI & WEB PROJECTS

    project_start = None

    for i, line in enumerate(resume_lines):
        normalized_line = line.lower().strip()

        if (
            re.fullmatch(r"projects?", normalized_line)
            or re.fullmatch(r"project experience", normalized_line)
            or re.fullmatch(r"academic projects?", normalized_line)
            or re.fullmatch(r"personal projects?", normalized_line)
            or re.fullmatch(
                r"featured production .* projects?",
                normalized_line
            )
        ):
            project_start = i + 1
            break

    if project_start is not None:

        # Sections that normally come after Projects.
        section_headers = [
            "experience",
            "professional experience",
            "internships",
            "internship",
            "education",
            "certifications",
            "certification",
            "technical skills",
            "skills",
            "achievements",
            "awards",
            "publications",
            "languages"
        ]

        project_end = len(resume_lines)

        for i in range(project_start, len(resume_lines)):
            normalized_line = resume_lines[i].lower().strip()

            if normalized_line in section_headers:
                project_end = i
                break

        project_section_lines = resume_lines[project_start:project_end]

        # --------------------------------------------------------
        # Method 1:
        # Many resumes use:
        #
        # Project Name | Technologies
        #
        # Example:
        # AI Workflow Automation | Python, FastAPI, LangChain
        #
        # Count these as individual projects.
        # --------------------------------------------------------

        pipe_project_lines = []

        for line in project_section_lines:

            # Project title should not normally be a bullet.
            if line.startswith(("•", "-", "*")):
                continue

            if "|" in line:
                left_side = line.split("|", 1)[0].strip()

                # Ignore very short/non-project lines.
                if len(left_side) >= 3:
                    pipe_project_lines.append(line)

        if pipe_project_lines:
            project_count = len(pipe_project_lines)

        else:

            # ----------------------------------------------------
            # Method 2:
            # Numbered project format
            #
            # 1. Project A
            # 2. Project B
            # 3. Project C
            # ----------------------------------------------------

            numbered_projects = []

            for line in project_section_lines:
                if re.match(r"^\d+[\.\)]\s+", line):
                    numbered_projects.append(line)

            if numbered_projects:
                project_count = len(numbered_projects)

            else:

                # ------------------------------------------------
                # Method 3:
                # Project title followed by bullet descriptions.
                #
                # Project A
                # • Description
                # • Description
                #
                # Project B
                # • Description
                # ------------------------------------------------

                for i in range(len(project_section_lines) - 1):

                    current_line = project_section_lines[i]
                    next_line = project_section_lines[i + 1]

                    current_is_bullet = current_line.startswith(
                        ("•", "-", "*")
                    )

                    next_is_bullet = next_line.startswith(
                        ("•", "-", "*")
                    )

                    if not current_is_bullet and next_is_bullet:
                        project_count += 1

    # Make sure the value is an integer.
    project_count = int(project_count)
            
    # ------------------------------------------------------------
    # CERTIFICATIONS
    # ------------------------------------------------------------

    certification_count = 0

    # Look for explicit certification count
    certification_number_match = re.search(
        r"\b(\d+)\s*(?:certifications?|certificates?)\b",
        lower_text,
        re.IGNORECASE
    )

    if certification_number_match:
        certification_count = int(
            certification_number_match.group(1)
        )

    else:
        # Look for a Certifications section
        certification_section_match = re.search(
            r"(?:certifications?|certificates?)\s*[:\-]?\s*(.*?)(?=\n\s*(?:education|experience|projects?|skills|internships?|achievements?)\b|\Z)",
            clean_text,
            re.IGNORECASE | re.DOTALL
        )

        if certification_section_match:
            certification_section = certification_section_match.group(1).strip()

            # Numbered certification entries
            numbered_certifications = re.findall(
                r"(?:^|\n)\s*\d+[\.\)]\s+",
                certification_section
            )

            if numbered_certifications:
                certification_count = len(numbered_certifications)

            else:
                # Bullet certification entries
                bullet_certifications = re.findall(
                    r"(?:^|\n)\s*[-•]\s+",
                    certification_section
                )

                if bullet_certifications:
                    certification_count = len(bullet_certifications)

                elif certification_section:
                    certification_lines = [
                        line.strip()
                        for line in certification_section.splitlines()
                        if line.strip()
                    ]

                    certification_count = min(
                        len(certification_lines),
                        10
                    )
   

    # ------------------------------------------------------------
    # TECHNICAL SKILLS
    # ------------------------------------------------------------

    skill_dictionary = [
        "Python",
        "Java",
        "JavaScript",
        "TypeScript",
        "C",
        "C++",
        "C#",
        "HTML",
        "CSS",
        "React",
        "Next.js",
        "Node.js",
        "Express.js",
        "MongoDB",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "FastAPI",
        "Django",
        "Flask",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Generative AI",
        "GenAI",
        "LLM",
        "NLP",
        "LangChain",
        "LangGraph",
        "Docker",
        "Git",
        "GitHub",
        "AWS",
        "Azure",
        "Power BI"
    ]

    technical_skills = []

    for skill in skill_dictionary:

        if re.search(
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)",
            clean_text,
            re.IGNORECASE
        ):

            technical_skills.append(skill)

    # ------------------------------------------------------------
    # RETURN RESULT
    # ------------------------------------------------------------

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "cgpa": cgpa,
        "internships_count": internship_count,
        "projects_count": project_count,
        "certifications_count": certification_count,
        "github_repos": github_repos,
        "github_url": github_url,
        "linkedin": linkedin,
        "technical_skills": technical_skills,
        "degree": degree,
        "branch": branch
    }

def extract_resume_information(resume_text):

    if not resume_text or not resume_text.strip():
        return {}

    # Clean resume text
    text = resume_text.replace("\r", "\n")
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # =========================================================
    # NAME
    # =========================================================

    name = None

    excluded_words = [
        "resume",
        "curriculum vitae",
        "cv",
        "linkedin",
        "github",
        "portfolio",
        "email",
        "phone",
        "contact",
        "professional summary",
        "summary",
        "technical skills",
        "skills",
        "education",
        "experience",
        "internship",
        "internships",
        "projects",
        "certifications"
    ]

    for line in lines[:15]:

        lower_line = line.lower()

        if "http://" in lower_line or "https://" in lower_line:
            continue

        if "@" in line:
            continue

        if re.search(r"\+?\d[\d\s().-]{8,}", line):
            continue

        if any(word in lower_line for word in excluded_words):
            continue

        words = line.split()

        if 2 <= len(words) <= 5 and len(line) <= 60:

            if re.fullmatch(r"[A-Za-z .'-]+", line):
                name = line
                break

    # =========================================================
    # EMAIL
    # =========================================================

    email = None

    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if email_match:
        email = email_match.group(0)

    # =========================================================
    # PHONE
    # =========================================================

    phone = None

    phone_match = re.search(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    )

    if phone_match:
        phone = phone_match.group(0)

    # =========================================================
    # CGPA / GPA
    # =========================================================

    cgpa = None

    cgpa_match = re.search(
        r"(?:CGPA|GPA)\s*[:\-]?\s*(\d+(?:\.\d+)?)",
        text,
        re.IGNORECASE
    )

    if cgpa_match:
        cgpa = float(cgpa_match.group(1))

    # =========================================================
    # LINKEDIN
    # =========================================================

    linkedin = None

    linkedin_match = re.search(
        r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9._%-]+/?",
        text,
        re.IGNORECASE
    )

    if linkedin_match:
        linkedin = linkedin_match.group(0).rstrip(".,)")

    # =========================================================
    # GITHUB
    # =========================================================

    github_url = None

    github_match = re.search(
        r"https?://(?:www\.)?github\.com/[A-Za-z0-9._-]+/?",
        text,
        re.IGNORECASE
    )

    if github_match:
        github_url = github_match.group(0).rstrip(".,)")

    # =========================================================
    # PORTFOLIO
    # =========================================================

    portfolio_url = None

    all_urls = re.findall(
        r"https?://[^\s<>\"]+",
        text,
        re.IGNORECASE
    )

    for url in all_urls:

        clean_url = url.rstrip(".,)")
        lower_url = clean_url.lower()

        if "linkedin.com" in lower_url:
            continue

        if "github.com" in lower_url:
            continue

        if any(domain in lower_url for domain in [
            "netlify.app",
            "vercel.app",
            "github.io",
            "portfolio"
        ]):
            portfolio_url = clean_url
            break

    # =========================================================
    # DEGREE
    # =========================================================

    degree = None

    degree_patterns = [
        r"B\.?Sc\.?\s*IT",
        r"Bachelor of Science",
        r"B\.?Tech",
        r"M\.?Tech",
        r"M\.?Sc",
        r"B\.?E\.?",
        r"M\.?E\.?",
        r"MBA",
        r"BCA",
        r"MCA"
    ]

    for pattern in degree_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            degree = match.group(0)
            break

    # =========================================================
    # BRANCH
    # =========================================================

    branch = None

    branch_patterns = [
        "computer science",
        "information technology",
        "artificial intelligence",
        "data science",
        "computer engineering",
        "electronics",
        "mechanical",
        "civil"
    ]

    lower_text = text.lower()

    for branch_name in branch_patterns:

        if branch_name in lower_text:
            branch = branch_name.title()
            break

    # =========================================================
    # INTERNSHIPS
    # =========================================================

    internships_count = 0

    for line in lines:

        lower_line = line.lower()

        if "intern" in lower_line:

            if lower_line not in [
                "internship",
                "internships",
                "internships & professional experience"
            ]:

                internships_count += 1

    internships_count = min(internships_count, 10)

    # =========================================================
    # PROJECTS
    # =========================================================

    projects_count = 0

    project_section = False

    for line in lines:

        lower_line = line.lower()

        if "featured production" in lower_line and "project" in lower_line:
            project_section = True
            continue

        if lower_line in [
            "projects",
            "project",
            "featured projects"
        ]:
            project_section = True
            continue

        if project_section:

            if lower_line in [
                "internships & professional experience",
                "experience",
                "education",
                "education & certifications",
                "certifications"
            ]:
                break

            if "|" in line or "—" in line:
                projects_count += 1

    projects_count = min(projects_count, 20)

    # =========================================================
    # CERTIFICATIONS
    # =========================================================

    certifications_count = 0

    for line in lines:

        lower_line = line.lower()

        if (
            "certification" in lower_line
            or "certified" in lower_line
            or "certificate" in lower_line
        ):

            if lower_line not in [
                "certification",
                "certifications",
                "education & certifications"
            ]:

                certifications_count += 1

    certifications_count = min(certifications_count, 20)

    # =========================================================
    # TECHNICAL SKILLS
    # =========================================================

    skill_list = [
        "Python",
        "SQL",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "Node.js",
        "Express",
        "FastAPI",
        "PostgreSQL",
        "MongoDB",
        "MySQL",
        "Pandas",
        "NumPy",
        "PyTorch",
        "TensorFlow",
        "Scikit-learn",
        "LangChain",
        "LangGraph",
        "FAISS",
        "Hugging Face",
        "Docker",
        "Git",
        "GitHub",
        "MLflow",
        "RAG",
        "LoRA",
        "n8n"
    ]

    technical_skills = []

    for skill in skill_list:

        if re.search(
            r"\b" + re.escape(skill) + r"\b",
            text,
            re.IGNORECASE
        ):

            technical_skills.append(skill)

    # =========================================================
    # FINAL RESULT
    # =========================================================

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "cgpa": cgpa,
        "internships_count": internships_count,
        "projects_count": projects_count,
        "certifications_count": certifications_count,
        "github_repos": 1 if github_url else 0,
        "github_url": github_url,
        "linkedin": linkedin,
        "portfolio_url": portfolio_url,
        "technical_skills": technical_skills,
        "degree": degree,
        "branch": branch
    }

# ============================================================
# EXTRACT RESUME DATA API
# ============================================================

@app.post("/extract-resume-data")
def extract_resume_data(data: ResumeText):

    try:

        if not data.resume_text.strip():

            return {
                "success": False,
                "error": "Resume text is empty."
            }


        extracted_data = extract_resume_information(
            data.resume_text
        )


        return {
            "success": True,
            "message": "Resume information extracted successfully.",
            "data": extracted_data
        }


    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
        
@app.post("/predict-placement")
def predict_placement(data: StudentData):

    try:

        # Convert request data to dictionary
        student_data = data.model_dump()

        # Create DataFrame
        df = pd.DataFrame([student_data])

        # Create engineered features
        df = create_engineered_features(df)

        # Preprocess the data
        X_processed = preprocessor.transform(df)

        # Make prediction
        prediction = model.predict(X_processed)[0]

        # Get prediction probabilities
        probabilities = model.predict_proba(X_processed)[0]

        # Probability of placed
        placed_probability = float(
            probabilities[1] * 100
        )

        # Probability of not placed
        not_placed_probability = float(
            probabilities[0] * 100
        )

        # Convert prediction to readable status
        placement_status = (
            "Placed"
            if prediction == 1
            else "Not Placed"
        )

        # Generate recommendations
        recommendations = generate_recommendations(
            student_data
        )

        # Return prediction result
        return {
            "success": True,
            "prediction": int(prediction),
            "placement_status": placement_status,
            "placed_probability": round(
                placed_probability,
                2
            ),
            "not_placed_probability": round(
                not_placed_probability,
                2
            ),
            "recommendations": recommendations
        }

    except Exception as e:

        print(
            "Prediction error:",
            str(e)
        )

        return {
            "success": False,
            "error": str(e)
        }