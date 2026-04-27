import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../api/axios';
import { CabinetSidebar } from './CabinetPage';
import './Cabinet.scss';

const STATUS_LABELS = {
  pending: 'В ожидании',
  processing: 'В оформлении',
  cancelled: 'Отменена',
  delivered: 'Получено',
};

const TYPE_LABELS = {
  product: 'Заказ товара',
  trial: 'Пробный урок',
};

export default function OrdersPage() {
  const { user } = useAuth();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/api/applications/')
      .then((res) => setOrders(res.data))
      .catch(() => setError('Не удалось загрузить заявки.'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="cabinet-page">
      <div className="cabinet-container">
        <div className="cabinet-header">
          <h1>Личный <span>кабинет</span></h1>
        </div>
        <div className="cabinet-grid">
          <CabinetSidebar user={user} />
          <main className="cabinet-content">
            <h2>Мои <span>заявки</span></h2>

            {loading && <div className="loading-screen">Загрузка...</div>}
            {error && <div className="cabinet-alert error">{error}</div>}

            {!loading && !error && orders.length === 0 && (
              <div className="empty-state">
                <p>У вас пока нет заявок.</p>
                <p>
                  Перейдите в <a href="/drum.music.stuf">интернет-магазин</a> или оставьте заявку на{' '}
                  <a href="/home">пробный урок</a>.
                </p>
              </div>
            )}

            {!loading && orders.length > 0 && (
              <div className="orders-list">
                {orders.map((order) => (
                  <Link key={order.id} to={`/cabinet/orders/${order.id}`} className="order-card">
                    <div className="order-top">
                      <span className="order-type">{TYPE_LABELS[order.type] || order.type}</span>
                      <span className={`status-badge ${order.status}`}>
                        {STATUS_LABELS[order.status] || order.status}
                      </span>
                    </div>
                    {order.display_product_name && (
                      <div className="order-product">{order.display_product_name}</div>
                    )}
                    <div className="order-date">
                      #{order.id} · {new Date(order.created_at).toLocaleDateString('ru-RU')}
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
