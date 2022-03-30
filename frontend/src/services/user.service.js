import axios from "axios";
const API_URL = "http://localhost:3000/api/";
const user = localStorage.getItem("user");

const getPublicContent = () => {
    return axios.get(API_URL + "public");
}

const getUserBoard = () => {
    return axios.get(API_URL + "userdata", { headers: {"Authorization" : `Bearer ${user.access_token}`}})
};

const deleteProduct = (product_id) => {
    return axios.delete(API_URL+ "deleteProduct/" + product_id)
}

const add_Product = (product_info) => {
    return axios.post(API_URL+ "addProduct", product_info)
}

const getModeratorBoard = () => {
    return axios.get(API_URL + "mod");
};

const getAdminBoard = () => {
    return axios.get(API_URL + "admin");
};

const UserService = {
    getPublicContent, getUserBoard, getModeratorBoard, getAdminBoard, deleteProduct, add_Product,
};

export default UserService;