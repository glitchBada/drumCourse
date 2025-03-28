// CategoryDetail.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import './CategoryDetail.scss'; // Стили для детальной страницы

const CategoryDetail = () => {
  const [products, setProducts] = useState([]);
  const [categoryName, setCategoryName] = useState('');
  const { slug } = useParams(); // Получаем slug категории из URL

  useEffect(() => {
    const fetchCategoryProducts = async () => {
      try {
        const url = `http://192.168.43.61:8000/api/products/?category=${slug}`;
        const response = await axios.get(url);
        console.log('Category Products:', response.data);
        setProducts(response.data);
        // Устанавливаем название категории (в идеале получать из API)
        setCategoryName(slug); // Замени на настоящее имя категории, если API его возвращает
      } catch (error) {
        console.error('Error fetching category products:', error);
      }
    };
    fetchCategoryProducts();
  }, [slug]);

  return (
    <div className="category-detail">
      <h1>Товары в категории: {categoryName}</h1>
      {products.length === 0 ? (
        <p>Нет товаров в этой категории</p>
      ) : (
        <div className="product-grid">
          {products.map(product => (
            <div key={product.id} className="product-card">
              <h3 className='prodctsh3'>{product.name}</h3>
              {product.images.length > 0 && (
                <img
                  src={product.images[0].image}
                  alt={product.name}
                  className="product-image"
                />
              )}
              <div className='linkend'>
                <p>Цена: {product.price} сом</p>
                <p>Категория: {product.category}</p>
                <p>Бренд: {product.brand}</p>
                <Link className='productdetails' to={`/product/${product.slug}`}>Посмотреть детали</Link>
              </div>
              
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CategoryDetail;