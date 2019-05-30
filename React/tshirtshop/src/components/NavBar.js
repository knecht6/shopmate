import React from 'react';
import {notify} from 'react-notify-toast';

export default class NavBar extends React.Component {
    logout=()=>{
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        localStorage.removeItem('cart_id')
        notify.show("Success!", "custom", 1000, {background: 'green', text:"white"});
    }
    render(){

        const access = localStorage.getItem('access');
        return (
            <nav className="navbar navbar-expand-lg">
                <div className="container">
                    <a className="nav-link" href="/">SHOPMATE</a>
                    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                    </button>

                    <div className="container collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className="navbar-nav ml-lg-auto">
                            <li className="nav-item">
                                <a className="nav-link" href="/">Home</a>
                            </li>
                            {access ? 
                                <div className="navbar-nav">
                                    <li className="nav-item">
                                        <a className="nav-link" href="/cart">Cart</a>
                                    </li>
                                    <li className="nav-item">
                                        <a className="nav-link" href="/account">Account</a>
                                    </li>
                                    <li className="nav-item" onClick={this.logout}>
                                        <a className="nav-link" href="/">Log Out</a>
                                    </li>
                                </div> : 
                                <div className="navbar-nav">
                                    <li className="nav-item">
                                        <a className="nav-link" href="/login">Log In</a>
                                    </li>
                                    <li className="nav-item">
                                        <a className="nav-link" href="/signup">Sign Up</a>
                                    </li>
                                </div>
                            }
                        </ul>
                    </div>
                </div>
            </nav>
        );
    }
}