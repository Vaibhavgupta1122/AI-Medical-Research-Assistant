import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { userAPI } from '../services/api';
import './ProfilePage.css';

function ProfilePage() {
  const { user, updateUser } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [formData, setFormData] = useState({
    profile: {
      age: '',
      gender: '',
      location: {
        country: '',
        state: '',
        city: ''
      },
      medicalBackground: {
        conditions: '',
        medications: '',
        allergies: ''
      }
    },
    preferences: {
      language: 'english',
      complexity: 'intermediate',
      notificationSettings: {
        email: true,
        researchUpdates: true
      }
    }
  });

  useEffect(() => {
    if (user) {
      // Initialize form data with user data
      setFormData({
        profile: {
          age: user.profile?.age || '',
          gender: user.profile?.gender || '',
          location: {
            country: user.profile?.location?.country || '',
            state: user.profile?.location?.state || '',
            city: user.profile?.location?.city || ''
          },
          medicalBackground: {
            conditions: user.profile?.medicalBackground?.conditions?.join(', ') || '',
            medications: user.profile?.medicalBackground?.medications?.join(', ') || '',
            allergies: user.profile?.medicalBackground?.allergies?.join(', ') || ''
          }
        },
        preferences: {
          language: user.preferences?.language || 'english',
          complexity: user.preferences?.complexity || 'intermediate',
          notificationSettings: {
            email: user.preferences?.notificationSettings?.email ?? true,
            researchUpdates: user.preferences?.notificationSettings?.researchUpdates ?? true
          }
        }
      });
      
      fetchStats();
    }
  }, [user]);

  const fetchStats = async () => {
    try {
      const response = await userAPI.getStats(user.id);
      if (response.data.success) {
        setStats(response.data.stats);
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleInputChange = (section, field, value) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }));
  };

  const handleLocationChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      profile: {
        ...prev.profile,
        location: {
          ...prev.profile.location,
          [field]: value
        }
      }
    }));
  };

  const handleNotificationChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      preferences: {
        ...prev.preferences,
        notificationSettings: {
          ...prev.preferences.notificationSettings,
          [field]: value
        }
      }
    }));
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      // Prepare data for API
      const profileData = {
        ...formData.profile,
        age: formData.profile.age ? parseInt(formData.profile.age) : undefined,
        medicalBackground: {
          conditions: formData.profile.medicalBackground.conditions
            .split(',')
            .map(s => s.trim())
            .filter(s => s),
          medications: formData.profile.medicalBackground.medications
            .split(',')
            .map(s => s.trim())
            .filter(s => s),
          allergies: formData.profile.medicalBackground.allergies
            .split(',')
            .map(s => s.trim())
            .filter(s => s)
        }
      };

      const response = await userAPI.updateProfile(user.id, profileData, formData.preferences);
      
      if (response.data.success) {
        updateUser(response.data.user);
        setIsEditing(false);
      }
    } catch (error) {
      console.error('Error updating profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    // Reset form data
    if (user) {
      setFormData({
        profile: {
          age: user.profile?.age || '',
          gender: user.profile?.gender || '',
          location: {
            country: user.profile?.location?.country || '',
            state: user.profile?.location?.state || '',
            city: user.profile?.location?.city || ''
          },
          medicalBackground: {
            conditions: user.profile?.medicalBackground?.conditions?.join(', ') || '',
            medications: user.profile?.medicalBackground?.medications?.join(', ') || '',
            allergies: user.profile?.medicalBackground?.allergies?.join(', ') || ''
          }
        },
        preferences: {
          language: user.preferences?.language || 'english',
          complexity: user.preferences?.complexity || 'intermediate',
          notificationSettings: {
            email: user.preferences?.notificationSettings?.email ?? true,
            researchUpdates: user.preferences?.notificationSettings?.researchUpdates ?? true
          }
        }
      });
    }
    setIsEditing(false);
  };

  if (!user) {
    return <div className="profile-page">Loading...</div>;
  }

  return (
    <div className="profile-page">
      <div className="profile-container">
        <div className="profile-header">
          <h1>Profile Settings</h1>
          <div className="header-actions">
            {!isEditing ? (
              <button className="btn btn-primary" onClick={() => setIsEditing(true)}>
                Edit Profile
              </button>
            ) : (
              <div className="edit-actions">
                <button className="btn btn-secondary" onClick={handleCancel} disabled={loading}>
                  Cancel
                </button>
                <button className="btn btn-primary" onClick={handleSave} disabled={loading}>
                  {loading ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="profile-content">
          <div className="profile-sections">
            {/* Basic Information */}
            <div className="profile-section">
              <h2>Basic Information</h2>
              <div className="section-content">
                <div className="form-group">
                  <label>Name</label>
                  <input
                    type="text"
                    value={user.name}
                    disabled
                    className="form-input disabled"
                  />
                </div>
                <div className="form-group">
                  <label>Email</label>
                  <input
                    type="email"
                    value={user.email}
                    disabled
                    className="form-input disabled"
                  />
                </div>
              </div>
            </div>

            {/* Demographics */}
            <div className="profile-section">
              <h2>Demographics</h2>
              <div className="section-content">
                <div className="form-row">
                  <div className="form-group">
                    <label>Age</label>
                    <input
                      type="number"
                      value={formData.profile.age}
                      onChange={(e) => handleInputChange('profile', 'age', e.target.value)}
                      disabled={!isEditing}
                      className="form-input"
                      min="1"
                      max="120"
                    />
                  </div>
                  <div className="form-group">
                    <label>Gender</label>
                    <select
                      value={formData.profile.gender}
                      onChange={(e) => handleInputChange('profile', 'gender', e.target.value)}
                      disabled={!isEditing}
                      className="form-select"
                    >
                      <option value="">Select</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                      <option value="prefer_not_to_say">Prefer not to say</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            {/* Location */}
            <div className="profile-section">
              <h2>Location</h2>
              <div className="section-content">
                <div className="form-row">
                  <div className="form-group">
                    <label>Country</label>
                    <input
                      type="text"
                      value={formData.profile.location.country}
                      onChange={(e) => handleLocationChange('country', e.target.value)}
                      disabled={!isEditing}
                      className="form-input"
                      placeholder="United States"
                    />
                  </div>
                  <div className="form-group">
                    <label>State/Province</label>
                    <input
                      type="text"
                      value={formData.profile.location.state}
                      onChange={(e) => handleLocationChange('state', e.target.value)}
                      disabled={!isEditing}
                      className="form-input"
                      placeholder="California"
                    />
                  </div>
                  <div className="form-group">
                    <label>City</label>
                    <input
                      type="text"
                      value={formData.profile.location.city}
                      onChange={(e) => handleLocationChange('city', e.target.value)}
                      disabled={!isEditing}
                      className="form-input"
                      placeholder="San Francisco"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Medical Background */}
            <div className="profile-section">
              <h2>Medical Background</h2>
              <div className="section-content">
                <div className="form-group">
                  <label>Medical Conditions</label>
                  <textarea
                    value={formData.profile.medicalBackground.conditions}
                    onChange={(e) => handleInputChange('profile', 'medicalBackground', {
                      ...formData.profile.medicalBackground,
                      conditions: e.target.value
                    })}
                    disabled={!isEditing}
                    className="form-textarea"
                    placeholder="Enter conditions separated by commas (e.g., Diabetes, Hypertension)"
                    rows={3}
                  />
                </div>
                <div className="form-group">
                  <label>Current Medications</label>
                  <textarea
                    value={formData.profile.medicalBackground.medications}
                    onChange={(e) => handleInputChange('profile', 'medicalBackground', {
                      ...formData.profile.medicalBackground,
                      medications: e.target.value
                    })}
                    disabled={!isEditing}
                    className="form-textarea"
                    placeholder="Enter medications separated by commas (e.g., Metformin, Lisinopril)"
                    rows={3}
                  />
                </div>
                <div className="form-group">
                  <label>Allergies</label>
                  <textarea
                    value={formData.profile.medicalBackground.allergies}
                    onChange={(e) => handleInputChange('profile', 'medicalBackground', {
                      ...formData.profile.medicalBackground,
                      allergies: e.target.value
                    })}
                    disabled={!isEditing}
                    className="form-textarea"
                    placeholder="Enter allergies separated by commas (e.g., Penicillin, Peanuts)"
                    rows={3}
                  />
                </div>
              </div>
            </div>

            {/* Preferences */}
            <div className="profile-section">
              <h2>Preferences</h2>
              <div className="section-content">
                <div className="form-row">
                  <div className="form-group">
                    <label>Language</label>
                    <select
                      value={formData.preferences.language}
                      onChange={(e) => handleInputChange('preferences', 'language', e.target.value)}
                      disabled={!isEditing}
                      className="form-select"
                    >
                      <option value="english">English</option>
                      <option value="spanish">Spanish</option>
                      <option value="french">French</option>
                      <option value="german">German</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Response Complexity</label>
                    <select
                      value={formData.preferences.complexity}
                      onChange={(e) => handleInputChange('preferences', 'complexity', e.target.value)}
                      disabled={!isEditing}
                      className="form-select"
                    >
                      <option value="basic">Basic</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                    </select>
                  </div>
                </div>
                <div className="form-group">
                  <label>Notification Settings</label>
                  <div className="checkbox-group">
                    <label className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={formData.preferences.notificationSettings.email}
                        onChange={(e) => handleNotificationChange('email', e.target.checked)}
                        disabled={!isEditing}
                      />
                      <span>Email notifications</span>
                    </label>
                    <label className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={formData.preferences.notificationSettings.researchUpdates}
                        onChange={(e) => handleNotificationChange('researchUpdates', e.target.checked)}
                        disabled={!isEditing}
                      />
                      <span>Research updates</span>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Statistics */}
          {stats && (
            <div className="stats-section">
              <h2>Your Activity</h2>
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-value">{stats.totalConversations || 0}</div>
                  <div className="stat-label">Total Conversations</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.usage?.totalQueries || 0}</div>
                  <div className="stat-label">Total Queries</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.bookmarkedConversations || 0}</div>
                  <div className="stat-label">Bookmarked</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{Math.round(stats.avgMessagesPerConversation || 0)}</div>
                  <div className="stat-label">Avg Messages/Conversation</div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;
