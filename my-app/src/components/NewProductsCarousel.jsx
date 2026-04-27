import React, { useState, useEffect } from 'react';
import Slider from 'react-slick';
import api from '../api/axios';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './NewProductsCarousel.scss'

function NewProductsCarousel() {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        api.get('/api/new-products/').then(res => setProducts(res.data));
    }, []);

    const settings = {
        dots: true,
        infinite: true,
        speed: 600,
        slidesToShow: 6,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 4000,
        arrows: false,
        responsive:[
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2,
                    // rows: 2,
                },
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    // rows: 2,
                },
            },
        ]
    };

    return (
        <div>
            <h2 className='Novinki'>Новинки</h2>
            <Slider className='newslider' {...settings}>
                {products.map(product => (
                    <div key={product.id}>
                        <a href={`/product/${product.slug}`}>
                            {product.images.length > 0 && (
                                <img
                                src={product.images[0].image}
                                alt={product.name}
                                className="newProduct-image"
                                />
                            )}
                        </a>
                    </div>
                ))}
            </Slider>
        </div>
    );
}

export default NewProductsCarousel;