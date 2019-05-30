import React from 'react';

export default class Payment extends React.Component {
    constructor(props){
        super(props);

        this.state = {

        }
    }

    render() {
        return(
            <div>
                <form action="http:127.0.0.1:3000/checkout/" method="post">
                    <script src="https://checkout.stripe.com/checkout.js" class="stripe-button"
                            data-key="{{ key }}"
                            data-description="Tshirtshop Charge"
                            data-amount="{{ total_amount }}"
                            data-locale="auto"></script>
                    </form>
            </div>
        );
    };
}