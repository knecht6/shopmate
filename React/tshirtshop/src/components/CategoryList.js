import React from 'react';
import Category from './Category';

const CategoryList = ({categoryes, onSelectedCategory}) => {

    const handleCategoryClick = category =>{
        console.log("handleCategoryClick");
        onSelectedCategory(category);
    };

    const strToComponent = categoryes => {
        return categoryes.map( category => 
            (
                <Category
                    key={category.category_id} 
                    cate={category.name}
                    onCategoryClick={()=>handleCategoryClick(category)}>
                </Category>));
    };
    return (
        <div className="container-fluid list-group-item">
            <h3>Categories</h3>
            {
                strToComponent(categoryes)
            }
        </div>
    );
};

export default CategoryList;