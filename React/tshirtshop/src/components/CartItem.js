import React from 'react';
import {notify} from 'react-notify-toast';

class CartItem extends React.Component {
    constructor(props){
        super(props);

        this.state = {
            item_id: props.product.item_id,
            name: props.product.name,
            price: props.product.price,
            quantity: props.product.quantity,
            subtotal: props.product.subtotal,
            attributes: props.product.attributes,
            product_quantity: props.product_quantity
        }
    }

    onChange(e) {
        console.log("Inside Delete")
        console.log(`It's going to be deleted ${e}`)
        const url_add_cart = "http://40.113.199.165:3000/shopping_cart_remove_product/";
        fetch(url_add_cart, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.access}`,
                'Content-Type': 'application/json',
            }, 
            body: JSON.stringify({
                "item_id": e,
            })
        }).then(resolve => {
            console.log(resolve.status);
            if(this.state.product_quantity!==1){
                window.location.reload()
            }else{
                localStorage.setItem('cart_id',"")
                window.location.replace("/");
            }
            });
    }

    handleSubmit = (e) => {
        e.preventDefault();
        console.log("Inside the Button")
        console.log(document.getElementById(`number_${this.state.item_id}`).value)
        let quantity=document.getElementById(`number_${this.state.item_id}`).value
        fetch('http://40.113.199.165:3000/shopping_cart_update/', {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.access}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "item_id": this.state.item_id,
                "quantity": quantity
            })
          }).then(resolve => {
            console.log(resolve.status);
            this.setState({
                quantity:quantity,
            })
            let myColor = { background: 'green', text: "white" };
            window.location.reload()
            notify.show("Update Succesfully", "custom", 1000, myColor);
          } )
    }

    render() {
        {console.log(this.state.item_id)}
        {console.log(this.state.quantity)}
        {console.log(this.state.product_quantity)}
        const id=`number_${this.state.item_id}`
        return(
                 <form onSubmit={this.handleSubmit}><div className="row">
                        <div className="col-2 product-title-sm">
                            <h4>{this.state.name}</h4>
                        </div>
                        <div className="col-2">
                            <p>{this.state.attributes}</p>
                        </div>
                        <div className="col-2">
                            <p>$ {this.state.price}</p>
                        </div>
                        <div className="col-2">
                            <input type="number" min="1" id={id} placeholder={this.state.quantity}></input>
                        </div>
                        <div className="col-2">
                            <h4>$ {this.state.subtotal}</h4>
                        </div>
                        <div className="col-2">
                            <button className="bttn-ico" type="submit"><i className="fas fa-pen-square"></i></button>
                            <button className="bttn-ico" onClick={()=>this.onChange(this.state.item_id)}><i className="fas fa-trash"></i></button>
                        </div>
                    </div></form>
        );
    }
}

export default CartItem;