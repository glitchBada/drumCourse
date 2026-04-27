import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../../api/axios';
import './AuthPages.scss';

const RESEND_COOLDOWN = 60;

function VerifyOTPPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const email = location.state?.email || '';

  const [codes, setCodes] = useState({ email: '', phone: '' });
  const [verified, setVerified] = useState({ email: false, phone: false });
  const [cooldown, setCooldown] = useState({ email: 0, phone: 0 });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  // Таймеры обратного отсчёта кулдауна
  useEffect(() => {
    const interval = setInterval(() => {
      setCooldown((prev) => ({
        email: prev.email > 0 ? prev.email - 1 : 0,
        phone: prev.phone > 0 ? prev.phone - 1 : 0,
      }));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const verify = async (purpose) => {
    const code = codes[purpose === 'email' ? 'email' : 'phone'];
    if (!code || code.length !== 6) {
      setError('Введите 6-значный код.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const res = await api.post('/api/auth/verify-otp/', { email, code, purpose });
      setVerified((prev) => ({ ...prev, [purpose === 'email' ? 'email' : 'phone']: true }));
      setSuccess(res.data.message);

      if (res.data.message.includes('активирован')) {
        setTimeout(() => navigate('/login'), 2000);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка верификации.');
    } finally {
      setLoading(false);
    }
  };

  const resend = async (purpose) => {
    setError('');
    try {
      await api.post('/api/auth/resend-otp/', { email, purpose });
      setCooldown((prev) => ({ ...prev, [purpose === 'email' ? 'email' : 'phone']: RESEND_COOLDOWN }));
      setSuccess(`Код отправлен повторно (${purpose === 'email' ? 'Email' : 'WhatsApp'}).`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка повторной отправки.');
    }
  };

  if (!email) {
    return (
      <div className="auth-page">
        <div className="auth-card">
          <p className="auth-footer">
            Перейдите к <a href="/register">регистрации</a>.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Под<span>тверждение</span></h2>
        <p style={{ color: '#aaa', textAlign: 'center', marginBottom: '1rem', fontSize: '0.9rem' }}>
          Коды отправлены на <strong style={{ color: '#fff' }}>{email}</strong> и WhatsApp.
        </p>

        {error && <div className="auth-error">{error}</div>}
        {success && <div className="auth-success">{success}</div>}

        <div className="otp-grid">
          {/* Email OTP */}
          <div className="otp-block">
            <label>Email {verified.email && <span className="done">✓</span>}</label>
            <input
              type="text"
              inputMode="numeric"
              maxLength={6}
              placeholder="000000"
              value={codes.email}
              onChange={(e) => setCodes({ ...codes, email: e.target.value.replace(/\D/g, '') })}
              disabled={verified.email}
            />
            {!verified.email && (
              <>
                <button
                  type="button"
                  onClick={() => verify('email')}
                  disabled={loading}
                  style={{
                    marginTop: '0.5rem',
                    background: '#e63946',
                    border: 'none',
                    borderRadius: '4px',
                    color: '#fff',
                    cursor: 'pointer',
                    padding: '0.4rem 0',
                    width: '100%',
                    fontSize: '0.8rem',
                  }}
                >
                  Подтвердить
                </button>
                <button
                  type="button"
                  className="resend-btn"
                  onClick={() => resend('email')}
                  disabled={cooldown.email > 0}
                >
                  {cooldown.email > 0 ? `Повтор через ${cooldown.email}с` : 'Отправить снова'}
                </button>
              </>
            )}
          </div>

          {/* Phone (WhatsApp) OTP */}
          <div className="otp-block">
            <label>WhatsApp {verified.phone && <span className="done">✓</span>}</label>
            <input
              type="text"
              inputMode="numeric"
              maxLength={6}
              placeholder="000000"
              value={codes.phone}
              onChange={(e) => setCodes({ ...codes, phone: e.target.value.replace(/\D/g, '') })}
              disabled={verified.phone}
            />
            {!verified.phone && (
              <>
                <button
                  type="button"
                  onClick={() => verify('phone')}
                  disabled={loading}
                  style={{
                    marginTop: '0.5rem',
                    background: '#e63946',
                    border: 'none',
                    borderRadius: '4px',
                    color: '#fff',
                    cursor: 'pointer',
                    padding: '0.4rem 0',
                    width: '100%',
                    fontSize: '0.8rem',
                  }}
                >
                  Подтвердить
                </button>
                <button
                  type="button"
                  className="resend-btn"
                  onClick={() => resend('phone')}
                  disabled={cooldown.phone > 0}
                >
                  {cooldown.phone > 0 ? `Повтор через ${cooldown.phone}с` : 'Отправить снова'}
                </button>
              </>
            )}
          </div>
        </div>

        <p className="auth-footer" style={{ marginTop: '1.5rem' }}>
          <a href="/register">← Назад к регистрации</a>
        </p>
      </div>
    </div>
  );
}

export default VerifyOTPPage;
