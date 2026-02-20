// API utility functions
const API_BASE_URL = '/api';

async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Chat API
const chatAPI = {
    startConversation: async (studentId = null) => {
        return apiRequest('/chat/start', {
            method: 'POST',
            body: JSON.stringify({ student_id: studentId })
        });
    },
    
    sendMessage: async (sessionId, message, studentId = null) => {
        return apiRequest('/chat/message', {
            method: 'POST',
            body: JSON.stringify({
                session_id: sessionId,
                message: message,
                student_id: studentId
            })
        });
    },
    
    getConversations: async (studentId = null) => {
        const params = studentId ? `?student_id=${studentId}` : '';
        return apiRequest(`/chat/conversations${params}`);
    }
};

// Analytics API
const analyticsAPI = {
    uploadData: async (file, schoolId = null) => {
        const formData = new FormData();
        formData.append('file', file);
        if (schoolId) {
            formData.append('school_id', schoolId);
        }
        
        const response = await fetch(`${API_BASE_URL}/analytics/upload-data`, {
            method: 'POST',
            body: formData
        });
        
        return await response.json();
    },
    
    getDashboard: async (schoolId = null) => {
        const params = schoolId ? `?school_id=${schoolId}` : '';
        return apiRequest(`/analytics/dashboard${params}`);
    },
    
    getRiskScores: async (schoolId = null, riskLevel = null) => {
        const params = new URLSearchParams();
        if (schoolId) params.append('school_id', schoolId);
        if (riskLevel) params.append('risk_level', riskLevel);
        return apiRequest(`/analytics/risk-scores?${params.toString()}`);
    },
    
    calculateRisk: async (studentId) => {
        return apiRequest('/analytics/calculate-risk', {
            method: 'POST',
            body: JSON.stringify({ student_id: studentId })
        });
    }
};

// Students API
const studentsAPI = {
    list: async (schoolId = null, status = null) => {
        const params = new URLSearchParams();
        if (schoolId) params.append('school_id', schoolId);
        if (status) params.append('status', status);
        return apiRequest(`/students?${params.toString()}`);
    },
    
    get: async (studentId) => {
        return apiRequest(`/students/${studentId}`);
    }
};

// Resources API
const resourcesAPI = {
    list: async (category = null, location = null) => {
        const params = new URLSearchParams();
        if (category) params.append('category', category);
        if (location) params.append('location', location);
        return apiRequest(`/resources?${params.toString()}`);
    },
    
    get: async (resourceId) => {
        return apiRequest(`/resources/${resourceId}`);
    }
};
