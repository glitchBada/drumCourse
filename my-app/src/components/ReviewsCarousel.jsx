import React, { useState, useEffect } from 'react';
import Slider from 'react-slick';
import api from '../api/axios';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './ReviewsCarrousel.scss'

const ReviewsCarousel = () => {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await api.get('/reviews/api/reviews/');
        setReviews(response.data);
      } catch (error) {
        console.error('Ошибка загрузки отзывов:', error);
      }
    };
    fetchReviews();
  }, []);

  const settings = {
    dots: true,
    infinite: true,
    speed: 3000,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 6000,
    centerMode: true,       // Центрирование слайдов
    // arrows: false,
  };

  return (
    <div className="reviews-carousel">
      <Slider {...settings}>
        {reviews.map((review, index) => (
          <div key={index} className="review-slide">
            <div className="author-info">
              {review.photo_url && (
                <img 
                  src={review.photo_url} 
                  alt={review.author_name} 
                  className="author-photo"
                />
              )}
              <h3 className="author-name">{review.author_name}</h3>
            </div>
            <p className="review-text">{review.text}</p>
          </div>
        ))}
      </Slider>
    </div>
  );
};

export default ReviewsCarousel;