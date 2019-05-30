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

  export default class Login extends React.Component {
    constructor(props) {
        super(props);
    
        this.state = {
          email: null,
          password: null,
          formErrors: {
            email: "",
            password: ""
          }
        };
      }
    
      handleSubmit = e => {
        e.preventDefault();
    
        if (formValid(this.state)) {
          console.log(`
            --SUBMITTING--
            Email: ${this.state.email}
            Password: ${this.state.password}
          `);

          fetch('http://40.113.199.165:3000/api/token/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "email": this.state.email,
                "password": this.state.password
            })
          }).then(resolve => {
            console.log(resolve.status);
              return resolve.json();
              
          }).then(data=>{
              window.location.replace("/");
              if(data.access!=null){
                console.log(data.status);
                localStorage.setItem('access', data.access);
                localStorage.setItem('refresh', data.refresh);
                localStorage.setItem('cart_id', "");
                console.log(localStorage.getItem('access'));
                console.log(data.status);
                let myColor = { background: 'green', text: "white" };
                notify.show("Success!", "custom", 1000, myColor);
                return this.props.history.push("/")
              }else{
                notify.show("Wrong Credentials!", "custom", 1000, {background: 'red', text:"Empty"});
                window.location.reload();
              }
          });
        } else {
          console.error("FORM INVALID - DISPLAY ERROR MESSAGE");
        }
        
      };
    
      handleChange = e => {
        e.preventDefault();
        const { name, value } = e.target;
        let formErrors = { ...this.state.formErrors };
    
        switch (name) {
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
    
      render() {
        const { formErrors } = this.state;
    
        return (
          <div className="wrapper">
            <div className="box">
              <h1>Log In</h1>
              <form className="log-form" onSubmit={this.handleSubmit} noValidate>
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
                <div className="createAccount">
                  <button className="bttn big-button-pink" type="submit">Log In</button>
                  
                </div>
              </form>
            </div>
          </div>
        );
      }
  }