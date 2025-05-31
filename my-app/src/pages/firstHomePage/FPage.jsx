import "./FPage.scss"
import FormforOrder from "../../components/Form"
import NumScrollDemo from "../../components/Carusel";
import { useState } from 'react';
import DrumFirstPic from '../../imgs/drumFirstPic.png'
import MaratPhoto from '../../imgs/MaratPhoto.png'
import MaratPhotoMobile from '../../imgs/MaratPhotoMobile.png'
import Disk from '../../imgs/disk.png'
import Avatar from '../../imgs/avatar.png'
import Avatars from '../../imgs/avatars.png'
import Star from '../../imgs/star.png'
import Var1 from '../../imgs/variant1.png'
import Var2 from '../../imgs/variant2.png'
import Var3 from '../../imgs/variant3.png'

function FirstHomePage() {
    return (
      <>
        <div>
        <section className="sectionsoffirstpage sec1">
          <h1><span>ПЕРВАЯ</span> БАРАБАННАЯ ШКОЛА В БИШКЕКЕ!</h1>
          {/* <button>
          <a href='#FormforOrder'>Стать барабанщиком</a>
          </button> */}
          <img className="drumFirstPic" src={DrumFirstPic} alt="" />
          <div className="Drums">DRUMS</div>
        </section>
        <div id="FormforOrder" className='mapandform'>
            <div className="map">
            </div >
            <FormforOrder />          
          </div>
        <section className="sectionsoffirstpage sec2">
          <div className="textOfSec2">
            <div className="text text1">
              <h2>DRUM <span>SCHOOL</span></h2>
              <img className="displayNone" src={MaratPhotoMobile} alt="" />
              <p>Привет! <span>Я Марат Миндубаев </span>- основатель и преподаватель школы барабанов Drumschool. В барабанном деле 16 лет и имею многолетний опыт как в студийных работах так и концертных. Работаю с такими группами как: Пишпек Сити, Икарус, The Woodstock tale, Jinks, Black Hate, Skifs.</p>
              <p>
                Работал с коллективами Ghost rider и E-note на студии High gain (г. Москва) в качестве сессионного барабанщика. Итак, добро пожаловать к нам, DrumSchool это: 
              </p>
            </div>
            <div className="text text2">
              <ul className="reciptList">
                <li className="recipt">Множество положительных отзывов</li>
                <li className="recipt">Профессиональные инструменты</li>
                <li className="recipt">Эффективная система обучения</li>
                <li className="recipt">Тусовка, общение, позитив</li>
                <li className="recipt">Оборудованные классы</li>
                <li className="recipt">Концерты и записи</li>
              </ul>
            </div>
            <img className="MaratPhoto" src={MaratPhoto} alt="" />
          </div>
        </section>
        <section className="sectionsoffirstpage sec3">
          <h2>ПОЧЕМУ ВЫБИРАЮТ <span>НАС</span></h2>
          <div className="whywe">
            <div className="whypoints">
              <div className="imagesforpoints">
                <img src={Disk} alt="" />
                <div className="whytext">
                  <h4>Базовые знания</h4>
                  <p>Вы научитесь нотной грамоте, правильной посадке за установкой, постановке рук и ног, базовым приемам игры.</p>
                </div>
              </div>
            </div>
            <div className="whypoints">
              <div className="imagesforpoints">
                <img src={Avatar} alt="" />
                <div className="whytext">
                  <h4>Индивидуальное обучение</h4>
                  <p>Забудьте про групповые занятия. У нас только индивидуальное обучение игре на барабанах с опытным преподавателем</p>
                </div>
              </div>
            </div>
            <div className="whypoints">
              <div className="imagesforpoints">
                <img src={Avatars} alt="" />
                <div className="whytext">
                  <h4>Интересно будет всем</h4>
                  <p>У нас богатый опыт обучения детей и взрослых, программа подстраивается под интересы и уровень каждого ученика.</p>
                </div>
              </div>
            </div>
            <div className="whypoints">
              <div className="imagesforpoints">
                <img src={Star} alt="" />
                <div className="whytext">
                  <h4>Разнообразие</h4>
                  <p>На занятиях Вы познакомитесь с разнообразными музыкальными стилями и научитесь играть любые барабанные партии</p>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section className="sectionsoffirstpage sec4">
          <div className="textof4sec">
            <h3>2</h3>
            <p>года существует школа на рынке</p>
          </div>
          <div className="textof4sec">
            <h3>9 ИЗ 10</h3>
            <p>учеников после наших курсов продолжают играть на барабанах</p>
          </div>
          <div className="textof4sec">
            <h3>60+</h3>
            <p>довольных учеников,которые прошли обучение в нашей школе</p>
          </div>
        </section>
        <section className="sectionsoffirstpage caruselllll">
          <NumScrollDemo className="carousellll"/>
        </section>  
        <section className="sectionsoffirstpage sec5 ">
          <h2 className="sertificate">ПОДАРОЧНЫЕ <span>СЕРТИФИКАТЫ</span></h2>
          <div className="sertVariants">
            <div className="variant">
              <img src={Var1} alt="" />
              <div className="varh1">
                <h4>ПОДАРОЧНЫЕ</h4><h4>Сертификаты на:</h4><h4> 4 / 8 / 12 занятий</h4>
              </div>
              <div className="varP">
                <p>Срок активации</p><p>сертификата -</p><p>3 месяца</p><p> со дня покупки</p>
              </div>
              </div>
            <div className="variant">
              <img src={Var2} alt="" />
              <div className="varh1">
                <h4>ПОДАРОЧНЫЙ</h4><h4>НАБОР +</h4><h4>4 / 8 / 12 ЗАНЯТИЙ</h4>
              </div>
              <div className="varP">
                <p>В набор входит:</p><p> Сертификат на</p><p> 4 / 8 / 12 занятий;</p><p> Барабанные палочки</p>
              </div>
              </div>
            <div className="variant">
              <img src={Var3} alt="" />

              <div className="varh1">
                <h4>ПОДАРОЧНЫЙ</h4><h4>НАБОР +</h4><h4>4 / 8 / 12 ЗАНЯТИЙ</h4>
              </div>
              <div className="varP">
                <p>В набор входит:</p><p>Сертификат на</p><p> 4 / 8 / 12 занятий;</p><p>Барабанные палочки;</p><p> Футболка DrumSchool</p>
              </div>
              </div>
          </div>
          <div className="googlemapdiv">
            <h2>где мы <span>находимся</span></h2>
            <iframe className="googleMap" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2925.6517789322197!2d74.62216837613406!3d42.83796897115239!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x389eb700ff74cd47%3A0x47c0e23a895c793a!2sDrum%20Courses!5e0!3m2!1sru!2skg!4v1744253091378!5m2!1sru!2skg" width="600" height="450" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
          </div>
          </section>
        </div>
      </>
    );
  }
  
  export default FirstHomePage;
  