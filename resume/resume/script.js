document.addEventListener("DOMContentLoaded", () => {
  // --- Handle Resume Upload on upload.html ---
  const uploadForm = document.getElementById("upload-form");
  if (uploadForm) {
    uploadForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      const fileInput = document.getElementById("resume-file");
      const loader = document.getElementById("loader");

      // Show loader
      loader.style.display = "block";

      const formData = new FormData();
      formData.append("resume", fileInput.files[0]);

      try {
        const response = await fetch("/api/upload_resume/", {
          method: "POST",
          body: formData,
        });

        const result = await response.json();

        // Hide loader
        loader.style.display = "none";

        if (result.success && result.data) {
          sessionStorage.setItem("parsed_resume", JSON.stringify(result.data));
          window.location.href = "index.html";
        } else {
          alert("Parsing failed. Try again.");
        }
      } catch (err) {
        loader.style.display = "none";
        alert("Error during parsing. Please try again.");
      }
    });
  }

  // --- Handle Data Rendering on index.html ---
  const parsed = sessionStorage.getItem("parsed_resume");
  if (parsed) {
    const data = JSON.parse(parsed);
    renderResumeDetails(data);

    const saveBtn = document.getElementById("save-btn");
    if (saveBtn) {
      saveBtn.addEventListener("click", async () => {
        const response = await fetch("/api/save_resume/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        const result = await response.json();
        if (result.success) {
          sessionStorage.removeItem("parsed_resume");
          Swal.fire({
            title: '🎉 Resume Saved!',
            text: 'Your resume has been successfully saved to the database.',
            icon: 'success',
            confirmButtonText: 'Close this window',
            confirmButtonColor: '#3085d6'
          }).then(() => {
            window.close();
          });
        } else {
          Swal.fire({
            title: 'Oops!',
            text: 'Something went wrong while saving.',
            icon: 'error',
            confirmButtonText: 'Try Again'
          });
        }
      });
    }
  }
});


// --- Render Resume Details to index.html ---
function renderResumeDetails(data) {
  // Basic example - update these IDs as needed
  document.getElementById("basic-name").textContent = data.name || "-";
  document.getElementById("basic-email").textContent = data.email || "-";
  document.getElementById("basic-phone").textContent = data.phone || "-";
  document.getElementById("basic-address").textContent = data.address || "-";
  document.getElementById("basic-nationality").textContent = data.nationality || "-";
  document.getElementById("basic-aadhar").textContent = data.aadhar_number || "-";
  document.getElementById("basic-pan").textContent = data.pan_number || "-";

  // Education section
  if (Array.isArray(data.education)) {
    const tbody = document.getElementById("education-body");
    tbody.innerHTML = "";
    data.education.forEach((edu) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${edu.qualification || ""}</td>
        <td>${edu.degree || ""}</td>
        <td>${edu.subject || ""}</td>
        <td>${edu.specialization || ""}</td>
        <td>${edu.passing_year || ""}</td>
        <td>${edu.mode || ""}</td>
        <td>${edu.institute || ""}</td>
        <td>${edu.university || ""}</td>
      `;
      tbody.appendChild(row);
    });
  }

  // Work Experience section
  if (Array.isArray(data.work_experience)) {
    const tbody = document.getElementById("experience-body");
    tbody.innerHTML = "";
    data.work_experience.forEach((exp) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${exp.company || ""}</td>
        <td>${exp.designation || ""}</td>
        <td>${exp.duration || ""}</td>
        <td>${exp.total_experience || ""}</td>
      `;
      tbody.appendChild(row);
    });
  }

  // Project section
  if (Array.isArray(data.projects)) {
    const tbody = document.getElementById("project-body");
    tbody.innerHTML = "";
    data.projects.forEach((proj, index) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${index + 1}</td>
        <td>${proj.duration || ""}</td>
        <td>${proj.company || ""}</td>
        <td>${proj.name || ""}</td>
        <td>${proj.designation || ""}</td>
        <td>${proj.client || ""}</td>
        <td>${proj.funding_agency || ""}</td>
        <td>${proj.sectors || ""}</td>
        <td>${proj.phases || ""}</td>
        <td>${proj.length || ""}</td>
        <td>${proj.project_experience || ""}</td>
      `;
      tbody.appendChild(row);
    });
  }

  // Final Topics (Comma-separated)
  document.getElementById("industry").textContent = (data.industry || []).join(", ");
  document.getElementById("sectors").textContent = (data.sectors || []).join(", ");
  document.getElementById("phases").textContent = (data.phases || []).join(", ");
  document.getElementById("keywords").textContent = (data.keywords || []).join(", ");
}
