import React from 'react';
import Review from './Review';
import {notify} from 'react-notify-toast';

export default class UpdateGeneralData extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            itemId:props.itemId,
            reviews:[],
        }
    }

    componentDidMount() {
        const url = `http://40.113.199.165:3000/get_product_reviews/?product_id=${this.state.itemId}`;
        let initialReviews = [];
        fetch(url).then(resolve => {
            return resolve.json();
        }).then(data=>{
            initialReviews = data.map((review) => {
                return review
            });
            console.log(initialReviews);
            this.setState({
                reviews: initialReviews,
            });
        });
        
      }

    handleSubmit = (e) => {
        e.preventDefault();
        console.log("Inside the Button")
        console.log(document.getElementById("review").value)
        console.log(document.getElementById("rating").value)
        let review = document.getElementById("review").value;
        let rate = document.getElementById("rating").value;
        // eslint-disable-next-line no-unused-expressions
        review,rate ?
        fetch('http://40.113.199.165:3000/create_product_review/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.access}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "product_id": this.state.itemId,
                "review": review,
                "rating": rate
            })
        }).then(resolve => {
            console.log(resolve.status);
            let myColor = { background: 'green', text: "white" };
            notify.show("Review Sended", "custom", 15000, myColor);
            window.location.reload();
            
        }): notify.show("Empty", "custom", 1000, {background: 'red', text:"white"});
    };

    render() {
        console.log(this.state.itemId)
        return(
            <div>
                {this.state.reviews.length>0?<div className="container-fluid box-product-ns"><h3>Reviews</h3>
                {
                      this.state.reviews.map( review => 
                        (
                            <Review 
                                key={review.department_id} 
                                review={review}
                            >
                            </Review>))
                    } 
                </div>:<spa></spa>
                }
            <div className="container box-product-ws">
                <form onSubmit={this.handleSubmit} noValidate>
                    <h4>Send a Review</h4>
                    <div className="container row">
                        <div className="col-md-3">
                            <label for="inputName" className="review-form-label">Your Review</label>
                        </div>
                        <div className="col-md-8">
                            <textarea type="text" className="form-control" id="review" row="3" />
                        </div>
                    </div>
                    <div className="container row">
                        <div className="col-md-3">
                            <label for="inputPhone" className="review-form-label">Rating</label>
                        </div>
                        <div className="col-md-8">
                            <input type="number" min="0" max="100" className="form-control" id="rating"  />
                        </div>
                    </div>
                    <button className="bttn md-button-pink-large" type="submit">Submit</button>
                </form>
            </div></div>
        );
    }
}