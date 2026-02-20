document.addEventListener('DOMContentLoaded', async () => {
    try {
        const dashboard = await analyticsAPI.getDashboard();
        
        // Update stats
        document.getElementById('total-students').textContent = dashboard.total_students || 0;
        document.getElementById('at-risk-students').textContent = dashboard.at_risk_students || 0;
        
        // Update risk distribution
        const riskDist = dashboard.risk_distribution || {};
        const riskChart = document.getElementById('risk-chart');
        riskChart.innerHTML = `
            <p>Low: ${riskDist.low || 0}</p>
            <p>Medium: ${riskDist.medium || 0}</p>
            <p>High: ${riskDist.high || 0}</p>
            <p>Critical: ${riskDist.critical || 0}</p>
        `;
    } catch (error) {
        console.error('Failed to load dashboard:', error);
    }
});
