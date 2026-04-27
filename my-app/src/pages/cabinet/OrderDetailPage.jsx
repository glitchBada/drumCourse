import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../api/axios';
import { CabinetSidebar } from './CabinetPage';
import './Cabinet.scss';

const STATUS_LABELS = {
  pending: 'В ожидании',
  processing: 'В оформлении и доставке',
  cancelled: 'Отменена',
  delivered: 'Получено',
};

const TYPE_LABELS = {
  product: 'Заказ товара',
  trial: 'Пробный урок',
};

function ConfirmModal({ onConfirm, onCancel, loading }) {
  return (
    <div className="confirm-overlay">
      <div className="confirm-modal">
        <h3>Подтверждение получения</h3>
        <p>
          Подтверждая получение, вы принимаете ответственность. Продавец более не обязан
          предпринимать действия по данной заявке. Это действие нельзя отменить.
        </p>
        <div className="modal-actions">
          <button className="cancel-btn" onClick={onCancel} disabled={loading}>
            Отмена
          </button>
          <button className="ok-btn" onClick={onConfirm} disabled={loading}>
            {loading ? 'Подтверждаю...' : 'Подтвердить'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function OrderDetailPage() {
  const { user } = useAuth();
  const { id } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [confirming, setConfirming] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    api.get(`/api/applications/${id}/`)
      .then((res) => setOrder(res.data))
      .catch(() => setError('Заявка не найдена.'))
      .finally(() => setLoading(false));
  }, [id]);

  const handleConfirm = async () => {
    setConfirming(true);
    try {
      const res = await api.post(`/api/applications/${id}/confirm/`);
      setOrder(res.data);
      setSuccess('Получение подтверждено. Спасибо!');
      setShowModal(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка подтверждения.');
      setShowModal(false);
    } finally {
      setConfirming(false);
    }
  };

  return (
    <div className="cabinet-page">
      {showModal && (
        <ConfirmModal
          onConfirm={handleConfirm}
          onCancel={() => setShowModal(false)}
          loading={confirming}
        />
      )}

      <div className="cabinet-container">
        <div className="cabinet-header">
          <h1>Личный <span>кабинет</span></h1>
        </div>
        <div className="cabinet-grid">
          <CabinetSidebar user={user} />
          <main className="cabinet-content">
            {loading && <div className="loading-screen">Загрузка...</div>}
            {error && !order && <div className="cabinet-alert error">{error}</div>}

            {order && (
              <div className="order-detail">
                <Link to="/cabinet/orders" className="back-link">← Назад к заявкам</Link>

                <h2>Заявка <span>#{order.id}</span></h2>

                {error && <div className="cabinet-alert error">{error}</div>}
                {success && <div className="cabinet-alert success">{success}</div>}

                <div className="detail-row">
                  <span className="label">Тип:</span>
                  <span className="value">{TYPE_LABELS[order.type] || order.type}</span>
                </div>

                {order.display_product_name && (
                  <div className="detail-row">
                    <span className="label">Товар:</span>
                    <span className="value">{order.display_product_name}</span>
                  </div>
                )}

                <div className="detail-row">
                  <span className="label">Статус:</span>
                  <span className={`status-badge ${order.status}`}>
                    {STATUS_LABELS[order.status] || order.status}
                  </span>
                </div>

                {order.message && (
                  <div className="detail-row">
                    <span className="label">Сообщение:</span>
                    <span className="value">{order.message}</span>
                  </div>
                )}

                <div className="detail-row">
                  <span className="label">Создана:</span>
                  <span className="value">
                    {new Date(order.created_at).toLocaleString('ru-RU')}
                  </span>
                </div>

                <div className="detail-row">
                  <span className="label">Обновлена:</span>
                  <span className="value">
                    {new Date(order.updated_at).toLocaleString('ru-RU')}
                  </span>
                </div>

                {order.admin_comment && (
                  <div className="admin-comment-box">
                    <strong>Комментарий администратора</strong>
                    {order.admin_comment}
                  </div>
                )}

                {order.status === 'processing' && (
                  <button
                    className="confirm-btn"
                    onClick={() => setShowModal(true)}
                  >
                    Подтвердить получение
                  </button>
                )}
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
