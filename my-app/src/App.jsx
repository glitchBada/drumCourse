import './App.scss';
import { Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Header from './components/Header';
import Footer from './components/Footer';
import FloatingMenu from './components/FloatingMenu';

import FirstHomePage from './pages/firstHomePage/FPage';
import SecondPage from './pages/secondPage/SPage';
import ProductList from './pages/productlist/ProductList';
import ProductDetail from './pages/productditails/ProductDetail';
import CategoryDetail from './pages/CategoryDetail/CategoryDetail';
import BlogPosts from './pages/blog/BlogPosts';
import Teachers from './pages/teachers/Teachers';
import Error404 from './pages/404/Error404';

import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import VerifyOTPPage from './pages/auth/VerifyOTPPage';
import CabinetPage from './pages/cabinet/CabinetPage';
import OrdersPage from './pages/cabinet/OrdersPage';
import OrderDetailPage from './pages/cabinet/OrderDetailPage';

function App() {
  return (
    <AuthProvider>
      <div className='App'>
        <Header />
        <div>
          <Routes>
            <Route path='/home' element={<FirstHomePage />} />
            <Route path='/study' element={<SecondPage />} />
            <Route path="/drum.music.stuf" element={<ProductList />} />
            <Route path="/product/:slug" element={<ProductDetail />} />
            <Route path="/category/:slug" element={<CategoryDetail />} />
            <Route path='/blog' element={<BlogPosts />} />
            <Route path='/teachers' element={<Teachers />} />

            <Route path='/login' element={<LoginPage />} />
            <Route path='/register' element={<RegisterPage />} />
            <Route path='/verify' element={<VerifyOTPPage />} />

            <Route path='/cabinet' element={
              <ProtectedRoute><CabinetPage /></ProtectedRoute>
            } />
            <Route path='/cabinet/orders' element={
              <ProtectedRoute><OrdersPage /></ProtectedRoute>
            } />
            <Route path='/cabinet/orders/:id' element={
              <ProtectedRoute><OrderDetailPage /></ProtectedRoute>
            } />

            <Route path="*" element={<Error404 />} />
          </Routes>
        </div>
        <FloatingMenu />
        <Footer />
      </div>
    </AuthProvider>
  );
}

export default App;
