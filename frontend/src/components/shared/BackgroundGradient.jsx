// components/BackgroundGradient.jsx
import React, { useEffect, useState } from 'react';
import IMAGES from '../../constants/images.js';
import { Container } from 'react-bootstrap';

const BackgroundGradient = () => {
    const [gradientImage, setGradientImage] = useState(null);
    const getRandomGradientImage = () => {
        const gradients = Array.from({length: 18}, (_, i) => IMAGES[`Gradient${i + 1}`]);
        return gradients[Math.floor(Math.random() * gradients.length)];
    };

    useEffect(() => { 
        setGradientImage(getRandomGradientImage());
    }, []); 

    return (
        <Container className="background-image blur" style={{ backgroundImage: `url(${gradientImage})` }}>
        </Container>
    );
};

export default BackgroundGradient;
