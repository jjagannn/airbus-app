import React, { useState, useEffect } from "react";
import UserService from "../services/user.service";
const Home = () => {
  const [content, setContent] = useState("Test data");
  useEffect(() => {
    UserService.getPublicContent().then(
      (response) => {
        setContent(response.data);
      },
      (error) => {
        const _content =
          (error.response && error.response.data) ||
          error.message ||
          error.toString();
        setContent(_content);
      }
    );
  }, []);
  return (
    <div className="container">
      <header className="jumbotron">
        <h3>{content.message}</h3>
      </header>
    </div>
  );
};
export default Home;