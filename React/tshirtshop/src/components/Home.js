import React from 'react';
import DepartmentList from './DepartmentList';
import ProductDetail from './ProductDetail';
import CategoryList from './CategoryList';

export default class Home extends React.Component {
    constructor(props) {
        super(props);
    
        this.state = {
          departments:[],
          products:[],
          categories:[],
          department:null,
        };
      }

    componentDidMount() {
        // const url = "https://api.randomuser.me/";
        // const response = await fetch(url);
        // const data = await response.json();
        // this.setState({ person: data.results[0], loading: false });

         const url = "http://40.113.199.165:3000/departments/";
         let initialDepartments = [];
         fetch(url).then(resolve => {
             return resolve.json();
         }).then(data=>{
             initialDepartments = data.map((department) => {
                 return department
             });
             console.log(initialDepartments);
             this.setState({
                 departments: initialDepartments,
             });
         });
         const url2 = "http://40.113.199.165:3000/products_on_catalog/?short_product_description_length=50&products_per_page=12&start_item=0";
         let initialProducts = [];
          fetch(url2).then(resolve => {
              return resolve.json();
          }).then(data=>{
              initialProducts = data.map((product) => {
                  return product
              });
              console.log(initialProducts);
              this.setState({
                  products: initialProducts,
              });
          });
          console.log(this.state.products);
      }

      handleSelectedDepartment = depto => {
          console.log("Selected")
          console.log(`Department id ${depto.department_id}`)
          const url = `http://40.113.199.165:3000/products_on_department/${depto.department_id}/?short_product_description_length=50&products_per_page=12&start_item=0`;
        let initialProducts = [];
         fetch(url).then(resolve => {
             return resolve.json();
         }).then(data=>{
             initialProducts = data.map((product) => {
                 return product
             });
             console.log(initialProducts);
             this.setState({
                 products: initialProducts,
             });
         });
         console.log(this.state.products);

         const url3 = `http://40.113.199.165:3000/categories_list/${depto.department_id}/`;
             let initialCategories = [];
             fetch(url3).then(resolve => {
                 return resolve.json();
             }).then(data=>{
                 initialCategories = data.map((category) => {
                     return category
                 });
                 console.log(initialCategories);
                 this.setState({
                     categories: initialCategories,
                 });
             });
             console.log(this.state.categories);
      }
      handleSelectedCategory = category => {
        console.log(`Selected category ${category.category_id}`)
        const url = `http://40.113.199.165:3000/products_in_category/${category.category_id}/?short_product_description_length=50&products_per_page=12&start_item=0`;
        let initialProducts = [];
         fetch(url).then(resolve => {
             return resolve.json();
         }).then(data=>{
             initialProducts = data.map((product) => {
                 return product
             });
             console.log(initialProducts);
             this.setState({
                 products: initialProducts,
             });
         });
         console.log(this.state.products);
    }

    search = (e) =>{
        e.preventDefault();
        console.log("Inside the Button")
        let search=document.getElementById("searchLabel").value;
        if(search){
            const url = `http://40.113.199.165:3000/catalog_search/?search_string=${search}&in_all_words=on&short_product_description_length=50&products_per_page=12&start_item=0`;
        let initialProducts = [];
         fetch(url).then(resolve => {
             return resolve.json();
         }).then(data=>{
             initialProducts = data.map((product) => {
                 return product
             });
             console.log(initialProducts);
             this.setState({
                 products: initialProducts,
             });
         });
         console.log(this.state.products);
        }
    }

    render () {
        return(
            <div className="container-fluid">
                <div className="row">
                    <div className="col-md-3">
                        <div className="list-group box-product-ws">
                            <form className="list-group-item" onSubmit={this.search}>
                                <div className="row">
                                    <div className="col-md-9">
                                        <input className="form-control" type="search" placeholder="Search" aria-label="Search" id="searchLabel"/>
                                    </div>
                                    <div className="col-md-2">
                                        <button className="bttn-ico" type="submit"><i className="fas fa-search"></i></button>
                                    </div>
                                </div>
                            </form>
                            <DepartmentList deptos={this.state.departments} onSelectedDepartment={this.handleSelectedDepartment}/><br /><br />
                            {this.state.categories.length>0?<CategoryList categoryes={this.state.categories} onSelectedCategory={this.handleSelectedCategory}></CategoryList>:<br />}
                        </div>
                        </div>
                        

                    <div className="col-md-9">
                        <ProductDetail products={this.state.products}/>
                    </div>
                </div>
            </div>
        );
    }
}