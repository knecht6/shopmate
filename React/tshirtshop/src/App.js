import React from 'react';
import './App.css';
import { BrowserRouter, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import Footer from './components/Footer';
import Home from './components/Home';
import Cart from './components/Cart';
import Signup from './components/Signup';
import Login from './components/Login';
import UpdateData from './components/UpdateData';
import ItemDetail from './components/ItemDetail';
import Notifications from 'react-notify-toast';
import Payment from './components/Payment';
import ShoppingSucess from './components/ShoppingSuccess';

class App extends React.Component {
  render() {
    return (
      
      <BrowserRouter>
        <div className="App">
        <div className='main'>
			<Notifications options={{zIndex: 200, top: '50px'}}/>
		    </div>
          <NavBar />
          <Route exact path="/" component={Home}></Route>
          <Route path="/login" component={Login}></Route>
          <Route path="/cart" component={Cart}></Route>
          <Route path="/signup" component={Signup}></Route>
          <Route path="/account" component={UpdateData}></Route>
          <Route path="/product/:id" component={ItemDetail}></Route>
          <Route path="/checkout" component={Payment}></Route>
          <Route path="/shopping_success" component={ShoppingSucess}></Route>
          <Footer />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
