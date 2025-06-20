import apiService from '../services/api';

function Dashboard({ user, onLogout }) {
  const handleLogout = () => {
    apiService.clearToken();
    onLogout();
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Pi Server Project</h1>
        <div className="user-info">
          <span>Welcome, {user.username}!</span>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </header>

      <main className="dashboard-content">
        <div className="user-card">
          <h2>User Profile</h2>
          <p><strong>Username:</strong> {user.username}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Member since:</strong> {new Date(user.created_at).toLocaleDateString()}</p>
          <p><strong>Status:</strong> {user.is_active ? 'Active' : 'Inactive'}</p>
        </div>

        <div className="features-card">
          <h2>Application Features</h2>
          <p>🎉 Authentication system is working!</p>
          <p>🔐 You are successfully logged in</p>
          <p>🚀 Ready to build more features</p>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;