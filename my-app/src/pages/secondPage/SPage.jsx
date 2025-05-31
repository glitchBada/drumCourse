import './SPage.scss'
import PlayB from '../../imgs/play-buttom.png'
import BaseCourse from '../../imgs/basecourse.png'
import StandartCourse from '../../imgs/standartcourse.png'
import CrashCourse from '../../imgs/crashcourse.png'
import VipCourse from '../../imgs/vipcourse.png'
import ReviewsCarousel from '../../components/ReviewsCarousel'
 
// https://grok.com/share/bGVnYWN5_fa3856d6-3da8-4570-94ac-463ffaee3cdd

function SecondPage() {
    return (
        <>
            <section className="sectionsoffirstpage sec21">
                <h1 className='stuudy'>ОБУЧЕ<span>НИЕ</span></h1>
                <div className='redgradient'>
                </div>
                <div className='druum'>
                    <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">
                        <img src={PlayB} alt="" />
                    </a>
                </div>
                <button className='startStudy'>
                    <a href="#">Стать барабанщиком</a>
                </button>
            </section>
            <section className='sectionsoffirstpage sec22'>
                <h2>МЕТОДИКА <span>ОБУЧЕНИЯ</span></h2>
                <div className='textpage2'>
                    <p>В Школе Drum Course обучаться игре на барабанах могут все желающие с 7–8 лет и старше, независимо от уровня подготовки. Мы практикуем гибкий индивидуальный подход, выстраивая обучение в зависимости от целей и запроса каждого ученика.</p>
                    <p>Главный акцент — на практику. Мы уделяем максимум времени игровой практике, развитию техники и музыкального мышления. При этом мы обязательно обучаем базовой теории музыки, необходимой для уверенного и осознанного музицирования.
                    </p>
                    <p>Обучение курсу проходит в несколько этапов и включает в себя как практические, так и теоретические знания.</p>

                </div>
            </section>
            <section className='sectionsoffirstpage sec23'>
                <h2>ОСНОВНЫЕ <span>ПРОГРАММЫ КУРСА</span></h2>
                <div className='programs'>
                    <div className="program">
                        <div className='programimg'>
                            <img src={BaseCourse} alt="" />
                        </div>
                        <div className='programtext'>
                            <h4>Базовый курс</h4>
                            <p>Базовый курс обучения на барабанах идеально подходит для новичков. Курс длится 2 месяца. 1 занятие = 1 час 30 минут. Занятия проходят на акустических барабанных установках. Все занятия индивидуальные!</p>
                        </div>
                    </div>
                    <div className="program">
                        <div className='programimg'>
                            <img src={StandartCourse} alt="" />
                        </div>
                        <div className='programtext'>
                            <h4>Основной курс</h4>
                            <p>Основной курс подходит для уже играющих барабанщиков, желающих улучшить свое мастерство, качество звучания, саунд, грув, и более профессионально обучиться игре барабанах.Курс длится 12 месяцев. 1 занятие = 1 час 30 минут. Занятия проходят на акустических барабанных установках. Все занятия индивидуальные!</p>
                        </div>
                    </div>
                    <div className="program">
                        <div className='programimg'>
                            <img src={CrashCourse} alt="" />
                        </div>
                        <div className='programtext'>
                            <h4>Crash-курс</h4>
                            <p>Crash-курс разработан для продвинутых барабанщиков, которые почувствовали технические или музыкальные препятствия в своей игре, хотели бы их преодолеть, и нуждаются в квалифицированном взгляде со стороны.</p>
                        </div>
                    </div>
                    <div className="program">
                        <div className='programimg'>
                            <img src={VipCourse} alt="" />
                        </div>
                        <div className='programtext'>
                            <h4>VIP-курс</h4>
                            <p>Набор множества курсов игры на барабанах с ориентациейна узкоспецифические моменты исполнения. Корректировка техники, развитие чувства времени, работа с метрономом, импровизационные моменты игры, глубокое изучение разных стилей, исполнение джазовых и латиноамериканскиx ритмов. </p>
                        </div>
                    </div>
                </div>
            </section>
            {/* <section className=''>
                <ReviewsCarousel />
            </section> */}
        </>
    );
}

export default SecondPage;