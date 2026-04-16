import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './LoginPage.css';

function LoginPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      let result;
      if (isLogin) {
        result = await login(email);
      } else {
        result = await register(email, name);
      }

      if (result.success) {
        navigate('/chat');
      } else {
        setError(result.error);
      }
    } catch (error) {
      setError('An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <h1 className="login-title">
            <span className="medical-icon">+</span>
            AI Medical Research Assistant
          </h1>
          <p className="login-subtitle">
            Evidence-based medical research at your fingertips
          </p>
        </div>

        <div className="login-form-container">
          <div className="form-tabs">
            <button
              className={`tab-button ${isLogin ? 'active' : ''}`}
              onClick={() => setIsLogin(true)}
            >
              Sign In
            </button>
            <button
              className={`tab-button ${!isLogin ? 'active' : ''}`}
              onClick={() => setIsLogin(false)}
            >
              Sign Up
            </button>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            {!isLogin && (
              <div className="form-group">
                <label htmlFor="name" className="form-label">
                  Full Name
                </label>
                <input
                  type="text"
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="form-input"
                  placeholder="Enter your full name"
                  required={!isLogin}
                />
              </div>
            )}

            <div className="form-group">
              <label htmlFor="email" className="form-label">
                Email Address
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="form-input"
                placeholder="Enter your email"
                required
              />
            </div>

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            <button
              type="submit"
              className="submit-button"
              disabled={loading}
            >
              {loading ? (
                <div className="loading-spinner">
                  <div className="spinner"></div>
                  Processing...
                </div>
              ) : (
                isLogin ? 'Sign In' : 'Sign Up'
              )}
            </button>
          </form>

          <div className="login-footer">
            <p>
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button
                className="link-button"
                onClick={() => setIsLogin(!isLogin)}
              >
                {isLogin ? 'Sign Up' : 'Sign In'}
              </button>
            </p>
          </div>
        </div>

        <div className="features-section">
          <h3>Features</h3>
          <ul className="features-list">
            <li>Access to latest medical research</li>
            <li>Clinical trial information</li>
            <li>AI-powered insights</li>
            <li>Personalized recommendations</li>
            <li>Evidence-based information</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
