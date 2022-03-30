import axios from "axios";
const API_URL = "http://localhost:3000/api/auth/";

const register = (username, email, password) => {
    return axios.post(API_URL + "register", {
        username,email,password,
    });
};

const login = (username,password) => {
    return axios.post(API_URL + "login",{
        username,password,
    })
    .then((response) => {
        // e.preventDefault();
        // console.log("Printing response data");
        // console.log(response);
        // console.log(response.data);
        if (response.data) {
            localStorage.setItem("user", JSON.stringify(response.data))
        }
        return response.data;
    });
};

const logout = () => {
    localStorage.removeItem("user");
    return axios.post(API_URL + "logout").then((response) => {
        console.log(response)
    });
};

const getCurrentUser = () => {
    return JSON.parse(localStorage.getItem("user"));
};

const AuthService = {
    register, login, logout, getCurrentUser,
}

export default AuthService;