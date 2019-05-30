import React from 'react';
import { Link } from 'react-router-dom';
import { ClipLoader } from 'react-spinners';
import { css } from '@emotion/core';

const override = css`
    display: block;
    margin-left: 40%;
    border-color: red;
`;

const ProductDetail = ({products}) => {
        if (!products.length) {
          return <ClipLoader 
            css={override}
            sizeUnit={"px"}
            size={100}
            color={'#123abc'}
            ></ClipLoader>;
        }
          return(
            <div className="row">
              {products.map(product => (
                <div className="col-md-3 box-product" key={product.product_id}>
                  <img src={`http://40.113.199.165:3000/media/product_images/${product.thumbnail}`} />
                  <h4>{product.name}</h4>
                  <h4 className="price-discount">$ { product.discounted_price > 0 ? product.discounted_price : product.price }</h4>
                  <a className="bttn md-button-pink"><Link to={`/product/${product.product_id}`}>See Product</Link></a>
                </div>
              ))}
            </div>
          );
}
export default ProductDetail;