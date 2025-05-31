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
                <h1>наши <span>педагоги</span></h1>
            </div>
            <div className="aboutteachers">
                <p>Команда преподавателей нашей школы — это профессиональные барабанщики с большим концертным и студийным опытом. Каждый из них — не только практикующий музыкант, но и увлечённый педагог, способный делиться своими знаниями с учениками любого уровня.</p>
                <p>Наши преподаватели владеют разными стилями и техниками игры: от попсы до метала. Они умеют адаптировать обучение под интересы и цели каждого ученика — будь то хобби, подготовка к поступлению в музыкальное учебное заведение или развитие профессиональных навыков.</p>
                <p>Главное для нас — это индивидуальный подход. Наши преподаватели легко находят общий язык с детьми, подростками и взрослыми, создавая комфортную атмосферу на уроках и помогая каждому раскрыть свой музыкальный потенциал.</p>
            </div>
            <iframe src="https://www.youtube.com/embed/cLwTABgZvpM?si=qjmp538fW02G8Dej" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen className="youtubeplayer"></iframe>
            <div className="cards">
                <div className="theachers maratteach">
                    <img className="cardpicture" src={Maratcardphoto} alt="" />
                    <h2>Марат Миндубаев</h2>
                    <p>34 года, Очень любит професионально играть на барабанах, отжигать на вечеринках. Характер веселый. Не женат.</p>
                    {/* <a href="#" className="smartphonr">
                        <FontAwesomeIcon className="smartphoneicon" icon={faWhatsapp} color="red"/>
                        Телефон
                    </a> */}

                </div>
                <div className="theachers zuteach">
                    <img className="cardpicture" src={Zucardphoto} alt="" />
                    <h2>ZU ...</h2>
                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quaerat ipsam debitis nobis dolores explicabo deleniti harum, voluptates nisi perferendis temporibus, quia, culpa maxime dicta quidem sunt mollitia quibusdam nam voluptas error doloribus est iste?</p>
                    {/* <a href="#" className="smartphonr">
                        <FontAwesomeIcon className="smartphoneicon" icon={faWhatsapp} color="red"/>
                        Телефон
                    </a> */}

                </div>
                <div className="theachers alinateach">
                    <img className="cardpicture" src={Alinacardphoto} alt="" />
                    <h2>Алина ...</h2>
                    <p>Очень хорошая память, особенно помнит опечатки в отзывах, особено "бараны"</p>
                    {/* <a href="#" className="smartphonr">
                        <FontAwesomeIcon className="smartphoneicon" icon={faWhatsapp} color="red"/>
                        Телефон
                    </a> */}

                </div>
            </div>
        </div>
    </>
);
}

export default Teachers;