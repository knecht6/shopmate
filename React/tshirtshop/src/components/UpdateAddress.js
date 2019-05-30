import React from 'react';
import {notify} from 'react-notify-toast';

export default class UpdateAddress extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            regions:[],
            region: props.customer.region,
            shipping_region_id: props.customer.shipping_region_id,
            address_1: props.customer.address_1,
            address_2: props.customer.address_2,
            city: props.customer.city,
            postal_code: props.customer.postal_code,
            country: props.customer.country,
        }
    }
    componentDidMount() {
        const url = "http://40.113.199.165:3000/register_customer/";
        let initialRegions = [];
        fetch(url).then(resolve => {
            return resolve.json();
        }).then(data=>{
            initialRegions = data.map((region) => {
                return region
            });
            console.log(initialRegions);
            this.setState({
                regions: initialRegions,
            });
        });
        
      }

      getSelected = () => {
        let selected = document.getElementById("regions_select").value;
        return selected;
      }

    handleSubmit = (e) =>{
        e.preventDefault();
        console.log("Inside the Button")
        let region = document.getElementById("inputRegion").value;
        region ? region=region: region=document.getElementById("inputRegion").placeholder;
        let shipping_region_id= this.getSelected();
        let address_1 = document.getElementById("inputAddress").value;
        address_1 ? address_1 = address_1: address_1=document.getElementById("inputAddress").placeholder;
        let address_2 = document.getElementById("inputAddress2").value;
        address_2 ? address_2=address_2: address_2 = document.getElementById("inputAddress2").placeholder;
        let city = document.getElementById("inputCity").value;
        city ? city = city: city = document.getElementById("inputCity").placeholder;
        let postal_code = document.getElementById("inputPostalCode").value;
        postal_code ? postal_code=postal_code: postal_code=document.getElementById("inputPostalCode").placeholder;
        let country = document.getElementById("inputCountry").value;
        country ? country=country: country=document.getElementById("inputCountry").placeholder;
        console.log(region)
        console.log(address_1)
        console.log(address_2)
        console.log(city)
        console.log(postal_code)
        console.log(country)

        fetch('http://40.113.199.165:3000/customer_update_address/', {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.access}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "region": region,
                "shipping_region_id": shipping_region_id,
                "address_1": address_1,
                "address_2": address_2,
                "city": city,
                "postal_code": postal_code,
                "country": country,
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
                    <h5>Address</h5>
                    <div className="form-row">
                        <div className="form-group col-md-6 regions">
                            <label htmlFor="Region">Region</label>
                            <input type="text" className="form-control" id="inputRegion" placeholder={this.state.region}/>
                        </div>
                        <div className="form-group col-md-6">
                        <label for="inputRegion2">Shipping Region</label>
                        
                        <select className="form-control" id="regions_select" onChange={this.getSelected}>
                    {
                      this.state.regions.map((region) =>
                      <option key={region.shipping_region} value={region.shipping_region_id} selected={region.shipping_region_id===this.state.shipping_region_id?region.shipping_region_id:""}>{region.shipping_region}</option>)
                    } 
                    </select>

                        </div>
                    </div>
                    <div className="form-row">
                        <div className="form-group col-md-6">
                        <label htmlFor="inputAddress">Address</label>
                        <input type="text" className="form-control" id="inputAddress" placeholder={this.state.address_1}/>
                        </div>
                        <div className="form-group col-md-6">
                        <label for="inputAddress2">Address 2</label>
                        <input type="text" className="form-control" id="inputAddress2" placeholder={this.state.address_2} />
                        </div>
                    </div>
                    <div className="form-row">
                        <div className="form-group col-md-4">
                        <label for="inputCity">City</label>
                        <input type="text" className="form-control" id="inputCity" placeholder={this.state.city} />
                        </div>
                        <div className="form-group col-md-4">
                        <label for="inputCountry">Country</label>
                        <input type="text" className="form-control" id="inputCountry" placeholder={this.state.country}/>
                        </div>
                        <div className="form-group col-md-4">
                        <label for="inputPostalCode">Postal Code</label>
                        <input type="text" className="form-control" id="inputPostalCode" placeholder={this.state.postal_code}/>
                        </div>
                    </div>
                    <button type="submit" className="bttn sm-button-pink">Update</button>
                </form>
            </div>
        );
    };
}