import React, {Component} from 'react';
import {
  Grid,
  Row
} from 'react-bootstrap';

import './App.css';
import NavBar from './componets/navbar';
import Footer from './componets/footer';

class App extends Component {


  render() {
    return (
      <Grid>
        <Row className="bar">
          <NavBar></NavBar>
        </Row>
        <Row>
          {this.props.children || "无对象"}
        </Row>
        <Row>
          <Footer></Footer>
        </Row>
      </Grid>
    );
  }
}

export default App;
