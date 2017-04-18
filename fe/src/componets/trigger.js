/**
 * Created by fengqiang on 2017/2/6.
 */
import React, {Component} from 'react';
import $ from 'jquery';
import {
  Row,
  Button,
  Col,
  Modal
} from 'react-bootstrap';
import './trigger.css';

class Trigger extends Component {
  constructor(props) {
    super(props);
    this.state = {
      show: false
    };
  }

  handleClick = () => {
    this.setState({loading: true});
    const uri = 'http://localhost:5000/sync/users';
    $.get(uri, function (r) {
      this.setState({
        loading: false
      });
      if (r.r === true) {
        this.setState({
          success: true
        });
      }

    }.bind(this));
  };

  render = ()=> (

    <Row>
      <div className='modal-container' style={{height: 200}}>
      <Button
        bsStyle='primary'
        bsSize='large'
        onClick={() => this.setState({show: true})}
      >
      </Button>

      <Modal
        show={this.state.show}
        container={this}
        aria-labelledby="contained-modal-title"
      >
        <Modal.Header closeButton>
          <Modal.Title id='contained-modal-title'>Title text</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          this is a body
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={() => this.setState({show: true})}></Button>
        </Modal.Footer>
      </Modal>
      </div>
    </Row>
  )
}

export default Trigger
