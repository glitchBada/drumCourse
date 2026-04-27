import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../api/axios';
import './Cabinet.scss';

function CabinetSidebar({ user }) {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const initials = `${user.first_name?.[0] || ''}${user.last_name?.[0] || ''}`.toUpperCase() || '?';

  return (
    <aside className="cabinet-sidebar">
      <div className="user-avatar">{initials}</div>
      <div className="user-name">{user.first_name} {user.last_name}</div>
      <div className="user-email">{user.email}</div>
      <nav>
        <Link to="/cabinet" className={location.pathname === '/cabinet' ? 'active' : ''}>
          Профиль
        </Link>
        <Link to="/cabinet/orders" className={location.pathname.startsWith('/cabinet/orders') ? 'active' : ''}>
          Мои заявки
        </Link>
      </nav>
      <button className="logout-btn" onClick={handleLogout} style={{ marginTop: '1.5rem', width: '100%' }}>
        Выйти
      </button>
    </aside>
  );
}

function CabinetPage() {
  const { user, updateUser } = useAuth();
  const [formData, setFormData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);
    try {
      const res = await api.patch('/api/auth/me/', formData);
      updateUser(res.data);
      setSuccess('Данные сохранены.');
    } catch (err) {
      const data = err.response?.data;
      setError(Object.values(data || {}).flat().join(' ') || 'Ошибка сохранения.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="cabinet-page">
      <div className="cabinet-container">
        <div className="cabinet-header">
          <h1>Личный <span>кабинет</span></h1>
        </div>
        <div className="cabinet-grid">
          <CabinetSidebar user={user} />
          <main className="cabinet-content">
            <h2>Мой <span>профиль</span></h2>
            {error && <div className="cabinet-alert error">{error}</div>}
            {success && <div className="cabinet-alert success">{success}</div>}
            <form className="profile-form" onSubmit={handleSubmit}>
              <input
                type="text"
                name="first_name"
                placeholder="Имя"
                value={formData.first_name}
                onChange={handleChange}
              />
              <input
                type="text"
                name="last_name"
                placeholder="Фамилия"
                value={formData.last_name}
                onChange={handleChange}
              />
              <input type="email" value={user?.email || ''} disabled />
              <p className="field-hint">Email нельзя изменить</p>
              <input type="text" value={user?.phone_number || ''} disabled />
              <p className="field-hint">Телефон нельзя изменить</p>
              <button type="submit" className="save-btn" disabled={loading}>
                {loading ? 'Сохранение...' : 'Сохранить'}
              </button>
            </form>
          </main>
        </div>
      </div>
    </div>
  );
}

export { CabinetSidebar };
export default CabinetPage;
