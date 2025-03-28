import React, { useState } from 'react';
import axios from 'axios';
import './Form.scss'

function FormforOrder() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    phoneNumber: '',
    email: '',
    message: '',
  });

  const handleChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post(
        'http://192.168.43.61:8000/submit-application/',
        formData,
        {
          headers: {
            'Content-Type': 'application/json',
          }
        }
      );
      console.log(response.data);
      // Очистка формы после успешной отправки
      setFormData({
        firstName: '',
        lastName: '',
        phoneNumber: '',
        email: '',
        message: '',
      });
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className='Form'>
      <h2>СВЯЖИТЕСЬ <span>С НАМИ</span></h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            <input type="text" name="firstName" placeholder='Имя' value={formData.firstName} onChange={handleChange} required />
          </label>
        </div>
        <div>
          <label>
            <input type="text" name="lastName" placeholder='Фамилия' value={formData.lastName} onChange={handleChange} required />
          </label>
        </div>
        <div>
          <label>
            <input type="text" name="phoneNumber" placeholder='Телефон' value={formData.phoneNumber} onChange={handleChange} required />
          </label>
        </div>
        <div>
          <label>
            <input type="email" name="email" placeholder='E-mail' value={formData.email} onChange={handleChange} required />
          </label>
        </div>
        <div className="textarea">
          <label>
            <input type="text" name="message" placeholder='Ваше сообщение' value={formData.message} onChange={handleChange} required />
          </label>
        </div>
        <button className='submitbutton' type="submit">Записаться на пробный урок</button>
      </form>
    </div>
  );
}
export default FormforOrder;