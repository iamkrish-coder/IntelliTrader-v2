import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { Button, Card, Col, Nav, ProgressBar, Row } from "react-bootstrap";
import { toast } from 'sonner';

import {} from '../../api';
import { LoadingSpinner, BackgroundGradient, HeaderProfile, HeaderLogo, HeaderNav } from '../../components';
import { handleSuccess, handleError } from '../../utils';

const Overview = () => {

    const currentSkin = (localStorage.getItem('skin-mode')) ? 'dark' : '';
    const [skin, setSkin] = useState(currentSkin);
  
    const switchSkin = (skin) => {
      if (skin === 'dark') {
        const btnWhite = document.getElementsByClassName('btn-white');
  
        for (const btn of btnWhite) {
          btn.classList.add('btn-outline-primary');
          btn.classList.remove('btn-white');
        }
      } else {
        const btnOutlinePrimary = document.getElementsByClassName('btn-outline-primary');
  
        for (const btn of btnOutlinePrimary) {
          btn.classList.remove('btn-outline-primary');
          btn.classList.add('btn-white');
        }
      }
    };
  
    switchSkin(skin);
    useEffect(() => {
      switchSkin(skin);
    }, [skin]);

    return (
        <React.Fragment>
            <HeaderProfile onSkin={setSkin} />
        </React.Fragment>
    );
};

export default Overview;