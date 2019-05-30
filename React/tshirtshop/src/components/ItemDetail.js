import React from 'react';
import renuew from './helpers';
import ProductReview from './ProductReview'
import { ClipLoader } from 'react-spinners';
import { css } from '@emotion/core';
import {notify} from 'react-notify-toast';

const override = css`
    display: block;
    margin-left: 40%;
    border-color: red;
`;

export default class ItemDetail extends React.Component {
    constructor(props){
        super(props);

        const {match:{params}} = props;
        this.state = {
            loading_product: true,
            loading_size: true,
            loading_color: true,
            colors: [],
            color: "",
            sizes: [],
            size: "",
            product: null,
            itemId: params.id,
            cart_id: "",
        }
    }

    async componentDidMount() {
        const url_product = `http://40.113.199.165:3000/product/${this.state.itemId}/`;
        const response_product = await fetch(url_product);
        const data_product = await response_product.json();
        this.setState({product: data_product, loading_product: false });
        console.log(data_product);

        const url_sizes = "http://40.113.199.165:3000/attribute_values/1";
        const response_sizes = await fetch(url_sizes, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.access}`,
                'Content-Type': 'application/json'
            }
        });
        const data_sizes = await response_sizes.json();
        this.setState({sizes: data_sizes, loading_size: false });
        if(localStorage.getItem('refresh')===null){
            window.location.replace("/login")
        }else if(response_sizes.status!==200 && data_sizes.code==="token_not_valid"){
            console.log("Bad Token")
            renuew()
            this.setState({
                renuew:!renuew,
            });  
        }
        console.log(data_sizes);

        const url_colors = "http://40.113.199.165:3000/attribute_values/2";
        const response_colors = await fetch(url_colors, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.access}`,
                'Content-Type': 'application/json'
            }
        });
        const data_colors = await response_colors.json();
        this.setState({colors: data_colors, loading_color: false });
        if(response_colors.status!==200 && data_colors.code==="token_not_valid"){
            console.log("Bad Token")
            renuew()
            this.setState({
                renuew:!renuew,
            });  
        }
        console.log(data_colors);
    }

    handleSubmit = (e) => {
        e.preventDefault();
            console.log(`
                --SUBMITTING--
                cart_id: ${localStorage.cart_id}
                product_id: ${this.state.itemId}
                attributes: ${this.state.size}, ${this.state.color}
            `);
            const url_add_cart = "http://40.113.199.165:3000/shopping_cart_add_product/";
            fetch(url_add_cart, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.access}`,
                    //'Accept': 'application/json',
                    'Content-Type': 'application/json',
                }, 
                body: JSON.stringify({
                    "cart_id": `${localStorage.cart_id}`,
                    "product_id": this.state.itemId,
                    "attributes": `${this.state.size}, ${this.state.color}`,
                })
            }).then(resolve => {
                console.log(resolve.status);
                let myColor = { background: 'green', text: "white" };
                notify.show("Item Added", "custom", 1000, myColor);
                if(localStorage.getItem('cart_id')===""){return resolve.json();}
              }).then(data=>{
                  if(localStorage.getItem('cart_id')===""){
                    console.log(data[0].cart_id);
                    localStorage.setItem('cart_id', data[0].cart_id);
                  }
                
            });
    };

    onColorChanged = (e) => {
        this.setState({
          color: e.currentTarget.value
          });
    }
    
    onSizeChanged = (e) => {
        this.setState({
          size: e.currentTarget.value
          });
    }

    render() {
        const img_container = document.getElementById("image-container");
        // change_img(image) {
        //     console.log(image);
        //     img_container.src = image.src;
        // }

        if (this.state.loading_product) {
            return <ClipLoader 
            css={override}
            sizeUnit={"px"}
            size={100}
            color={'#123abc'}
            ></ClipLoader>;
        }
        if (this.state.loading_size) {
            return <ClipLoader 
            css={override}
            sizeUnit={"px"}
            size={100}
            color={'#123abc'}
            ></ClipLoader>;
        }
        if (this.state.loading_color) {
            return <ClipLoader 
            css={override}
            sizeUnit={"px"}
            size={100}
            color={'#123abc'}
            ></ClipLoader>;
        }
      
        if (!this.state.product) {
            return <ClipLoader 
            css={override}
            sizeUnit={"px"}
            size={100}
            color={'#123abc'}
            ></ClipLoader>;
        }
        if (!this.state.sizes.length) {
            return <ClipLoader 
            css={override}
            sizeUnit={"px"}
            size={100}
            color={'#123abc'}
            ></ClipLoader>;
        }
        if (!this.state.colors.length) {
            return <ClipLoader 
            css={override}
            sizeUnit={"px"}
            size={100}
            color={'#123abc'}
            ></ClipLoader>;
        }
    

        return(
            <div className="container box-product-ws"><div>
                <form onSubmit={this.handleSubmit} noValidate>
                    <div className="row">
                        <div className="col-md-6">
                            <div className="box-product-ns">
                                <div className="product-display">
                                    <img src={`http://40.113.199.165:3000/media/product_images/${this.state.product.image}`} id="image-container" />
                                </div>
                                <div className="product-nav">
                                    <img src={`http://40.113.199.165:3000/media/product_images/${this.state.product.image}`} />
                                    <img src={`http://40.113.199.165:3000/media/product_images/${this.state.product.image_2}`} />
                                </div>
                            </div>
                        </div>
                        <div className="col-md-6 col-lg-6">
                            <h2>{this.state.product.name}</h2>
                            <h3 className="price-discount">$ {this.state.product.discounted_price > 0 ? this.state.product.discounted_price : this.state.product.price}</h3>
                            {/* <p className="price">$ {this.state.product.price}</p> */}
                            <fieldset className="d-inline" id="size_select">
                                <label>Size: </label>
                                {this.state.sizes.map(size => (
                                    <label className="size-button"><input type="radio" name="size" value={size.value} checked={this.state.size === size.value} onChange={this.onSizeChanged}/>{size.value}</label>
                                ))}
                            </fieldset>
                            <fieldset className="d-inline" id="color_select" onChange={this.getSelectedColor}>
                                <label>Color: </label>
                                {this.state.colors.map(color => (
                                    <label className="size-button"><input type="radio" name="color" value={color.value} checked={this.state.color === color.value} onChange={this.onColorChanged}/>{color.value}</label>
                                ))}
                            </fieldset>
                            <div>
                                <button className="bttn big-button-pink" type="submit">Add to Cart</button>
                            </div>
                        </div>
                    </div>
                </form>
                </div><br /><br />
                <div>
                <ProductReview itemId={this.state.itemId}/></div>
            </div>
        );
    };
    
}