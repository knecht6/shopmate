import React from 'react';

export default function Footer(props) {
    return (
        <footer className="container py-5">
          <div className="row">
            <div className="col-12 col-md product-title-sm">
              <h4>SHOPMATE</h4>
              <small className="d-block mb-3 text-muted">&copy; 2019</small>
            </div>
            <div className="col-6 col-md">
              <h5>Home</h5>
              <ul className="list-unstyled text-small">
                <li><a className="text-muted" href="/">Home</a></li>
              </ul>
            </div>
            <div className="col-6 col-md">
              <h5>Department</h5>
              <ul className="list-unstyled text-small">
                <li><a className="text-muted" href="#">Regional</a></li>
                <li><a className="text-muted" href="#">Nature</a></li>
                <li><a className="text-muted" href="#">Seasonal</a></li>
              </ul>
            </div>
            <div className="col-6 col-md">
              <h5>Users</h5>
              <ul className="list-unstyled text-small">
                <li><a className="text-muted" href="/login">Log In</a></li>
                <li><a className="text-muted" href="/signup">Sign Up</a></li>
                <li><a className="text-muted" href="/account">Account</a></li>
              </ul>
            </div>
            <div className="col-6 col-md">
              <h5>Cart</h5>
              <ul className="list-unstyled text-small">
                <li><a className="text-muted" href="/cart">My Cart</a></li>
              </ul>
            </div>
          </div>
        </footer>
    );
}