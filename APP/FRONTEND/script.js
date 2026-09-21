// ============================================================
// PLACEMENT PREDICTION SYSTEM - FRONTEND INITIALIZATION
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("Frontend JavaScript initialized.");

    // ------------------------------------------------------------
    // BASIC ELEMENTS
    // ------------------------------------------------------------

    const navItems =
        document.querySelectorAll(".nav-item");

    const pages =
        document.querySelectorAll(".page");

    const pageTitle =
        document.getElementById("pageTitle");


    // ------------------------------------------------------------
    // PAGE NAVIGATION
    // ------------------------------------------------------------

    function showPage(pageName) {

        console.log("Opening page:", pageName);

        // Hide all pages
        pages.forEach(function (page) {

            page.classList.remove("active-page");

        });


        // Show selected page
        const selectedPage =
            document.getElementById(
                pageName + "Page"
            );


        if (selectedPage) {

            selectedPage.classList.add(
                "active-page"
            );

            console.log(
                "Page opened successfully:",
                pageName
            );

        } else {

            console.error(
                "Page not found:",
                pageName + "Page"
            );

            return;

        }


        // Update sidebar active item
        navItems.forEach(function (item) {

            item.classList.remove("active");

            if (
                item.getAttribute("data-page")
                === pageName
            ) {

                item.classList.add("active");

            }

        });


        // Update page title
        const titles = {

            dashboard: "Dashboard",

            assessment:
                "Student Assessment",

            resume:
                "Resume Analysis",

            analysis:
                "Student Analysis",

            history:
                "Assessment History",

            models:
                "ML Models",

            about:
                "About Project"

        };


        if (pageTitle) {

            pageTitle.textContent =
                titles[pageName]
                || "Dashboard";

        }

    }


    // ------------------------------------------------------------
    // SIDEBAR NAVIGATION
    // ------------------------------------------------------------

    navItems.forEach(function (item) {

        item.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                const pageName =
                    item.getAttribute(
                        "data-page"
                    );

                console.log(
                    "Sidebar clicked:",
                    pageName
                );

                if (pageName) {

                    showPage(pageName);

                }

            }
        );

    });


    // ------------------------------------------------------------
    // QUICK ACTION CARDS
    // ------------------------------------------------------------

    const quickCards =
        document.querySelectorAll(
            ".quick-card"
        );


    quickCards.forEach(function (card) {

        card.addEventListener(
            "click",
            function () {

                const pageName =
                    card.getAttribute(
                        "data-page"
                    );

                console.log(
                    "Quick action clicked:",
                    pageName
                );

                if (pageName) {

                    showPage(pageName);

                }

            }
        );

    });


    // ------------------------------------------------------------
    // START DASHBOARD
    // ------------------------------------------------------------

    showPage("dashboard");

});

document.addEventListener("DOMContentLoaded", function () {

    // ============================================================
    // API URL
    // ============================================================

    const API_URL = "http://127.0.0.1:8000";


    // ============================================================
    // GET HTML ELEMENTS
    // ============================================================

    const navItems = document.querySelectorAll(".nav-item");
    const pages = document.querySelectorAll(".page");
    const pageTitle = document.getElementById("pageTitle");

    const resumeFile = document.getElementById("resumeFile");
    const browseResumeButton = document.getElementById("browseResumeButton");
    const resumeUploadArea = document.getElementById("resumeUploadArea");
    const selectedResume = document.getElementById("selectedResume");
    const analyzeResumeButton = document.getElementById("analyzeResumeButton");

    const predictionForm = document.getElementById("predictionForm");
    const newPredictionButton = document.getElementById("newPredictionButton");

    const clearHistoryButton = document.getElementById("clearHistoryButton");
    const clearHistoryButtonMain = document.getElementById("clearHistoryButtonMain");


    // ============================================================
    // PAGE NAVIGATION
    // ============================================================

   function showPage(pageName) {

    console.log("Opening page:", pageName);

    // Hide all pages
    pages.forEach(function (page) {
        page.classList.remove("active-page");
    });

    // Show selected page
    const selectedPage =
        document.getElementById(pageName + "Page");

    if (selectedPage) {
        selectedPage.classList.add("active-page");

        console.log(
            "Page opened successfully:",
            pageName
        );
    } else {
        console.error(
            "Page not found:",
            pageName + "Page"
        );
    }

    // Update sidebar
    navItems.forEach(function (item) {

        item.classList.remove("active");

        if (
            item.getAttribute("data-page") === pageName
        ) {
            item.classList.add("active");
        }

    });

    // Page titles
    const titles = {
        dashboard: "Dashboard",
        assessment: "Student Assessment",
        resume: "Resume Analysis",
        analysis: "Student Analysis",
        history: "Assessment History",
        models: "ML Models",
        about: "About Project"
    };

    if (pageTitle) {
        pageTitle.textContent =
            titles[pageName] || "Dashboard";
    }


    // ========================================================
    // REFRESH PAGE DATA
    // ========================================================

    if (pageName === "history") {

        console.log(
            "Refreshing assessment history..."
        );

        updateHistory();

    }

    if (pageName === "dashboard") {

        updateDashboard();

    }

}


    // ============================================================
    // RESUME UPLOAD
    // ============================================================

    console.log("Resume upload system initialized.");


    // ------------------------------------------------------------
    // CHOOSE RESUME BUTTON
    // ------------------------------------------------------------

    if (browseResumeButton && resumeFile) {

        browseResumeButton.addEventListener("click", function (event) {

            event.preventDefault();

            console.log("Choose Resume button clicked.");

            resumeFile.click();

        });

    }


    // ------------------------------------------------------------
    // FILE INPUT CHANGE
    // ------------------------------------------------------------

    if (resumeFile) {

        resumeFile.addEventListener("change", function () {

            console.log("File input changed.");

            if (!resumeFile.files || resumeFile.files.length === 0) {

                console.log("No file selected.");

                return;

            }

            const file = resumeFile.files[0];

            console.log("Selected file:", file.name);
            console.log("File size:", file.size);
            console.log("File type:", file.type);

            validateAndDisplayResume(file);

        });

    }


    // ============================================================
    // VALIDATE RESUME
    // ============================================================

   function validateAndDisplayResume (file) {

        if (!file) {

            alert("Please select a resume.");

            return;

        }


        const fileName = file.name.toLowerCase();

        const isPDF = fileName.endsWith(".pdf");
        const isDOCX = fileName.endsWith(".docx");


        if (!isPDF && !isDOCX) {

            alert("Invalid file format.\n\nPlease upload a PDF or DOCX resume.");

            if (resumeFile) {
                resumeFile.value = "";
            }

            return;

        }


        // Maximum size: 10 MB
        const maxSize = 10 * 1024 * 1024;

        if (file.size > maxSize) {

            alert("File is too large.\n\nMaximum allowed size is 10 MB.");

            if (resumeFile) {
                resumeFile.value = "";
            }

            return;

        }


        displaySelectedResume(file);

    }


    // ============================================================
    // DISPLAY SELECTED RESUME
    // ============================================================

    function displaySelectedResume(file) {

        if (!selectedResume) {
            return;
        }


        selectedResume.innerHTML = `
            <div class="selected-file">
                <div>
                    <strong>${escapeHTML(file.name)}</strong>
                    <br>
                    <small>${formatFileSize(file.size)}</small>
                </div>

                <button
                    type="button"
                    id="removeResumeButton"
                    class="secondary-button">
                    Remove
                </button>
            </div>
        `;


        if (analyzeResumeButton) {

            analyzeResumeButton.disabled = false;

        }


        const removeButton =
            document.getElementById("removeResumeButton");


        if (removeButton) {

            removeButton.addEventListener("click", function () {

                removeResume();

            });

        }

    }


    // ============================================================
    // REMOVE RESUME
    // ============================================================

    function removeResume() {

        console.log("Removing selected resume.");

        if (resumeFile) {
            resumeFile.value = "";
        }

        if (selectedResume) {

            selectedResume.innerHTML = `
                <p>No resume selected.</p>
            `;

        }

        if (analyzeResumeButton) {

            analyzeResumeButton.disabled = true;

        }

        sessionStorage.removeItem("extractedResumeText");
        sessionStorage.removeItem("resumeFileName");
        sessionStorage.removeItem("extractedStudentData");

    }


    // ============================================================
    // DRAG AND DROP
    // ============================================================

    if (resumeUploadArea) {

        resumeUploadArea.addEventListener(
            "dragover",
            function (event) {

                event.preventDefault();

                resumeUploadArea.classList.add("drag-over");

            }
        );


        resumeUploadArea.addEventListener(
            "dragleave",
            function () {

                resumeUploadArea.classList.remove("drag-over");

            }
        );


        resumeUploadArea.addEventListener(
            "drop",
            function (event) {

                event.preventDefault();

                resumeUploadArea.classList.remove("drag-over");

                console.log("Resume dropped.");

                const files = event.dataTransfer.files;

                if (!files || files.length === 0) {

                    return;

                }


                const file = files[0];

                console.log("Dropped file:", file.name);

                validateAndDisplayResume(file);


                // Put dropped file into input
                if (resumeFile) {

                    try {

                        const dataTransfer = new DataTransfer();

                        dataTransfer.items.add(file);

                        resumeFile.files = dataTransfer.files;

                    } catch (error) {

                        console.warn(
                            "Could not assign dropped file to input:",
                            error
                        );

                    }

                }

            }
        );

    }


    // ============================================================
    // ANALYZE RESUME BUTTON
    // ============================================================

    if (analyzeResumeButton) {

        analyzeResumeButton.addEventListener(
            "click",
            async function (event) {

                event.preventDefault();

                console.log("=================================");
                console.log("ANALYZE RESUME STARTED");
                console.log("=================================");


                try {

                    // ------------------------------------------------
                    // CHECK FILE
                    // ------------------------------------------------

                    if (
                        !resumeFile ||
                        !resumeFile.files ||
                        resumeFile.files.length === 0
                    ) {

                        alert("Please select a resume first.");

                        return;

                    }


                    const file = resumeFile.files[0];

                    console.log("File ready for upload:", file.name);
                    console.log("File size:", file.size);
                    console.log("File type:", file.type);


                    // ------------------------------------------------
                    // VALIDATE FILE AGAIN
                    // ------------------------------------------------

                    const fileName =
                        file.name.toLowerCase();


                    if (
                        !fileName.endsWith(".pdf") &&
                        !fileName.endsWith(".docx")
                    ) {

                        alert(
                            "Only PDF and DOCX files are supported."
                        );

                        return;

                    }


                    // ------------------------------------------------
                    // BUTTON LOADING
                    // ------------------------------------------------

                    analyzeResumeButton.disabled = true;

                    analyzeResumeButton.textContent =
                        "Uploading Resume...";


                    // ------------------------------------------------
                    // CREATE FORMDATA
                    // ------------------------------------------------

                    const formData = new FormData();

                    formData.append("file", file);


                    console.log(
                        "FormData created."
                    );

                    console.log(
                        "Uploading to:",
                        API_URL + "/upload-resume"
                    );


                    // ------------------------------------------------
                    // UPLOAD RESUME TO FASTAPI
                    // ------------------------------------------------

                    const uploadResponse =
                        await fetch(
                            API_URL + "/upload-resume",
                            {
                                method: "POST",
                                body: formData
                            }
                        );


                    console.log(
                        "Upload HTTP status:",
                        uploadResponse.status
                    );


                    // ------------------------------------------------
                    // READ RESPONSE
                    // ------------------------------------------------

                    const responseText =
                        await uploadResponse.text();


                    console.log(
                        "Raw server response:",
                        responseText
                    );


                    if (!uploadResponse.ok) {

                        throw new Error(
                            "Server returned HTTP " +
                            uploadResponse.status +
                            "\n\n" +
                            responseText
                        );

                    }


                    let uploadResult;


                    try {

                        uploadResult =
                            JSON.parse(responseText);

                    } catch (error) {

                        throw new Error(
                            "FastAPI returned an invalid JSON response.\n\n" +
                            responseText
                        );

                    }


                    console.log(
                        "Upload result:",
                        uploadResult
                    );


                    // ------------------------------------------------
                    // CHECK SUCCESS
                    // ------------------------------------------------

                    if (!uploadResult.success) {

                        throw new Error(
                            uploadResult.message ||
                            "Resume upload failed."
                        );

                    }


                    // ------------------------------------------------
                    // SAVE RESUME TEXT
                    // ------------------------------------------------

                    const resumeText =
                        uploadResult.resume_text || "";


                    sessionStorage.setItem(
                        "extractedResumeText",
                        resumeText
                    );


                    sessionStorage.setItem(
                        "resumeFileName",
                        uploadResult.filename ||
                        file.name
                    );


                    console.log(
                        "Resume text extracted."
                    );


                    // ------------------------------------------------
                    // UPDATE BUTTON
                    // ------------------------------------------------

                    analyzeResumeButton.textContent =
                        "Extracting Information...";


                    // ------------------------------------------------
                    // EXTRACT RESUME INFORMATION
                    // ------------------------------------------------

                    console.log(
                        "Calling /extract-resume-data..."
                    );


                    const extractResponse =
                        await fetch(
                            API_URL +
                            "/extract-resume-data",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify({
                                    resume_text:
                                        resumeText
                                })
                            }
                        );


                    console.log(
                        "Extraction HTTP status:",
                        extractResponse.status
                    );


                    const extractText =
                        await extractResponse.text();


                    console.log(
                        "Extraction response:",
                        extractText
                    );


                    if (!extractResponse.ok) {

                        throw new Error(
                            "Resume information extraction failed.\n\n" +
                            "HTTP " +
                            extractResponse.status +
                            "\n\n" +
                            extractText
                        );

                    }


                    let extractResult;


                    try {

                        extractResult =
                            JSON.parse(extractText);

                    } catch (error) {

                        throw new Error(
                            "Invalid JSON from extraction API.\n\n" +
                            extractText
                        );

                    }


                    console.log(
                        "Extracted information:",
                        extractResult
                    );


                    // ------------------------------------------------
                    // CHECK EXTRACTION
                    // ------------------------------------------------

                    if (!extractResult.success) {

                        throw new Error(
                            extractResult.message ||
                            "Could not extract information from resume."
                        );

                    }


                    // ------------------------------------------------
                    // SAVE DATA
                    // ------------------------------------------------

                    const studentData =
                        extractResult.data || {};


                    sessionStorage.setItem(
                        "extractedStudentData",
                        JSON.stringify(studentData)
                    );
                    displayResumeAnalysis();

                    // ------------------------------------------------
                    // SHOW SUCCESS MESSAGE
                    // ------------------------------------------------

                    let message =
                        "Resume uploaded and analyzed successfully!\n\n";


                    message +=
                        "File: " +
                        (uploadResult.filename ||
                        file.name) +
                        "\n\n";


                    message +=
                        "Extracted Information:\n";


                    message +=
                        "CGPA: " +
                        displayValue(studentData.cgpa) +
                        "\n";


                    message +=
                        "Internships: " +
                        displayValue(
                            studentData.internships_count
                        ) +
                        "\n";


                    message +=
                        "Projects: " +
                        displayValue(
                            studentData.projects_count
                        ) +
                        "\n";


                    message +=
                        "Certifications: " +
                        displayValue(
                            studentData.certifications_count
                        ) +
                        "\n";


                    message +=
                        "GitHub: " +
                        displayValue(
                            studentData.github_repos
                        ) +
                        "\n";


                    message +=
                        "LinkedIn: " +
                        displayValue(
                            studentData.linkedin
                        ) +
                        "\n";


                    message +=
                        "Degree: " +
                        displayValue(
                            studentData.degree
                        ) +
                        "\n";


                    message +=
                        "Branch: " +
                        displayValue(
                            studentData.branch
                        );


                    alert(message);


                    console.log(
                        "================================="
                    );

                    console.log(
                        "RESUME ANALYSIS COMPLETED"
                    );

                    console.log(
                        "================================="
                    );


                    // ------------------------------------------------
                    // GO TO STUDENT ANALYSIS
                    // ------------------------------------------------

                    showPage("analysis");


                } catch (error) {

                    console.error(
                        "================================="
                    );

                    console.error(
                        "RESUME UPLOAD ERROR"
                    );

                    console.error(
                        error
                    );

                    console.error(
                        "================================="
                    );


                    alert(
                        "Resume upload failed.\n\n" +
                        error.message +
                        "\n\n" +
                        "Please check the browser Console (F12)."
                    );

                } finally {

                    if (analyzeResumeButton) {

                        analyzeResumeButton.disabled = false;

                        analyzeResumeButton.textContent =
                            "🔍 Analyze Resume";

                    }

                }

            }
        );

    }

// ============================================================
// MANUAL PREDICTION
// ============================================================

if (predictionForm) {

    predictionForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        console.log("=================================");
        console.log("PREDICT PLACEMENT BUTTON CLICKED");
        console.log("=================================");

        const loading =
            document.getElementById("loading");

        const result =
            document.getElementById("result");

        if (loading) {
            loading.style.display = "block";
        }

        if (result) {
            result.style.display = "none";
        }

        try {

            // ====================================================
            // GET FORM VALUES
            // ====================================================

            const studentData = {

                age: Number(
                    document.getElementById("age").value
                ),

                gender:
                    document.getElementById("gender").value,

                cgpa: Number(
                    document.getElementById("cgpa").value
                ),

                branch:
                    document.getElementById("branch").value,

                college_tier:
                    document.getElementById("college_tier").value,

                internships_count: Number(
                    document.getElementById("internships_count").value
                ),

                projects_count: Number(
                    document.getElementById("projects_count").value
                ),

                certifications_count: Number(
                    document.getElementById("certifications_count").value
                ),

                coding_skill_score: Number(
                    document.getElementById("coding_skill_score").value
                ),

                aptitude_score: Number(
                    document.getElementById("aptitude_score").value
                ),

                communication_skill_score: Number(
                    document.getElementById("communication_skill_score").value
                ),

                logical_reasoning_score: Number(
                    document.getElementById("logical_reasoning_score").value
                ),

                hackathons_participated: Number(
                    document.getElementById("hackathons_participated").value
                ),

                github_repos: Number(
                    document.getElementById("github_repos").value
                ),

                linkedin_connections: Number(
                    document.getElementById("linkedin_connections").value
                ),

                mock_interview_score: Number(
                    document.getElementById("mock_interview_score").value
                ),

                attendance_percentage: Number(
                    document.getElementById("attendance_percentage").value
                ),

                backlogs: Number(
                    document.getElementById("backlogs").value
                ),

                extracurricular_score: Number(
                    document.getElementById("extracurricular_score").value
                ),

                leadership_score: Number(
                    document.getElementById("leadership_score").value
                ),

                volunteer_experience:
                    document.getElementById("volunteer_experience").value,

                // Required by the trained model
                sleep_hours: 7,

                study_hours_per_day: 3
            };


            // ====================================================
            // SHOW DATA IN CONSOLE
            // ====================================================

            console.log(
                "DATA BEING SENT TO FASTAPI:"
            );

            console.log(
                JSON.stringify(
                    studentData,
                    null,
                    2
                )
            );


            // ====================================================
            // SEND REQUEST
            // ====================================================

            const response =
                await fetch(
                    API_URL + "/predict-placement",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                studentData
                            )
                    }
                );


            console.log(
                "API STATUS:",
                response.status
            );


            const responseText =
                await response.text();


            console.log(
                "API RESPONSE:",
                responseText
            );


            // ====================================================
            // CHECK RESPONSE
            // ====================================================

            if (!response.ok) {

                throw new Error(
                    "HTTP " +
                    response.status +
                    "\n\n" +
                    responseText
                );

            }


            const data =
                JSON.parse(
                    responseText
                );


            console.log(
                "FINAL PREDICTION:",
                data
            );


            if (!data.success) {

                throw new Error(
                    data.error ||
                    data.message ||
                    "Prediction failed."
                );

            }


            // ====================================================
            // DISPLAY RESULT
            // ====================================================

            const predictionStatus =
                document.getElementById(
                    "predictionStatus"
                );

            const placedProbability =
                document.getElementById(
                    "placedProbability"
                );

            const notPlacedProbability =
                document.getElementById(
                    "notPlacedProbability"
                );

            const recommendationsList =
                document.getElementById(
                    "recommendationsList"
                );


            if (predictionStatus) {

                predictionStatus.textContent =
                    data.placement_status;

            }


            if (placedProbability) {

                placedProbability.textContent =
                    Number(
                        data.placed_probability || 0
                    ).toFixed(2) + "%";

            }


            if (notPlacedProbability) {

                notPlacedProbability.textContent =
                    Number(
                        data.not_placed_probability || 0
                    ).toFixed(2) + "%";

            }


            // ====================================================
            // RECOMMENDATIONS
            // ====================================================

            if (recommendationsList) {

                recommendationsList.innerHTML = "";

                const recommendations =
                    data.recommendations || [];


                recommendations.forEach(
                    function (recommendation) {

                        const li =
                            document.createElement(
                                "li"
                            );

                        li.textContent =
                            recommendation;

                        recommendationsList.appendChild(
                            li
                        );

                    }
                );

            }


            // ====================================================
            // SHOW RESULT
            // ====================================================

            if (result) {

                result.style.display =
                    "block";

            }


            // ====================================================
            // SAVE HISTORY
            // ====================================================

            saveAssessment(
                data,
                studentData
            );

            updateDashboard();

            updateHistory();


            console.log(
                "PREDICTION COMPLETED SUCCESSFULLY"
            );


        } catch (error) {

            console.error(
                "PREDICTION ERROR:",
                error
            );


            alert(
                "Prediction failed.\n\n" +
                error.message
            );


        } finally {

            if (loading) {

                loading.style.display =
                    "none";

            }

        }

    });

}
    
    // ============================================================
    // NEW PREDICTION
    // ============================================================

    if (newPredictionButton) {

        newPredictionButton.addEventListener(
            "click",
            function () {

                if (predictionForm) {

                    predictionForm.reset();

                }


                const result =
                    document.getElementById("result");


                if (result) {

                    result.style.display =
                        "none";

                }


                showPage("assessment");

            }
        );

    }


    function saveAssessment(result, studentData) {

    console.log("=== SAVING PREDICTION HISTORY ===");

    try {

        let history = JSON.parse(
            localStorage.getItem("assessmentHistory") || "[]"
        );

        const record = {
            id: Date.now(),
            date: new Date().toLocaleString(),

            status:
                result.placement_status ||
                result.prediction ||
                "Unknown",

            placed_probability:
                Number(result.placed_probability || 0),

            not_placed_probability:
                Number(result.not_placed_probability || 0),

            student: studentData || {}
        };

        history.unshift(record);

        localStorage.setItem(
            "assessmentHistory",
            JSON.stringify(history)
        );

        console.log("Prediction saved:", record);
        console.log(
            "History saved:",
            localStorage.getItem("assessmentHistory")
        );

    } catch (error) {

        console.error(
            "History save error:",
            error
        );

    }
}

    // ============================================================
    // DASHBOARD
    // ============================================================

    function updateDashboard() {

        const history =
            JSON.parse(
                localStorage.getItem(
                    "assessmentHistory"
                ) || "[]"
            );


        const total =
            document.getElementById(
                "totalAssessments"
            );


        const placed =
            document.getElementById(
                "placedAssessments"
            );


        const notPlaced =
            document.getElementById(
                "notPlacedAssessments"
            );


        const average =
            document.getElementById(
                "averageProbability"
            );


        if (total) {

            total.textContent =
                history.length;

        }


        const placedCount =
            history.filter(
                function (item) {

                    return item.status === "Placed";

                }
            ).length;


        const notPlacedCount =
            history.filter(
                function (item) {

                    return item.status === "Not Placed";

                }
            ).length;


        if (placed) {

            placed.textContent =
                placedCount;

        }


        if (notPlaced) {

            notPlaced.textContent =
                notPlacedCount;

        }


        if (average) {

            if (history.length === 0) {

                average.textContent =
                    "0%";

            } else {

                const totalProbability =
                    history.reduce(
                        function (sum, item) {

                            return sum +
                                Number(
                                    item.placed_probability ||
                                    0
                                );

                        },
                        0
                    );


                const avg =
                    totalProbability /
                    history.length;


                average.textContent =
                    avg.toFixed(1) + "%";

            }

        }


        updateRecentAssessments();

    }


    // ============================================================
    // RECENT ASSESSMENTS
    // ============================================================

    function updateRecentAssessments() {

        const container =
            document.getElementById(
                "recentAssessments"
            );


        if (!container) {
            return;
        }


        const history =
            JSON.parse(
                localStorage.getItem(
                    "assessmentHistory"
                ) || "[]"
            );


        if (history.length === 0) {

            container.innerHTML =
                "<p>No assessments yet.</p>";

            return;

        }


        container.innerHTML = "";


        history.slice(0, 5).forEach(
            function (item) {

                const div =
                    document.createElement("div");


                div.className =
                    "recent-assessment";


                div.innerHTML = `
                    <strong>${escapeHTML(item.status)}</strong>
                    <span>
                        ${Number(
                            item.placed_probability || 0
                        ).toFixed(1)}%
                        placement probability
                    </span>
                    <small>
                        ${escapeHTML(item.date)}
                    </small>
                `;


                container.appendChild(div);

            }
        );

    }


    // ============================================================
// HISTORY
// ============================================================

function updateHistory() {

    const tableBody =
        document.getElementById("historyTableBody");

    if (!tableBody) {
        return;
    }

    const history =
        JSON.parse(
            localStorage.getItem("assessmentHistory") || "[]"
        );

    tableBody.innerHTML = "";

    if (history.length === 0) {

        tableBody.innerHTML = `
            <tr>
                <td colspan="5" class="empty-table">
                    No assessment history available.
                </td>
            </tr>
        `;

        return;
    }

    history.forEach(function (item, index) {

        const row =
            document.createElement("tr");

        row.innerHTML = `
            <td>
                ${index + 1}
            </td>

            <td>
                ${escapeHTML(item.date)}
            </td>

            <td>
                ${escapeHTML(item.status)}
            </td>

            <td>
                ${Number(
                    item.placed_probability || 0
                ).toFixed(2)}%
            </td>

            <td>
                <button
                    type="button"
                    class="secondary-button"
                    onclick="deleteAssessment(${item.id})">
                    Delete
                </button>
            </td>
        `;

        tableBody.appendChild(row);

    });

}


    // ============================================================
    // DELETE ASSESSMENT
    // ============================================================

    window.deleteAssessment =
        function (id) {

            let history =
                JSON.parse(
                    localStorage.getItem(
                        "assessmentHistory"
                    ) || "[]"
                );


            history =
                history.filter(
                    function (item) {

                        return item.id !== id;

                    }
                );


            localStorage.setItem(
                "assessmentHistory",
                JSON.stringify(history)
            );


            updateDashboard();

            updateHistory();

        };


    // ============================================================
    // CLEAR HISTORY
    // ============================================================

    function clearHistory() {

        const history =
            JSON.parse(
                localStorage.getItem(
                    "assessmentHistory"
                ) || "[]"
            );


        if (history.length === 0) {

            alert(
                "There is no assessment history to delete."
            );

            return;

        }


        const confirmed =
            confirm(
                "Are you sure you want to delete all assessment history?"
            );


        if (!confirmed) {
            return;
        }


        localStorage.removeItem(
            "assessmentHistory"
        );


        updateDashboard();

        updateHistory();


        alert(
            "Assessment history deleted successfully."
        );

    }


    if (clearHistoryButton) {

        clearHistoryButton.addEventListener(
            "click",
            clearHistory
        );

    }


    if (clearHistoryButtonMain) {

        clearHistoryButtonMain.addEventListener(
            "click",
            clearHistory
        );

    }


    // ============================================================
    // HELPER FUNCTIONS
    // ============================================================

    function formatFileSize(bytes) {

        if (bytes < 1024) {

            return bytes + " B";

        }

        if (bytes < 1024 * 1024) {

            return (
                bytes / 1024
            ).toFixed(1) + " KB";

        }

        return (
            bytes /
            (1024 * 1024)
        ).toFixed(1) + " MB";

    }


    function displayValue(value) {

        if (
            value === null ||
            value === undefined ||
            value === ""
        ) {

            return "Not found";

        }

        return String(value);

    }


    function escapeHTML(value) {

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

    }


    // ============================================================
    // INITIALIZE
    // ============================================================

    updateDashboard();

    updateHistory();

    showPage("dashboard");


    console.log(
        "Placement Prediction System frontend loaded successfully."
    );

});

// ============================================================
// DISPLAY EXTRACTED RESUME DATA
// ============================================================

function displayResumeAnalysis() {

    const savedData =
        sessionStorage.getItem("extractedStudentData");

    if (!savedData) {
        console.log("No extracted resume data found.");
        return;
    }

    let data;

    try {

        data = JSON.parse(savedData);

    } catch (error) {

        console.error(
            "Could not read extracted resume data:",
            error
        );

        return;
    }

    console.log(
        "Displaying resume analysis:",
        data
    );


    // ------------------------------------------------------------
    // HELPER
    // ------------------------------------------------------------

    function setValue(id, value) {

        const element =
            document.getElementById(id);

        if (!element) {
            return;
        }

        if (
            value === null ||
            value === undefined ||
            value === ""
        ) {

            element.textContent = "Not available";

        } else {

            element.textContent = value;

        }

    }


// ------------------------------------------------------------
// RESUME EXTRACTED VALUES
// ------------------------------------------------------------

setValue(
    "analysisName",
    data.name
);

setValue(
    "analysisCgpa",
    data.cgpa
);

setValue(
    "analysisInternships",
    data.internships_count
);

setValue(
    "analysisProjects",
    data.projects_count
);

setValue(
    "analysisCertifications",
    data.certifications_count
);

// Digital Profile
setValue(
    "analysisGithub",
    data.github_url || "Not detected"
);

setValue(
    "analysisLinkedin",
    data.linkedin || "Not detected"
);

setValue(
    "analysisPortfolio",
    data.portfolio_url || "Not detected"
);

setValue(
    "analysisHackathons",
    data.hackathons_participated ?? "Not available"
);

    // ------------------------------------------------------------
    // VALUES NOT AVAILABLE FROM RESUME
    // ------------------------------------------------------------

    setValue(
        "analysisAttendance",
        "Not available"
    );

    setValue(
        "analysisBacklogs",
        "Not available"
    );

    setValue(
        "analysisCoding",
        "Not available"
    );

    setValue(
        "analysisAptitude",
        "Not available"
    );

    setValue(
        "analysisLogical",
        "Not available"
    );

    setValue(
        "analysisHackathons",
        "Not available"
    );


    // ------------------------------------------------------------
    // STRENGTHS
    // ------------------------------------------------------------

    const strengthsList =
        document.getElementById("strengthsList");

    if (strengthsList) {

        strengthsList.innerHTML = "";

        const strengths = [];


        if (
            data.internships_count !== null &&
            data.internships_count !== undefined &&
            Number(data.internships_count) > 0
        ) {

            strengths.push(
                "Internship experience found in resume."
            );

        }


        if (
            data.projects_count !== null &&
            data.projects_count !== undefined &&
            Number(data.projects_count) > 0
        ) {

            strengths.push(
                "Project experience found in resume."
            );

        }


        if (
            data.certifications_count !== null &&
            data.certifications_count !== undefined &&
            Number(data.certifications_count) > 0
        ) {

            strengths.push(
                "Certifications found in resume."
            );

        }


        if (
            data.technical_skills &&
            data.technical_skills.length > 0
        ) {

            strengths.push(
                "Technical skills identified."
            );

        }


        if (strengths.length === 0) {

            strengths.push(
                "No major strengths could be extracted automatically."
            );

        }


        strengths.forEach(
            function (strength) {

                const li =
                    document.createElement("li");

                li.textContent = strength;

                strengthsList.appendChild(li);

            }
        );

    }


    // ------------------------------------------------------------
    // IMPROVEMENTS
    // ------------------------------------------------------------

    const improvementsList =
        document.getElementById("improvementsList");

    if (improvementsList) {

        improvementsList.innerHTML = "";

        const improvements = [];


        if (
            data.cgpa === null ||
            data.cgpa === undefined
        ) {

            improvements.push(
                "CGPA was not detected in the resume."
            );

        }


        if (
            data.linkedin === null ||
            data.linkedin === undefined ||
            data.linkedin === ""
        ) {

            improvements.push(
                "LinkedIn profile was not detected."
            );

        }


        if (
            data.github_repos === null ||
            data.github_repos === undefined ||
            Number(data.github_repos) === 0
        ) {

            improvements.push(
                "GitHub information was not detected."
            );

        }


        improvements.push(
            "Attendance, aptitude, coding and interview scores require assessment data."
        );


        improvements.forEach(
            function (improvement) {

                const li =
                    document.createElement("li");

                li.textContent = improvement;

                improvementsList.appendChild(li);

            }
        );

    }

}

// ============================================================
// RESUME PREDICTION BUTTON
// ============================================================

const resumePredictButton = document.getElementById("resumePredictButton");

if (resumePredictButton) {

    resumePredictButton.addEventListener("click", async function () {

        try {

            // ------------------------------------------------
            // Get extracted resume data
            // ------------------------------------------------

            const savedData = sessionStorage.getItem("extractedStudentData");

            if (!savedData) {

                alert(
                    "Resume information was not found. Please upload and analyze your resume first."
                );

                return;
            }


            const resumeData = JSON.parse(savedData);


            // ------------------------------------------------
            // Helper function
            // ------------------------------------------------

            function getNumber(value, defaultValue = 0) {

                const number = Number(value);

                return Number.isFinite(number) ? number : defaultValue;

            }


            // ------------------------------------------------
            // Get values from the assessment form
            // ------------------------------------------------

            const attendance = getNumber(
                document.getElementById("resumeAttendance")?.value
            );

            const backlogs = getNumber(
                document.getElementById("resumeBacklogs")?.value
            );

            const coding = getNumber(
                document.getElementById("resumeCoding")?.value
            );

            const aptitude = getNumber(
                document.getElementById("resumeAptitude")?.value
            );

            const communication = getNumber(
                document.getElementById("resumeCommunication")?.value
            );

            const logical = getNumber(
                document.getElementById("resumeLogical")?.value
            );

            const mockInterview = getNumber(
                document.getElementById("resumeMockInterview")?.value
            );

            const hackathons = getNumber(
                document.getElementById("resumeHackathons")?.value
            );


            // ------------------------------------------------
            // Validate required assessment fields
            // ------------------------------------------------

            if (
                document.getElementById("resumeAttendance")?.value === "" ||
                document.getElementById("resumeBacklogs")?.value === "" ||
                document.getElementById("resumeCoding")?.value === "" ||
                document.getElementById("resumeAptitude")?.value === "" ||
                document.getElementById("resumeCommunication")?.value === "" ||
                document.getElementById("resumeLogical")?.value === "" ||
                document.getElementById("resumeMockInterview")?.value === "" ||
                document.getElementById("resumeHackathons")?.value === ""
            ) {

                alert(
                    "Please complete all missing assessment fields before predicting."
                );

                return;
            }


            // ------------------------------------------------
            // Get resume-extracted values
            // ------------------------------------------------

            const cgpa = getNumber(resumeData.cgpa);

            const internships = getNumber(
                resumeData.internships_count
            );

            const projects = getNumber(
                resumeData.projects_count
            );

            const certifications = getNumber(
                resumeData.certifications_count
            );

            const githubRepos = getNumber(
                resumeData.github_repos
            );


            // ------------------------------------------------
            // Validate CGPA
            // ------------------------------------------------

            if (cgpa <= 0) {

                alert(
                    "CGPA could not be extracted from your resume. Please make sure your resume contains your CGPA and analyze the resume again."
                );

                return;
            }


            // ------------------------------------------------
            // Create API request
            // ------------------------------------------------

            const requestData = {

                cgpa: cgpa,

                internships_count: internships,

                projects_count: projects,

                certifications_count: certifications,

                github_repos: githubRepos,

                attendance_percentage: attendance,

                backlogs: backlogs,

                coding_skill_score: coding,

                aptitude_score: aptitude,

                communication_skill_score: communication,

                logical_reasoning_score: logical,

                mock_interview_score: mockInterview,

                hackathons_participated: hackathons
            };


            // ------------------------------------------------
            // Show loading state
            // ------------------------------------------------

            resumePredictButton.disabled = true;

            resumePredictButton.textContent =
                "Predicting Placement...";


            // ------------------------------------------------
            // Send request to FastAPI
            // ------------------------------------------------

            const response = await fetch(
                "http://127.0.0.1:8000/predict-resume-placement",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(requestData)
                }
            );


            // ------------------------------------------------
            // Read API response
            // ------------------------------------------------

            const result = await response.json();


            // ------------------------------------------------
            // Handle API error
            // ------------------------------------------------

            if (!response.ok || !result.success) {

                throw new Error(
                    result.error ||
                    result.message ||
                    "Prediction failed."
                );
            }


            // ------------------------------------------------
            // Display prediction
            // ------------------------------------------------

            let resultBox =
                document.getElementById("resumePredictionResult");


            if (!resultBox) {

                resultBox = document.createElement("div");

                resultBox.id =
                    "resumePredictionResult";

                resultBox.style.marginTop =
                    "25px";

                resultBox.style.padding =
                    "25px";

                resultBox.style.borderRadius =
                    "15px";

                resultBox.style.background =
                    "#f5f7ff";

                resultBox.style.border =
                    "1px solid #dfe3ff";

                resumePredictButton
                    .parentElement
                    .parentElement
                    .appendChild(resultBox);
            }


            const status =
                result.placement_status;

            const placedProbability =
                Number(result.placed_probability).toFixed(2);

            const notPlacedProbability =
                Number(result.not_placed_probability).toFixed(2);


            // ------------------------------------------------
            // Recommendations
            // ------------------------------------------------

            let recommendationsHTML = "";


            if (
                Array.isArray(result.recommendations) &&
                result.recommendations.length > 0
            ) {

                recommendationsHTML =
                    result.recommendations
                        .map(function (recommendation) {

                            return `
                                <li style="margin-bottom:8px;">
                                    ${recommendation}
                                </li>
                            `;

                        })
                        .join("");
            }


            // ------------------------------------------------
            // Result HTML
            // ------------------------------------------------

            resultBox.innerHTML = `

                <h3 style="margin-bottom:15px;">
                    Placement Prediction Result
                </h3>

                <div style="
                    font-size:22px;
                    font-weight:700;
                    margin-bottom:15px;
                ">
                    ${status}
                </div>

                <div style="
                    display:grid;
                    grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
                    gap:15px;
                    margin-bottom:20px;
                ">

                    <div style="
                        padding:15px;
                        background:white;
                        border-radius:10px;
                    ">

                        <strong>
                            Placement Probability
                        </strong>

                        <div style="
                            font-size:24px;
                            font-weight:700;
                            margin-top:8px;
                        ">
                            ${placedProbability}%
                        </div>

                    </div>


                    <div style="
                        padding:15px;
                        background:white;
                        border-radius:10px;
                    ">

                        <strong>
                            Not Placed Probability
                        </strong>

                        <div style="
                            font-size:24px;
                            font-weight:700;
                            margin-top:8px;
                        ">
                            ${notPlacedProbability}%
                        </div>

                    </div>

                </div>


                <h4 style="margin-bottom:10px;">
                    Recommendations
                </h4>

                <ul style="
                    padding-left:20px;
                    margin:0;
                ">
                    ${recommendationsHTML}
                </ul>

            `;


            // ------------------------------------------------
            // Save prediction
            // ------------------------------------------------

            const history =
                JSON.parse(
                    localStorage.getItem("assessmentHistory") || "[]"
                );


            history.push({

                date: new Date().toLocaleString(),

                status: status,

                placed_probability:
                    Number(result.placed_probability),

                not_placed_probability:
                    Number(result.not_placed_probability),

                source: "Resume Assessment"

            });


            localStorage.setItem(
                "assessmentHistory",
                JSON.stringify(history)
            );


            // ------------------------------------------------
            // Scroll to result
            // ------------------------------------------------

            resultBox.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });


        } catch (error) {

            console.error(
                "Resume prediction error:",
                error
            );

            alert(
                "Prediction failed: " +
                error.message
            );


        } finally {

            // ------------------------------------------------
            // Restore button
            // ------------------------------------------------

            resumePredictButton.disabled = false;

            resumePredictButton.textContent =
                "Predict Placement";

        }

    });

}

