import React from 'react';
import {notify} from 'react-notify-toast';

export default class UpdateGeneralData extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: props.customer.name,
            day_phone: props.customer.day_phone,
            eve_phone: props.customer.eve_phone,
            mob_phone: props.customer.mob_phone,
        }
    }

    handleSubmit = (e) => {
        e.preventDefault();
        console.log("Inside the Button")
        console.log(document.getElementById("inputName").placeholder)
        console.log(document.getElementById("inputPhone").value)
        let name = document.getElementById("inputName").value;
        name ? name=name: name=document.getElementById("inputName").placeholder;
        let day_phone = document.getElementById("inputPhone").value;
        day_phone ? day_phone=day_phone: day_phone=document.getElementById("inputPhone").placeholder;
        let eve_phone = document.getElementById("inputPhone2").value;
        eve_phone ? eve_phone=eve_phone: eve_phone=document.getElementById("inputPhone2").placeholder;
        let mob_phone = document.getElementById("inputPhone3").value;
        mob_phone ? mob_phone=mob_phone: mob_phone=document.getElementById("inputPhone3").placeholder
        
        console.log(this.state.name)
        fetch('http://40.113.199.165:3000/customer/', {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.access}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "name": name,
                "day_phone": day_phone,
                "eve_phone": eve_phone,
                "mob_phone": mob_phone
            })
        }).then(resolve => {
            console.log(resolve.status);
            let myColor = { background: 'green', text: "white" };
            notify.show("Update Succesfully", "custom", 1000, myColor);
        })
    };

    render() {
        
        return(
            <div className="container box-product-ws">
                <form onSubmit={this.handleSubmit} noValidate>
                    <h5>General</h5>
                    <div className="form-row">
                     <div className="form-group col-md-3">
                        <label for="inputName">Name</label>
                        <input type="text" className="form-control" id="inputName" placeholder={this.props.customer.name} />
                        </div>
                        <div className="form-group col-md-3">
                        <label for="inputPhone">Office Phone</label>
                        <input type="text" className="form-control" id="inputPhone" placeholder={this.props.customer.day_phone} />
                        </div>
                        <div className="form-group col-md-3">
                        <label for="inputPhone2">Home Phone</label>
                        <input type="text" className="form-control" id="inputPhone2" placeholder={this.props.customer.eve_phone}/>
                        </div>
                        <div className="form-group col-md-3">
                        <label for="inputPhone3">Mobile Phone</label>
                        <input type="text" className="form-control" id="inputPhone3" placeholder={this.props.customer.mob_phone}/>
                        </div>
                    </div>
                    <button className="bttn sm-button-pink" type="submit">Update</button>
                </form>
            </div>
        );
    }
}