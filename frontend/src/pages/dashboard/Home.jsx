import React from 'react';
import { useNavigate } from 'react-router-dom'
import { Image, Button, Container } from 'react-bootstrap';

const Home = ({ assets }) => {
    const navigate = useNavigate()
    const { IMAGES, SVG, ICONS, MESSAGES } = assets;

    return (
        <React.Fragment>
            <div className="home-page">
                <div id="wrapper">
                    <header id="banner" className="scrollto clearfix" data-enllax-ratio=".5">
                        <div id="banner-content" className="row clearfix">
                            <div className="col-38">
                                <div className="section-heading">
                                    <h1>IntelliTrader</h1>
                                    <h2>IntelliTrader is an advanced algorithmic trading platform designed for personal use, enabling users to automate and enhance their trading strategies. Built with cutting-edge technologies like Python, FastAPI, React, Sass, Tailwind CSS, and AWS Cloud.</h2>
                                </div>
                                <Button variant='outline-dark' onClick={() => navigate('/login')}>Get Started</Button>

                            </div>
                        </div>
                    </header>

                    <footer id="landing-footer" className="clearfix">
                        <div className="row clearfix">

                        </div>
                    </footer>
                </div>
            </div>
        </React.Fragment>
    )
}

export default Home;