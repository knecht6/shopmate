import React from 'react';
import {notify} from 'react-notify-toast';

const emailRegex = RegExp(
    /^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
  );
  
  const formValid = ({ formErrors, ...rest }) => {
    let valid = true;
  
    // validate form errors being empty
    Object.values(formErrors).forEach(val => {
      val.length > 0 && (valid = false);
    });
  
    // validate the form was filled out
    Object.values(rest).forEach(val => {
      val === null && (valid = false);
    });
  
    return valid;
  };

  export default class Signup extends React.Component {
    constructor(props) {
        super(props);
    
        this.state = {
          regions:[],
          firstName: null,
          email: null,
          password: null,
          formErrors: {
            firstName: "",
            email: "",
            password: ""
          }
        };
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
    
      handleSubmit = e => {
        e.preventDefault();
    
        if (formValid(this.state)) {
          console.log(`
            --SUBMITTING--
            First Name: ${this.state.firstName}
            Email: ${this.state.email}
            Password: ${this.state.password}
          `);

          fetch('http://40.113.199.165:3000/register_customer/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "name": this.state.firstName,
                "email": this.state.email,
                "password": this.state.password,
                "shipping_region_id": this.getSelected()
            })
          }).then(resolve => {
            console.log(resolve.status);
            if(resolve.status===201){
              notify.show("Success!", "custom", 1000, {background: 'green', text:"white"});
              return this.props.history.push("/login")
            }else{
              window.location.reload();
              notify.show("Something Went Wrong!", "custom", 1000, {background: 'red', text:"white"});
            }
          } )
        } else {
          console.error("FORM INVALID - DISPLAY ERROR MESSAGE");
        }
      };
    
      handleChange = e => {
        e.preventDefault();
        const { name, value } = e.target;
        let formErrors = { ...this.state.formErrors };
    
        switch (name) {
          case "firstName":
            formErrors.firstName =
              value.length < 3 ? "minimum 3 characaters required" : "";
            break;
          case "email":
            formErrors.email = emailRegex.test(value)
              ? ""
              : "invalid email address";
            break;
          case "password":
            formErrors.password =
              value.length < 6 ? "minimum 6 characaters required" : "";
            break;
          default:
            break;
        }
    
        this.setState({ formErrors, [name]: value }, () => console.log(this.state));
      };
    
      getSelected = () => {
        let selected = document.getElementById("regions_select").value;
        return selected;
      }
      render() {
        const { formErrors } = this.state;
    
        return (
          <div className="wrapper">
            <div className="box">
              <h1>Create Account</h1>
              <form className="log-form" onSubmit={this.handleSubmit} noValidate>
                <div className="firstName">
                  <label htmlFor="firstName">First Name</label>
                  <input
                    className={formErrors.firstName.length > 0 ? "error" : null}
                    placeholder="First Name"
                    type="text"
                    name="firstName"
                    noValidate
                    onChange={this.handleChange}
                  />
                  {formErrors.firstName.length > 0 && (
                    <span className="errorMessage">{formErrors.firstName}</span>
                  )}
                </div>
                <div className="email">
                  <label htmlFor="email">Email</label>
                  <input
                    className={formErrors.email.length > 0 ? "error" : null}
                    placeholder="Email"
                    type="email"
                    name="email"
                    noValidate
                    onChange={this.handleChange}
                  />
                  {formErrors.email.length > 0 && (
                    <span className="errorMessage">{formErrors.email}</span>
                  )}
                </div>
                <div className="password">
                  <label htmlFor="password">Password</label>
                  <input
                    className={formErrors.password.length > 0 ? "error" : null}
                    placeholder="Password"
                    type="password"
                    name="password"
                    noValidate
                    onChange={this.handleChange}
                  />
                  {formErrors.password.length > 0 && (
                    <span className="errorMessage">{formErrors.password}</span>
                  )}
                </div>
                <div className="regions">
                  <label htmlFor="Region">Region</label>
                  <select className="form-control" id="regions_select" onChange={this.getSelected}>
                    {
                      this.state.regions.map((region) =>
                      <option key={region.shipping_region} value={region.shipping_region_id}>{region.shipping_region}</option>)
                    } 
                    </select>
                    {console.log(this.refs.regions_id)}
                </div>
                <div className="createAccount">
                  <button className="bttn big-button-pink" type="submit">Create Account</button>
                  <small><a href="/login">Already Have an Account?</a></small>
                </div>
              </form>
            </div>
          </div>
        );
      }
  }