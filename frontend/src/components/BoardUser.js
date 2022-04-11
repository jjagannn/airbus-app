import React, { useState, useEffect } from "react";
import UserService from "../services/user.service";
import {Modal, Button, Form} from 'react-bootstrap';
// import {useForm} from 'react-hook-form';
const BoardUser = () => {
  const [content, setContent] = useState("");
  useEffect(() => {
    UserService.getUserBoard().then(
      (response) => {
        setContent(response.data);
      },
      (error) => {
        const _content =
          (error.response &&
            error.response.data &&
            error.response.data.message) ||
          error.message ||
          error.toString();
        setContent(_content);
      }
    );
  }, []);
  const deleteProduct = (product_id) => {
    UserService.deleteProduct(product_id).then(
      () => {
        window.location.reload();
      }
      )
    }
  // const updateProduct = (product_id) => {
  //   UserService.updateProduct(product_id).then(
  //     () => {
  //       window.location.reload();
  //     }
  //     )
  //   }
    const [show, setShow] = useState(false);
    const [showUpdateModal, setShowUpdateModal] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const handleCloseUpdateModal = () => setShowUpdateModal(false);
    const handleShowUpdateModal = () => setShowUpdateModal(true);
    const [id, setId] = useState("");
    const [productName, setProductName] = useState("");
    const [productCat, setProductCat] = useState("");
    const [productDescr, setProductDescr] = useState("");
    const [units, setUnits] = useState("");

    function validateForm() {
      return (id.length > 0 && productName.length > 0 && productCat.length >0 && productDescr.length >0 && units.length >0);
    };
    
    const addProduct = (product_info) => {
      UserService.add_Product(product_info)
      .then(
        () => {
          setId("");
          setProductName("");
          setProductDescr("");
          setProductCat("");
          setUnits("");
          window.location.reload();
        },
        err => {
          alert("Product ID already exists!")
      }
        )
      };

      const updateProduct = (product_info) => {
        UserService.update_Product(product_info)
        .then(
          () => {
            setId("");
            setProductName("");
            setProductDescr("");
            setProductCat("");
            setUnits("");
            window.location.reload();
          },
          err => {
            alert("Error updating the product")
        }
          )
        };
// Add user submit handling
    const handleSubmit = (e) => {
      e.preventDefault();
      const itemData = {id, productName, productCat, productDescr, units};
      console.log(itemData);
      addProduct(itemData);
      handleClose();
    };
    const handleSubmitUpdateModal = (e) => {
      e.preventDefault();
      const itemData = {id, productName, productCat, productDescr, units};
      console.log(itemData);
      updateProduct(itemData);
      handleClose();
    };
    const [query, setQuery] = useState("");
  //   const filtered = getValues("products").filter(
  //     product =>
  //         product.description.toLowerCase().indexOf(searchTerm) > -1,
  // );
  // set filtered products in state
  // setFilteredProducts(filtered);

  return (
    <div className="container">
      {/* <header className="jumbotron">
        <h3>Product details</h3>
      </header> */}
  <table className="table">
  <thead className="thead-dark">
    <tr>
      <th scope="col">Product ID</th>
      <th scope="col">Product Category</th>
      <th scope="col">Product Name</th>
      <th scope="col">Product Description</th>
      <th scope="col">Units</th>
      <th scope="col">Action (Update or Delete record)</th>
    </tr>

  </thead>
  <tbody>
{/* Add product modal */}
        <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Add a product</Modal.Title>
        </Modal.Header>
        <Modal.Body>
        
          <Form.Group className="mb-3">
            <Form.Label>Product ID</Form.Label>
            <Form.Control required value={id} onChange={(e) => setId(e.target.value)} placeholder="Enter product id"/>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Product Category</Form.Label>
            <Form.Control required value={productCat} onChange={(e) => setProductCat(e.target.value)} placeholder="Enter product category"/>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Product Name</Form.Label>
            <Form.Control required value={productName} onChange={(e) => setProductName(e.target.value)} placeholder="Enter product name"/>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Product Description</Form.Label>
            <Form.Control required value={productDescr} onChange={(e) => setProductDescr(e.target.value)} placeholder="Enter product description"/>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Units</Form.Label>
            <Form.Control required value={units} onChange={(e) => setUnits(e.target.value)} placeholder="Enter the number of units"/>
          </Form.Group>

        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>Close</Button>
          <Button variant="primary" onClick={handleSubmit} disabled={!validateForm()}>Submit</Button>
        </Modal.Footer>
        </Modal>

{/* Update product modal */}
        <Modal show={showUpdateModal} onHide={handleCloseUpdateModal}>
        <Modal.Header closeButton>
          <Modal.Title>Update product</Modal.Title>
        </Modal.Header>
        <Modal.Body>
        
          <Form.Group className="mb-3">
            <Form.Label>Product ID</Form.Label>
            <Form.Control required value={id} onChange={(e) => setId(e.target.value)} placeholder="Enter product id"/>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Product Category</Form.Label>
            <Form.Control required value={productCat} onChange={(e) => setProductCat(e.target.value)} placeholder="Enter product category"/>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Product Name</Form.Label>
            <Form.Control required value={productName} onChange={(e) => setProductName(e.target.value)} placeholder="Enter product name"/>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Product Description</Form.Label>
            <Form.Control required value={productDescr} onChange={(e) => setProductDescr(e.target.value)} placeholder="Enter product description"/>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Units</Form.Label>
            <Form.Control required value={units} onChange={(e) => setUnits(e.target.value)} placeholder="Enter the number of units"/>
          </Form.Group>

        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseUpdateModal}>Close</Button>
          <Button variant="primary" onClick={handleSubmitUpdateModal} disabled={!validateForm()}>Submit</Button>
        </Modal.Footer>
        </Modal>

{/* Searchbar */}
        <tr>
          <td>
            <input placeholder="Filter by Category" onChange={event => setQuery(event.target.value.trim())} />
            </td>
        </tr>

{/* Table displaying all products data */}
        {content.table_data?.filter((field)=>{return field.product_category.toLowerCase().includes(query)}).map((item, i) => (
        <tr key={i}>
          <td>{item.product_id}</td>
          <td>{item.product_category}</td>
          <td>{item.product_name}</td>
          <td>{item.product_description}</td>
          <td>{item.units}</td>
          <td>
            <button type="button" onClick={handleShowUpdateModal}>Update</button>
            &nbsp;&nbsp;&nbsp;
            <button type="button" onClick={()=>{deleteProduct(item.product_id)}}>Delete</button>
          </td>
        </tr>
          ))}
{/* Add product submit */}
        <tr>
          <td>
            <Button type="button" onClick={handleShow}>Add a product</Button>
          </td>
        </tr>
  </tbody>
</table>

    </div>
  );
};
export default BoardUser;