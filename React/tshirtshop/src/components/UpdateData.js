import React from 'react';
import UpdateAddress from './UpdateAddress';
import UpdateCreditCard from './UpdateCreditCard';
import UpdateGeneralData from './UpdateGeneralData';
import renuew from './helpers'
import { ClipLoader } from 'react-spinners';
import { css } from '@emotion/core';

const override = css`
    display: block;
    margin-left: 40%;
    border-color: red;
`;

export default class UpdateData extends React.Component {
    rel(){
        window.location.reload();
    }
    constructor(props) {
        super(props);
        
        this.state = {
          datas: null,
          loading: true,
          renuew: false,
        };
    }

    async componentDidMount() {
        const url = "http://40.113.199.165:3000/customer/";
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.access}`,
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json() ;
        this.setState({datas: data, loading: false })
        console.log(data.code);
        // eslint-disable-next-line no-unused-expressions
        if(localStorage.getItem('refresh')===null){
            window.location.replace("/login")
        }else if(response.status!==200 && data.code==="token_not_valid"){
            console.log("Bad Token")
            renuew()
            this.setState({
                renuew:!renuew,
            })
        }
        console.log(data);
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
      
        if (!this.state.datas) {
            return <ClipLoader 
            css={override}
            sizeUnit={"px"}
            size={100}
            color={'#123abc'}
            ></ClipLoader>;
        }
        
        console.log(this.state.datas.name);

        return(
            <div>
                <div>
                    <UpdateGeneralData customer={this.state.datas} />
                </div>
                <div>
                    <UpdateAddress customer={this.state.datas} />
                </div>
                <div>
                    <UpdateCreditCard customer={this.state.datas} />
                </div>
                <div align="center"><button align="center" className="bttn sm-button-pink" onClick={this.rel}>Finish</button></div>
            </div>
        );
    };
}