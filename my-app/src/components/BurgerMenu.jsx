import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import "./BurgerMenu.scss"; // Подключаем SCSS стили

const BurgerMenu = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const { isAuthenticated, user } = useAuth();

    // Обработчик клика по бургеру
    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    // Закрытие меню при клике на ссылку
    const closeMenu = () => {
        setIsMenuOpen(false);
    };

    return (
        <>
            <div 
                className={`burger ${isMenuOpen ? "active" : ""}`} 
                onClick={toggleMenu} 
                aria-label="Меню"
            >
                <span></span>
                <span></span>
                <span></span>
            </div>
            <ul className={`menu ${isMenuOpen ? "active" : ""}`}>
                <li><a href="/home" onClick={closeMenu}>О школе</a></li>
                <li><a href="/study" onClick={closeMenu}>Обучение</a></li>
                <li><a href="/teachers" onClick={closeMenu}>Педагоги</a></li>
                <li><a href="/blog" onClick={closeMenu}>События</a></li>
                <li><a href="/drum.music.stuf" onClick={closeMenu}>Интернет-Магазин DRUMROOM</a></li>
                {isAuthenticated ? (
                    <li><a href="/cabinet" onClick={closeMenu}>{user?.first_name || 'Кабинет'}</a></li>
                ) : (
                    <li><a href="/login" onClick={closeMenu}>Войти</a></li>
                )}
            </ul>
        </>
    );
};

export default BurgerMenu;