// import React, { useState, useEffect } from 'react';
// import { useParams } from 'react-router-dom'; // Import useParams for v6
// import axios from 'axios';
// import './ProductDetail.scss'

// function ProductDetail() {
//   const { slug } = useParams(); // Get slug from URL params
//   const [product, setProduct] = useState(null);
//   const [formData, setFormData] = useState({
//     name: '',
//     surname: '',
//     phone: '',
//     email: ''
//   });

//   useEffect(() => {
//     axios.get(`http://192.168.43.61:8000/api/products/${slug}/`)
//       .then(res => {
//         console.log('Product Data:', res.data); // Debug log
//         setProduct(res.data);
//       })
//       .catch(err => console.error('Error fetching product:', err));
//   }, [slug]);

//   const handleChange = (e) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     axios.post('http://192.168.43.61:8000/api/apply/', {
//       ...formData,
//       product_name: product.name
//     })
//       .then(() => {
//         alert('Мы очень благодарны за Ваш заказ, он успешно отправлен. В скором времени с вами свяжется продавец.');
//         setFormData({ name: '', surname: '', phone: '', email: '' });
//       })
//       .catch(err => console.error('Error submitting application:', err));
//   };

//   if (!product) return <div>Loading...</div>;

//   return (
//     <div className='productdet'>
//       <h1>{product.name}</h1>
//       <p>{product.description}</p>
//       <p>Цена:{product.price} сом</p>
      
//       <div className="gallery">
//         {product.images.map(image => (
//           <img key={image.id} src={image.image} alt={product.name} />
//         ))}
//       </div>

//       <form onSubmit={handleSubmit}>
//         <input
//           type="text"
//           name="name"
//           value={formData.name}
//           onChange={handleChange}
//           placeholder="Name"
//           required
//         />
//         <input
//           type="text"
//           name="surname"
//           value={formData.surname}
//           onChange={handleChange}
//           placeholder="Surname"
//           required
//         />
//         <input
//           type="tel"
//           name="phone"
//           value={formData.phone}
//           onChange={handleChange}
//           placeholder="Phone"
//           required
//         />
//         <input
//           type="email"
//           name="email"
//           value={formData.email}
//           onChange={handleChange}
//           placeholder="Email"
//           required
//         />
//         <button type="submit">Submit Application</button>
//       </form>
//     </div>
//   );
// }

// export default ProductDetail;

import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import lightGallery from 'lightgallery';
import 'lightgallery/css/lightgallery.css';
import 'lightgallery/css/lg-zoom.css';
import 'lightgallery/css/lg-thumbnail.css';
import lgThumbnail from 'lightgallery/plugins/thumbnail';
import lgZoom from 'lightgallery/plugins/zoom';
import './ProductDetail.scss';

function ProductDetail() {
  const { slug } = useParams();
  const [product, setProduct] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    surname: '',
    phone: '',
    email: ''
  });
  const galleryRef = useRef(null);

  useEffect(() => {
    axios.get(`http://192.168.43.61:8000/api/products/${slug}/`)
      .then(res => {
        console.log('Product Data:', res.data);
        setProduct(res.data);
      })
      .catch(err => console.error('Error fetching product:', err));
  }, [slug]);

  useEffect(() => {
    if (galleryRef.current && product) {
      lightGallery(galleryRef.current, {
        plugins: [lgThumbnail, lgZoom],
        speed: 500,
      });
    }
  }, [product]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://192.168.43.61:8000/api/apply/', {
      ...formData,
      product_name: product.name
    })
      .then(() => {
        alert('Мы очень благодарны за Ваш заказ, он успешно отправлен. В скором времени с вами свяжется продавец.');
        setFormData({ name: '', surname: '', phone: '', email: '' });
      })
      .catch(err => console.error('Error submitting application:', err));
  };

  if (!product) return <div>Loading...</div>;

  return (
    <div className="productdet">
      <h1 className='productnameindetails'>{product.name}</h1>
      <div className='imageGalleryAndDetails'>
        <div className="gallery" ref={galleryRef}>
        {product.images.map(image => (
          <a key={image.id} href={image.image}>
            <img src={image.image} alt={product.name} />
          </a>
        ))}
        </div>
        <div className='formanddet'>
          <p>{product.description}</p>
          <p>Цена: <span>{product.price} сом</span></p>
          <form className='formForDetails' onSubmit={handleSubmit}>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Имя"
              required
            />
            <input
              type="text"
              name="surname"
              value={formData.surname}
              onChange={handleChange}
              placeholder="Фамилия"
              required
            />
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="Телефон"
              required
            />
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Email"
              required
            />
            <button type="submit">Заказать!</button>
          </form>
        </div>
      </div>

      
      
    </div>
  );
}

export default ProductDetail;