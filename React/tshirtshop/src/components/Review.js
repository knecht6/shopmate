import React from 'react';


const Review = (props) => {
    console.log(props)
    const {name, review,rating} = props.review;
    return (
    <div className="container-fluid box-product-ws">
        <div className="row">
            <div className="col-md-1 user-ico">
                <i className="fas fa-user-circle"></i>
            </div>
            <div className="col-md-3">
                {/* <div className="rating">
                    <input type="radio" name="star" id="star1"/><i className="fas fa-star"></i>
                    <input type="radio" name="star" id="star2"/><i className="fas fa-star"></i>
                    <input type="radio" name="star" id="star3"/><i className="fas fa-star"></i>
                    <input type="radio" name="star" id="star4"/><i className="fas fa-star"></i>
                    <input type="radio" name="star" id="star5"/><i className="fas fa-star"></i>
                </div> */}
                <h4>{rating}</h4>
                <h5>{name}</h5>
            </div>
            <div className="col-md-6">
                <p> " {review} " </p>
            </div>
        </div>
    </div>
    )
};

export default Review;