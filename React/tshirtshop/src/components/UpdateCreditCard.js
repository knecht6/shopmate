import React from 'react';
import {notify} from 'react-notify-toast';

export default class UpdateCreditCard extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            credit_card: props.customer.credit_card,
        }
    }
    handleSubmit = (e) => {
        e.preventDefault();
        console.log("Inside the Button")
        let credit_card=document.getElementById("inputCreditCard").value;
        credit_card ? credit_card=credit_card: credit_card = document.getElementById("inputCreditCard").placeholder;
        fetch('http://40.113.199.165:3000/customer_update_credit_card/', {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.access}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "credit_card": credit_card,
            })
          }).then(resolve => {
            console.log(resolve.status);
            let myColor = { background: 'green', text: "white" };
            notify.show("Update Succesfully", "custom", 1000, myColor);
          } )
    };
    render() {
        return(
            <div className="container box-product-ws">
                <form onSubmit={this.handleSubmit} noValidate>
                    <h5>Credit Card</h5>
                    <div className="form-row">
                        <div className="form-group col-md-6">
                        <label for="inputCreditCard">Credit Card</label>
                        <input type="text" className="form-control" id="inputCreditCard" placeholder={this.state.credit_card} />
                        </div>
                    </div>
                    <button type="submit" className="bttn sm-button-pink">Update</button>
                </form>
            </div>
        );
    };
}