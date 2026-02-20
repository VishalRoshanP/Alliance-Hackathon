document.addEventListener('DOMContentLoaded', async () => {
    const uploadButton = document.getElementById('upload-button');
    const dataFile = document.getElementById('data-file');
    const filterButton = document.getElementById('filter-button');
    const riskTableBody = document.getElementById('risk-table-body');
    
    // Upload file
    uploadButton.addEventListener('click', async () => {
        const file = dataFile.files[0];
        if (!file) {
            alert('Please select a file');
            return;
        }
        
        try {
            const statusDiv = document.getElementById('upload-status');
            statusDiv.textContent = 'Uploading...';
            
            const response = await analyticsAPI.uploadData(file);
            
            statusDiv.textContent = `Uploaded successfully! Processed ${response.processed} records.`;
            if (response.errors && response.errors.length > 0) {
                console.warn('Upload errors:', response.errors);
            }
            
            // Refresh risk scores
            loadRiskScores();
        } catch (error) {
            console.error('Upload failed:', error);
            document.getElementById('upload-status').textContent = 'Upload failed. Please try again.';
        }
    });
    
    // Apply filters
    filterButton.addEventListener('click', () => {
        loadRiskScores();
    });
    
    // Load risk scores
    const loadRiskScores = async () => {
        try {
            const schoolFilter = document.getElementById('school-filter').value;
            const riskLevelFilter = document.getElementById('risk-level-filter').value;
            
            const response = await analyticsAPI.getRiskScores(
                schoolFilter || null,
                riskLevelFilter || null
            );
            
            displayRiskScores(response.assessments || []);
        } catch (error) {
            console.error('Failed to load risk scores:', error);
        }
    };
    
    // Display risk scores in table
    const displayRiskScores = (assessments) => {
        riskTableBody.innerHTML = '';
        
        if (assessments.length === 0) {
            riskTableBody.innerHTML = '<tr><td colspan="5">No data available</td></tr>';
            return;
        }
        
        assessments.forEach(assessment => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${assessment.student_id}</td>
                <td>-</td>
                <td>${assessment.risk_score}</td>
                <td><span class="risk-level ${assessment.risk_level}">${assessment.risk_level}</span></td>
                <td><button onclick="viewDetails(${assessment.student_id})">View Details</button></td>
            `;
            riskTableBody.appendChild(row);
        });
    };
    
    // Initial load
    loadRiskScores();
});

function viewDetails(studentId) {
    window.location.href = `/static/student.html?id=${studentId}`;
}
