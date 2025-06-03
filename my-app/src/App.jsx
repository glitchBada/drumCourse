import './App.scss';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Updated imports
import Header from './components/Header';
import FirstHomePage from './pages/firstHomePage/FPage';
import Footer from './components/Footer'
import SecondPage from './pages/secondPage/SPage';
import ProductDetail from './pages/productditails/ProductDetail'
import ProductList from './pages/productlist/ProductList';
import CategoryDetail from './pages/CategoryDetail/CategoryDetail'
import Error404 from './pages/404/Error404';
import BlogPosts from './pages/blog/BlogPosts';
import FloatingMenu from './components/FloatingMenu';
import Teachers from './pages/teachers/Teachers';


function App() {
  return (
    <>
      <div className='App'>
        <Header />
          <div>
            <Routes>
              <Route path='/home' element={<FirstHomePage/>} />
              <Route path='/study' element={<SecondPage />} />
              <Route path="/drum.music.stuf" element={<ProductList />} />
              <Route path="/product/:slug" element={<ProductDetail />} />
              <Route path="/category/:slug" element={<CategoryDetail />} />
              <Route path="*" element={<Error404 />} />
              <Route path='/blog' element={<BlogPosts />} />
              <Route path='/teachers' element={<Teachers />} />
            </Routes>
          </div>
        <FloatingMenu />
        <Footer />
      </div>
    </>
  );
}

export default App;
