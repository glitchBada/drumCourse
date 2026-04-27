import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';
import './Form.scss';

function FormforOrder() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isAuthenticated) {
      navigate('/login', { state: { from: { pathname: '/home' } } });
      return;
    }

    setError('');
    setLoading(true);
    try {
      await api.post('/api/applications/', { type: 'trial', message });
      setSubmitted(true);
      setMessage('');
    } catch (err) {
      const data = err.response?.data;
      setError(
        data?.detail ||
        Object.values(data || {}).flat().join(' ') ||
        'Ошибка отправки. Попробуйте позже.'
      );
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className='Form'>
        <h2>ЗАЯВКА <span>ОТПРАВЛЕНА</span></h2>
        <p style={{ color: '#aaa', textAlign: 'center', padding: '1rem 0' }}>
          Мы свяжемся с вами в ближайшее время.{' '}
          <a href="/cabinet/orders" style={{ color: '#e63946' }}>Посмотреть заявки</a>
        </p>
      </div>
    );
  }

  return (
    <div className='Form'>
      <h2>СВЯЖИТЕСЬ <span>С НАМИ</span></h2>
      {!isAuthenticated && (
        <p style={{ color: '#aaa', textAlign: 'center', fontSize: '0.9rem', marginBottom: '1rem' }}>
          Для записи необходима{' '}
          <a href="/login" style={{ color: '#e63946' }}>авторизация</a>.
        </p>
      )}
      {error && (
        <p style={{ color: '#ff6b6b', textAlign: 'center', fontSize: '0.875rem', marginBottom: '0.75rem' }}>
          {error}
        </p>
      )}
      <form onSubmit={handleSubmit}>
        <div className="textarea">
          <label>
            <input
              type="text"
              name="message"
              placeholder='Ваше сообщение (необязательно)'
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
          </label>
        </div>
        <button className='submitbutton' type="submit" disabled={loading}>
          {loading ? 'Отправка...' : 'Записаться на пробный урок'}
        </button>
      </form>
    </div>
  );
}

export default FormforOrder;
