import './Carusel.scss'
import React from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

export default function SimpleSlider() {
  var settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,

  };
  return (
    
    <>
    <Slider {...settings}>
      <div className='divinslider' style='display:flex;'>
        <h3>2</h3>
        <p>года существует школа на рынке</p>
      </div>
      <div className='divinslider' style='display:flex;'>
        <h3>9 ИЗ 10</h3>
        <p>учеников после наших курсов продолжают играть на барабанах</p>
      </div>
      <div className='divinslider' style='display:flex;'>
        <h3>60+</h3>
        <p>довольных учеников,которые прошли обучение в нашей школе</p>
      </div>
    </Slider>
    </>
  );
}