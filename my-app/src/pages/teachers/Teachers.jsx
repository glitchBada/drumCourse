import Maratcardphoto from "../../imgs/1742146928185.jpg"
import Zucardphoto from "../../imgs/1742146928179.jpg"
import Alinacardphoto from "../../imgs/1742146928173.jpg"
import "./Teachers.scss"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {faPhone} from '@fortawesome/free-solid-svg-icons';
import {faWhatsapp, faInstagram} from '@fortawesome/free-brands-svg-icons'

function Teachers () {
return (
    <>
        <div className="teacherspage">
            <div className="titleTeachers">
                <h1>наши педо<span>гоги</span></h1>
            </div>
            <div className="aboutteachers">
                <p>Lorem ipsum dolor sit amet.</p>
                <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Blanditiis porro, autem at eum ab quos?</p>
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quod fugit quam sapiente corporis iste accusantium, reprehenderit iure, voluptates unde facere fugiat et a.</p>
                <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vero!</p>
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit.</p>
            </div>
            <iframe src="https://www.youtube.com/embed/cLwTABgZvpM?si=qjmp538fW02G8Dej" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen className="youtubeplayer"></iframe>
            <div className="cards">
                <div className="theachers maratteach">
                    <img className="cardpicture" src={Maratcardphoto} alt="" />
                    <h2>Марат Миндубаев</h2>
                    <p>34 года, Очень любит професионально играть на барабанах, отжигать на вечеринках. Характер веселый. Не женат.</p>
                    <a href="#" className="smartphonr">
                        <FontAwesomeIcon className="smartphoneicon" icon={faWhatsapp} color="red"/>
                        Телефон
                    </a>

                </div>
                <div className="theachers zuteach">
                    <img className="cardpicture" src={Zucardphoto} alt="" />
                    <h2>ZU ...</h2>
                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quaerat ipsam debitis nobis dolores explicabo deleniti harum, voluptates nisi perferendis temporibus, quia, culpa maxime dicta quidem sunt mollitia quibusdam nam voluptas error doloribus est iste?</p>
                    <a href="#" className="smartphonr">
                        <FontAwesomeIcon className="smartphoneicon" icon={faWhatsapp} color="red"/>
                        Телефон
                    </a>

                </div>
                <div className="theachers alinateach">
                    <img className="cardpicture" src={Alinacardphoto} alt="" />
                    <h2>Алина ...</h2>
                    <p>Очень хорошая память, особенно помнит опечатки в отзывах, особено "бараны"</p>
                    <a href="#" className="smartphonr">
                        <FontAwesomeIcon className="smartphoneicon" icon={faWhatsapp} color="red"/>
                        Телефон
                    </a>

                </div>
            </div>
        </div>
    </>
);
}

export default Teachers;