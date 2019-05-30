import React from 'react';
import renuew from './helpers';
import { ClipLoader } from 'react-spinners';
import { css } from '@emotion/core';
import CartItem from './CartItem';
import ScriptTag from 'react-script-tag';


const override = css`
    display: block;
    margin-left: 40%;
    border-color: red;
`;

class Cart extends React.Component {

    constructor(props){
        super(props);

        this.state = {
            cart: null,
            loading: true,
            loading_shipping: true,
            input_id: null,
            amount: null,
            shipping_option: null,
            shipping:0,
            total:0,
            s_id: null,
            shippingId:1,
            customer_id: null,
        }
    }

    async componentDidMount() {
        const url_cart = `http://40.113.199.165:3000/shopping_cart_get_products/?cart_id=${localStorage.getItem('cart_id')}`;
        const response_cart = await fetch(url_cart, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.access}`,
                'Content-Type': 'application/json'
            }
        });
        const data_cart = await response_cart.json();
        this.setState({cart: data_cart, loading: false, total: data_cart.total_amount, customer_id: data_cart.customer_id});
        if(localStorage.getItem('refresh')===null){
            window.location.replace("/login")
        }else if(response_cart.status===401 && data_cart.code==="token_not_valid"){
            console.log("Bad Token")
            renuew()
            this.setState({
                renuew:!renuew,
            });  
        }
        console.log(data_cart);

        const url_shipping = `http://40.113.199.165:3000/get_shipping_options/`;
        const response_shipping = await fetch(url_shipping, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.access}`,
                'Content-Type': 'application/json'
            }
        });
        const data_shipping = await response_shipping.json();
        this.setState({shipping_option: data_shipping, loading_shipping: false, shipping: data_shipping[0].shipping_cost,shippingId:data_shipping[0].shipping_id, total:(parseFloat(this.state.cart.total_amount) + parseFloat(data_shipping[0].shipping_cost)).toFixed(2)});
        console.log(this.state.shipping_option);
        if(localStorage.getItem('refresh')===null){
            window.location.replace("/login")
        }else if(response_cart.status===401 && data_cart.code==="token_not_valid"){
            console.log("Bad Token")
            renuew()
            this.setState({
                renuew:!renuew,
            });  
        }
    }

    getSelected = () => {
        let selected = document.getElementById("shipping_select").value;
        let res = selected.split("-");
        console.log(res[0]);
        console.log(res[1]);
        console.log(selected)
        this.setState({
            shippingId: res[1],
            shipping: res[0],
            total: (parseFloat(this.state.cart.total_amount) + parseFloat(res[0])).toFixed(2)
        });        
      }

    render() {

        if (this.state.loading) {
            return <ClipLoader 
            css={override}
            sizeUnit={"px"}
            size={100}
            color={'#123abc'}
            ></ClipLoader>;
        }
        if (!this.state.cart) {
            return <ClipLoader 
            css={override}
            sizeUnit={"px"}
            size={100}
            color={'#123abc'}
            ></ClipLoader>;
        }

        if (this.state.loading_shipping) {
            return <ClipLoader 
            css={override}
            sizeUnit={"px"}
            size={100}
            color={'#123abc'}
            ></ClipLoader>;
        }
        if (!this.state.shipping_option) {
            return <ClipLoader 
            css={override}
            sizeUnit={"px"}
            size={100}
            color={'#123abc'}
            ></ClipLoader>;
        }

        let total= `http://40.113.199.165:3000/checkout/?total_amount=${this.state.total}&cart_id=${localStorage.getItem('cart_id')}&shipping_id=${this.state.shippingId}&customer_id=${this.state.customer_id}`
        console.log(total)
        return(
            <div className="container box-product-ns">
                <div className="row">
                    <div className="col-2">
                        <label>Product</label>
                    </div>
                    <div className="col-2">
                        <label>Size, Color</label>
                    </div>
                    <div className="col-2">
                        <label>Price</label>
                    </div>
                    <div className="col-2">
                        <label>Quantity</label>
                    </div>
                    <div className="col-2">
                        <label>Subtotal</label>
                    </div>
                    <div className="col-2">
                        <label>Actions</label>
                    </div>
                </div>
                {console.log(this.state.cart.products)}
                
                {localStorage.refresh? localStorage.cart_id!==""&&localStorage.access? this.state.cart.products.map((product) => (
                    <CartItem product={product} product_quantity={this.state.cart.products.length}/>
                )):<spam></spam>:<spam></spam>}
                {localStorage.cart_id!==""?
                <div className="row row_extra">
                    <div className="col-md-6">
                    <div className="regions">
                        <label htmlFor="Shipping">Shipping option</label>
                        <select className="form-control" id="shipping_select" onChange={this.getSelected}>
                            {
                            this.state.shipping_option.map((option)=>
                            
                                <option key={option.shipping_id} value={`${option.shipping_cost}-${option.shipping_id}`}>{option.shipping_type}</option>
                                
                            
                            )
                            } 
                            </select>

                        </div>
                    </div>
                    <div className="col-md-6">
                        <div className="cart_total">
                            <div className="section_title">Cart Total</div>
                            <div className="section_subtitle">Final Info</div>
                            <div className="cart_total_container">
                                <ul>
                                    <li className="d-flex flex-row align-items-center justify-content-start">
                                        <div className="cart_total_title">Subtotal</div>
                                        <div className="cart_total_value ml-auto">$ {this.state.cart.total_amount}</div>
                                    </li>
                                    <li className="d-flex flex-row align-items-center justify-content-start">
                                        <div className="cart_total_title">Shipping</div>
                                        <div className="cart_total_value ml-auto">$ {this.state.shipping}.00</div>
                                    </li>
                                    <li className="d-flex flex-row align-items-center justify-content-start">
                                        <div className="cart_total_title">Total</div>
                                        <div className="cart_total_value ml-auto">$ {this.state.total}</div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>:<span></span>}

                <div className="row">
                    <div className="col">
                        <div className="d-flex flex-lg-row flex-column align-items-center justify-content-center">
                            <div className="bttn md-button-pink-large">
                                <a href="/">Continue Shopping</a>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="row">
                    <div className="col">
                        <div className="d-flex flex-lg-row flex-column align-items-center justify-content-center">
                            {localStorage.cart_id!==""?
                            <form action={total} method="post">
                                    {/* <input type="text" name="extraParam2" value={this.state.cart.customer_id}></input> */}
                                    <ScriptTag src="https://checkout.stripe.com/checkout.js" 
                                        className="stripe-button"
                                        data-key={this.state.cart.key}
                                        data-description="Tshirtshop Charge"
                                        data-locale="auto"/>
                            
                            </form>:<span></span>}
                        </div>
                    </div>
                </div>

            </div>
        );
    }
}



export default Cart;