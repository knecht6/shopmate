import React from 'react';


export default class ShoppingSucess extends React.Component {
    
    componentDidMount() {
        localStorage.setItem('cart_id',"")
      }
    
    render(){
        return (
            <div className="container box-product-ws">
                <h1>Thank's for your purchase!</h1>
                <div>
                    <img src="http://www.sclance.com/pngs/success-png/success_png_1327906.png" />
                </div>
                <button className="bttn md-button-pink-large"><a href="/">Go Back</a></button>
            </div>
        );
    }
}