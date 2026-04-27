import './Header.scss'
import Logo from '../imgs/Drum_courses_white.png'
import Burgermenu from './BurgerMenu';
import { useAuth } from '../context/AuthContext';

function Header() {
    const { isAuthenticated, user } = useAuth();

    return (
        <header className='Hheader'>
            <Burgermenu />
            <a className="logo" href='/home'>
                <img className='imglogo' src={Logo} alt="" />
            </a>
            <div className="headMenu">
                <div className="firstheaderlayer">
                    <a href="#" className="firstlayerlinks headerlinks adres">
                        <svg xmlns="http://www.w3.org/2000/svg" height='20px' width="22px" viewBox="0 0 384 512"><path fill='gray' d="M215.7 499.2C267 435 384 279.4 384 192C384 86 298 0 192 0S0 86 0 192c0 87.4 117 243 168.3 307.2c12.3 15.3 35.1 15.3 47.4 0zM192 128a64 64 0 1 1 0 128 64 64 0 1 1 0-128z"/></svg>
                        <p>г. Бишкек, Абдырахманова 36</p>
                    </a>
                    <a href="#" className="firstlayerlinks headerlinks phone">
                    <svg xmlns="http://www.w3.org/2000/svg" height="17px" width="17px" fill="gray" viewBox="0 0 512 512"><path d="M164.9 24.6c-7.7-18.6-28-28.5-47.4-23.2l-88 24C12.1 30.2 0 46 0 64C0 311.4 200.6 512 448 512c18 0 33.8-12.1 38.6-29.5l24-88c5.3-19.4-4.6-39.7-23.2-47.4l-96-40c-16.3-6.8-35.2-2.1-46.3 11.6L304.7 368C234.3 334.7 177.3 277.7 144 207.3L193.3 167c13.7-11.2 18.4-30 11.6-46.3l-40-96z"/></svg>
                        <p>+996 (550) 172 - 225</p>
                    </a>
                    <div className="firstlayerlinks auth-nav">
                        {isAuthenticated ? (
                            <a href="/cabinet" className="headerlinks auth-link">
                                {user?.first_name || 'Кабинет'}
                            </a>
                        ) : (
                            <a href="/login" className="headerlinks auth-link">
                                Войти
                            </a>
                        )}
                    </div>
                </div>
                <div className="secondheaderlayer">
                    <a href="/home" className="secondlayerlinks headerlinks">О школе</a>
                    <a href="/study" className="secondlayerlinks headerlinks">Обучение</a>
                    <a href="/teachers" className="secondlayerlinks headerlinks">Педагоги</a>
                    <a href="/blog" className="secondlayerlinks headerlinks">События</a>
                    <a href="/drum.music.stuf" className="secondlayerlinks headerlinks linktomarket">Интернет-Магазин DRUMROOM</a>
                </div>
            </div>
        </header>
    );
  }

  export default Header;
