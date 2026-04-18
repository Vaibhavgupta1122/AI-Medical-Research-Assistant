// Debug script to check API connectivity
const testAPI = async () => {
    console.log('Testing API connectivity...');

    try {
        // Test backend health
        const response = await fetch('http://localhost:5000/api/health');
        const data = await response.json();
        console.log('Backend Health:', data);

        // Test AI service health
        const aiResponse = await fetch('http://localhost:8000/health');
        const aiData = await aiResponse.json();
        console.log('AI Service Health:', aiData);

        console.log('All services are working!');
    } catch (error) {
        console.error('API Test Failed:', error);
    }
};

// Auto-run on page load
if (typeof window !== 'undefined') {
    window.addEventListener('load', () => {
        setTimeout(testAPI, 1000);
    });
}
