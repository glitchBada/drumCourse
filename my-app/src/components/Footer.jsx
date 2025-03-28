import Logo from '../imgs/logo.png'
import "./Footer.scss"
import Facebook from '../imgs/facebook.png'
import Youtube from '../imgs/youtube.png'
import Instagram from '../imgs/instagram.png'
import VK from '../imgs/vk.png'


function Footer() {
    return (

      <>
        <div className="footer">
            <div className="logo">
                <img src={Logo} alt="" />
            </div>
            <div className="social">
                <a href="https://youtu.be/dQw4w9WgXcQ?si=kcl3lWqiZ_QQLxa3">
                    <img src={Facebook} alt="" />
                </a>
                <a href="https://youtu.be/dQw4w9WgXcQ?si=kcl3lWqiZ_QQLxa3">
                    <img src={Youtube} alt="" />
                </a>
                <a href="https://www.instagram.com/drumcourses.bishkek?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==">
                    <img src={Instagram} alt="" />
                </a>
                <a href="https://youtu.be/dQw4w9WgXcQ?si=kcl3lWqiZ_QQLxa3">
                    <img src={VK} alt="" />
                </a>
            </div>
            <div className="number">
                <a href="https://wa.me/996550172225">
                    <svg xmlns="http://www.w3.org/2000/svg" height="17px" width="17px" fill="gray" viewBox="0 0 512 512"><path d="M164.9 24.6c-7.7-18.6-28-28.5-47.4-23.2l-88 24C12.1 30.2 0 46 0 64C0 311.4 200.6 512 448 512c18 0 33.8-12.1 38.6-29.5l24-88c5.3-19.4-4.6-39.7-23.2-47.4l-96-40c-16.3-6.8-35.2-2.1-46.3 11.6L304.7 368C234.3 334.7 177.3 277.7 144 207.3L193.3 167c13.7-11.2 18.4-30 11.6-46.3l-40-96z"/></svg>
                    <p>+996 (550) 172 - 225</p>
                </a>
            </div>
            <div className="OsOO">
                <p>Все права защищены. 2019</p>
            </div>
        </div>
      </>
    );
}
export default Footer;