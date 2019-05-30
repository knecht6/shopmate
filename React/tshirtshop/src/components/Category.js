import React from 'react';


const Category = (props) => {
    const {cate} = props;
    const {onCategoryClick} = props;
    return (
    <div className="locationCont" onClick={onCategoryClick}>
        <button className="bttn list-group-bttn">{cate}</button>
    </div>
    )
};

export default Category;