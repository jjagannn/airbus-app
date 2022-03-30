import './App.css';
import React, {useState, useEffect} from 'react';
import "bootstrap/dist/css/bootstrap.min.css";
import {Routes, Route, Link} from "react-router-dom";
import AuthService from "./services/auth.service";
import Login from "./components/Login";
import Register from "./components/Register";
import Profile from "./components/Profile";
import Home from "./components/Home";
import BoardUser from "./components/BoardUser";
import EventBus from "./common/EventBus";

const App = () => {
  const [currentUser, setCurrentUser] = useState(undefined);
  useEffect(() => {
    const user = AuthService.getCurrentUser();
    if (user) {
      setCurrentUser(user);
    }
    EventBus.on("logout", () => {
      logout();
    });
    return () => {
      EventBus.remove("logout");
    };
  }, []);

  const logout = () => {
    AuthService.logout();
    setCurrentUser(undefined);
  };

  return (
    <div>
      <nav className='navbar navbar-expand navbar-dark bg-dark'>
        <Link to={"/"} className='navbar-brand'>Airbus</Link>
        <div className='navbar-nav mr-auto'>
          <li className='nav-item'>
            <Link to={"/home"} className='nav-link'>
              Home
            </Link>
          </li>
          {currentUser && (
            <li className='nav-item'>
              <Link to={"/user"} className='nav-link'>
                User
              </Link>
            </li>
          )}
        </div>
        { currentUser ? (
          <div className='navbar-nav ml-auto'>
            <li className='nav-item'>
              <Link to={"/profile"} className='nav-link'>
                {currentUser.username}
              </Link>
            </li>
            <li className='nav-item'>
              <a href='/login' className='nav-link' onClick={logout}>Logout</a>
            </li>
          </div>
        ) : (
          <div className="navbar-nav ml-auto">
            <li className="nav-item">
              <Link to={"/login"} className="nav-link">
                Login
              </Link>
            </li>
            <li className="nav-item">
              <Link to={"/register"} className="nav-link">
                Sign Up
              </Link>
            </li>
          </div>
        )}
      </nav>
      <div className='container mt-3'>
        <Routes>
          <Route exact path={"/"} element={<Home />}/>
          <Route exact path={"/home"} element={<Home />}/>
          <Route exact path={"/login"} element={<Login />}/>
          <Route exact path={"/register"} element={<Register />}/>
          <Route exact path={"/profile"} element={<Profile />}/>
          <Route path={"/user"} element={<BoardUser />}/>
        </Routes>
      </div>
    </div>
  );
};

export default App;
