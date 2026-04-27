import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import lightGallery from 'lightgallery';
import 'lightgallery/css/lightgallery.css';
import 'lightgallery/css/lg-zoom.css';
import 'lightgallery/css/lg-thumbnail.css';
import lgThumbnail from 'lightgallery/plugins/thumbnail';
import lgZoom from 'lightgallery/plugins/zoom';
import api from '../../api/axios';
import { useAuth } from '../../context/AuthContext';
import './ProductDetail.scss';

function ProductDetail() {
  const { slug } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const [product, setProduct] = useState(null);
  const [message, setMessage] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [submitError, setSubmitError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const galleryRef = useRef(null);

  useEffect(() => {
    api.get(`/api/products/${slug}/`)
      .then((res) => setProduct(res.data))
      .catch((err) => console.error('Error fetching product:', err));
  }, [slug]);

  useEffect(() => {
    if (galleryRef.current && product) {
      lightGallery(galleryRef.current, {
        plugins: [lgThumbnail, lgZoom],
        speed: 500,
      });
    }
  }, [product]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isAuthenticated) {
      navigate('/login', { state: { from: { pathname: `/product/${slug}` } } });
      return;
    }

    setSubmitError('');
    setSubmitting(true);
    try {
      await api.post('/api/applications/', {
        type: 'product',
        product: product.id,
        message,
      });
      setSubmitted(true);
    } catch (err) {
      const data = err.response?.data;
      setSubmitError(
        data?.detail ||
        Object.values(data || {}).flat().join(' ') ||
        'Ошибка отправки заявки.'
      );
    } finally {
      setSubmitting(false);
    }
  };

  if (!product) return <div className="loading-screen">Загрузка...</div>;

  return (
    <div className="productdet">
      <h1 className='productnameindetails'>{product.name}</h1>
      <div className='imageGalleryAndDetails'>
        <div className="gallery" ref={galleryRef}>
          {product.images.map((image) => (
            <a key={image.id} href={image.image}>
              <img src={image.image} alt={product.name} />
            </a>
          ))}
        </div>

        <div className='formanddet'>
          <p>{product.description}</p>
          <p>Цена: <span>{product.price} сом</span></p>

          {submitted ? (
            <div style={{ color: '#5cb85c', padding: '1rem 0', fontSize: '0.95rem' }}>
              Заявка отправлена! <a href="/cabinet/orders" style={{ color: '#e63946' }}>Посмотреть заявки</a>
            </div>
          ) : (
            <form className='formForDetails' onSubmit={handleSubmit}>
              {!isAuthenticated && (
                <p style={{ color: '#aaa', fontSize: '0.85rem', marginBottom: '0.75rem' }}>
                  Для заказа необходима{' '}
                  <a href="/login" style={{ color: '#e63946' }}>авторизация</a>.
                </p>
              )}
              {submitError && (
                <p style={{ color: '#ff6b6b', fontSize: '0.85rem', marginBottom: '0.75rem' }}>
                  {submitError}
                </p>
              )}
              <input
                type="text"
                name="message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Комментарий к заказу (необязательно)"
              />
              <button type="submit" disabled={submitting}>
                {submitting ? 'Отправка...' : 'Заказать!'}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
