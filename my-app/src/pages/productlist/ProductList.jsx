// import React, { useState, useEffect } from 'react';
// import axios from 'axios';
// import { useNavigate, useLocation, Link } from 'react-router-dom';
// import './ProductList.scss';
// import NewProductsCarousel from '../../components/NewProductsCarousel'

// const ProductList = () => {
//   const [products, setProducts] = useState([]);
//   const [categories, setCategories] = useState([]);
//   const [brands, setBrands] = useState([]);
//   const [selectedCategory, setSelectedCategory] = useState('');
//   const [selectedBrand, setSelectedBrand] = useState('');
//   const [searchTerm, setSearchTerm] = useState('');

//   const location = useLocation();
//   const navigate = useNavigate();

//   useEffect(() => {
//     const fetchCategories = async () => {
//       try {
//         const response = await axios.get('http://192.168.43.61:8000/api/categories/');
//         console.log('Categories:', response.data);
//         setCategories(response.data);
//       } catch (error) {
//         console.error('Error fetching categories:', error);
//       }
//     };

//     const fetchBrands = async () => {
//       try {
//         const response = await axios.get('http://192.168.43.61:8000/api/brands/');
//         console.log('Brands:', response.data);
//         setBrands(response.data);
//       } catch (error) {
//         console.error('Error fetching brands:', error);
//       }
//     };

//     fetchCategories();
//     fetchBrands();
//   }, []);

//   useEffect(() => {
//     const fetchProducts = async () => {
//       try {
//         const params = new URLSearchParams(location.search);
//         const search = params.get('search') || '';
//         const queryParams = new URLSearchParams();

//         if (selectedCategory) queryParams.append('category', selectedCategory);
//         if (selectedBrand) queryParams.append('brand', selectedBrand);
//         if (search) queryParams.append('search', search);

//         const url = `http://192.168.43.61:8000/api/products/?${queryParams.toString()}`;
//         const response = await axios.get(url);
//         console.log('Products:', response.data);
//         setProducts(response.data);
//       } catch (error) {
//         console.error('Error fetching products:', error);
//       }
//     };
//     fetchProducts();
//   }, [selectedCategory, selectedBrand, location.search]);

//   useEffect(() => {
//     const params = new URLSearchParams(location.search);
//     const search = params.get('search') || '';
//     setSearchTerm(search);
//   }, [location.search]);

//   const handleCategoryChange = (e) => {
//     setSelectedCategory(e.target.value);
//   };

//   const handleBrandChange = (e) => {
//     setSelectedBrand(e.target.value);
//   };

//   const handleSearch = (e) => {
//     e.preventDefault();
//     const params = new URLSearchParams(location.search);
//     if (searchTerm) {
//       params.set('search', searchTerm);
//     } else {
//       params.delete('search');
//     }
//     navigate(`?${params.toString()}`);
//   };

//   return (
//     <div className="product-list">
//       <h1>НАШ АССОРТИМЕНТ</h1>

//       {/* Ссылки на категории */}
//       <ul className="category-list">
//         {categories.map(category => (
//           <li key={category.id}>
//             <Link to={`/category/${category.slug}`}>{category.name}</Link>
//           </li>
//         ))}
//       </ul>

//       {/* Форма поиска */}
//       <form onSubmit={handleSearch}>
//         <input
//           type="text"
//           value={searchTerm}
//           onChange={(e) => setSearchTerm(e.target.value)}
//           placeholder="Search products..."
//         />
//         <button type="submit">Search</button>
//       </form>

//       {/* Выбор категории */}
//       <select value={selectedCategory} onChange={handleCategoryChange}>
//         <option value="">Все категории</option>
//         {categories.map(category => (
//           <option key={category.id} value={category.slug}>
//             {category.name}
//           </option>
//         ))}
//       </select>

//       {/* Выбор бренда */}
//       <select value={selectedBrand} onChange={handleBrandChange}>
//         <option value="">Все бренды</option>
//         {brands.map(brand => (
//           <option key={brand.id} value={brand.slug}>
//             {brand.name}
//           </option>
//         ))}
//       </select>

//       <NewProductsCarousel />

//       {/* Отображение продуктов */}
//       {products.length === 0 ? (
//         <p>Загрузка...</p>
//       ) : (
//         <div className="product-grid">
//           {products.map(product => (
//             <div key={product.id} className="product-card">
//               <h3 className='prodctsh3'>{product.name}</h3>
//               {product.images.length > 0 && (
//                 <img
//                   src={product.images[0].image}
//                   alt={product.name}
//                   className="product-image"
//                 />
//               )}
//               <div className='linkend'>
//                 <p>Цена: {product.price} сом</p>
//                 <p>Категория: {product.category}</p>
//                 <p>Бренд: {product.brand}</p>
//                 <Link className='productdetails' to={`/product/${product.slug}`}>Посмотреть детали</Link>
//               </div>
              
//             </div>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// };

// export default ProductList;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './ProductList.scss';
import NewProductsCarousel from '../../components/NewProductsCarousel';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedBrand, setSelectedBrand] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('http://194.87.76.29:8000/api/categories/');
        console.log('Categories:', response.data);
        setCategories(response.data);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };

    const fetchBrands = async () => {
      try {
        const response = await axios.get('http://194.87.76.29:8000/api/brands/');
        console.log('Brands:', response.data);
        setBrands(response.data);
      } catch (error) {
        console.error('Error fetching brands:', error);
      }
    };

    fetchCategories();
    fetchBrands();
  }, []);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const params = new URLSearchParams(location.search);
        const search = params.get('search') || '';
        const queryParams = new URLSearchParams();

        if (selectedCategory) queryParams.append('category', selectedCategory);
        if (selectedBrand) queryParams.append('brand', selectedBrand);
        if (search) queryParams.append('search', search);

        const url = `http://194.87.76.29:8000/api/products/?${queryParams.toString()}`;
        const response = await axios.get(url);
        console.log('Products:', response.data);
        setProducts(response.data);
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    };
    fetchProducts();
  }, [selectedCategory, selectedBrand, location.search]);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const search = params.get('search') || '';
    setSearchTerm(search);
  }, [location.search]);

  const handleCategoryChange = (e) => {
    setSelectedCategory(e.target.value);
  };

  const handleBrandSelect = (brandSlug) => {
    setSelectedBrand(brandSlug === selectedBrand ? '' : brandSlug); // Toggle selection
  };

  const handleSearch = (e) => {
    e.preventDefault();
    const params = new URLSearchParams(location.search);
    if (searchTerm) {
      params.set('search', searchTerm);
    } else {
      params.delete('search');
    }
    navigate(`?${params.toString()}`);
  };

  const sliderSettings = {
    dots: false,
    infinite: true,
    speed: 500,
    slidesToShow: 4,
    slidesToScroll: 1,
    rows: 2, 
    slidesPerRow: 1,
    responsive: [
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 4,
          rows: 2,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          rows: 2,
        },
      },
    ],
  };

  return (
    <div className="product-list">
      <h1 className='NashAsortiment'>НАШ АССОРТИМЕНТ</h1>
      <NewProductsCarousel />
      <div className='categorylist-and-searching'>
        {/* Ссылки на категории */}
        <ul className="category-list">
          {categories.map(category => (
            <li key={category.id}>
              <Link to={`/category/${category.slug}`}>{category.name}</Link>
            </li>
          ))}
        </ul>

        {/* Форма поиска */}
        <form className='searching' onSubmit={handleSearch}>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Поиск..."
          />
          <button type="submit">Поиск</button>
          
        </form>
      </div>
      

      {/* Выбор категории */}
      
      <select className='selectcategory' value={selectedCategory} onChange={handleCategoryChange}>
        <option value="">Все категории</option>
        {categories.map(category => (
          <option key={category.id} value={category.slug}>
            {category.name}
          </option>
        ))}
      </select>

      {/* Слайдер брендов */}
      <div className="brand-slider">
        <Slider className='badasslider'{...sliderSettings}>
          {brands.map(brand => (
            <div
            style="display:flex"
              key={brand.id}
              className={` brand-item ${selectedBrand === brand.slug ? 'selected' : ''}`}
              onClick={() => handleBrandSelect(brand.slug)}
            >
              {brand.logo ? (
                <img src={brand.logo} alt={brand.name} className="brand-logo" />
              ) : (
                <span>{brand.name}</span>
              )}
            </div>
          ))}
        </Slider>
      </div>

      
      {/* Отображение продуктов */}
      {products.length === 0 ? (
        <p>НИЧЕГО НЕ НАЙДЕНО</p>
      ) : (
        <div className="product-grid">
          {products.map(product => (
            <div key={product.id} className="product-card">
              <h3 className="prodctsh3">{product.name}</h3>
              {product.images.length > 0 && (
                <img
                  src={product.images[0].image}
                  alt={product.name}
                  className="product-image"
                />
              )}
              <div className="linkend">
                <p>Цена: {product.price} сом</p>
                <p>Категория: {product.category}</p>
                <p>Бренд: {product.brand}</p>
                <Link className="productdetails" to={`/product/${product.slug}`}>
                  Посмотреть детали
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProductList;