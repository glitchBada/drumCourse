import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPhone, faBars } from '@fortawesome/free-solid-svg-icons';
import {faWhatsapp, faInstagram} from '@fortawesome/free-brands-svg-icons'
import './CircularMenu.scss';

const FloatingMenu = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="floating-menu">
      <div className={`menu-items ${isOpen ? 'open' : ''}`}>
        <a
          href="https://wa.me/996550172225"
          className="menu-item whatsapp"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FontAwesomeIcon icon={faWhatsapp} />
        </a>
        <a
          href="https://www.instagram.com/drumcourses.bishkek?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
          className="menu-item instagram"
          target="_blank"
          rel="noopener noreferrer"

        >
          <FontAwesomeIcon icon={faInstagram} />
        </a>
        <a href="tel:+996550172225" className="menu-item phonen">
          <FontAwesomeIcon icon={faPhone} />
        </a>
      </div>
      <button className="menu-toggle" onClick={toggleMenu}>
        <div className="drum-ring">
          <FontAwesomeIcon icon={faBars} className="menu-icon" />
        </div>
      </button>
    </div>
  );
};

export default FloatingMenu;
