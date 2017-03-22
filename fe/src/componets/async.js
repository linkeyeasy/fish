/**
 * Created by fengqiang on 2017/2/6.
 */
import React, {Component} from 'react';
import $ from 'jquery';
import {
  Row,
  Button,
  Col,
  Alert
} from 'react-bootstrap';

class AsyncUser extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      success: false
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
      <Col xs={12} md={12}>
        <Alert
          bsStyle={this.state.success ? "success" : "warning"}>
          <Button
            disabled={this.state.loading}
            onClick={this.handleClick}
            bsStyle={this.state.success ? "success" : "primary"}
          >{this.state.loading ? "同步中。。。" : "同步用户信息"}</Button>
          <div style={{marginTop:10 + 'px'}}></div>
          <p>
            {this.state.success ? "用户数据已全部同步成功！" : "同步数据可能用时较长，请耐心等待..."}
          </p>
        </Alert>
      </Col>
    </Row>
  )
}

export default AsyncUser