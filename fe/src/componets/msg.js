/**
 * Created by fengqiang on 2017/2/6.
 */
import React, {Component} from 'react';
import './msg.css';
import $ from 'jquery';

import {
  Media,
  Row,
  Col,
  Image,
  Glyphicon
} from 'react-bootstrap';

class Msg extends Component {
  constructor(props) {
    super(props);
    this.state = {
      collection: true,
      reply: false,
      content: ''
    };
  }

  handleClick = (data) => {
    this.setState({loading: true});
    const uri = 'http://localhost:5000/send';
    $.post(
      uri,
      {openid: data.from_user, content: this.state.content},
      function (r) {
      this.setState({
        loading: false
      });
      if (r.r === true) {
        this.setState({
          reply: true
        });
      }
    }.bind(this));
  };

  render = ()=>(
    <Media>
      <Media.Left>
        <Image width={64} height={64} src={this.props.data.head_img_url} alt="头像" circle/>
      </Media.Left>
      <Media.Body>
        <Media.Heading>
          <Row>
            <Col xs={9} md={9}>
              {this.props.data.nickname}
              <span className="gray" style={{fontSize: 0.8 + 'em'}}> {this.props.data.creation_time}</span>
            </Col>
            <Col xs={1} md={1}>
              <div className={this.props.data.reply ? 'green': 'gray'}>
              {this.props.data.reply ? '已回复': '新消息'}
              </div>
            </Col>
            <Col xs={2} md={2}>
              <a href="#" className={this.state.collection ? 'yellow': 'gray'}><Glyphicon glyph="star"/></a>
              <a href="#" onClick={this.handleClick.bind(this, this.props.data)} className={this.state.reply ? 'yellow': 'gray'}><Glyphicon glyph="share-alt"/></a>
            </Col>
          </Row>
        </Media.Heading>
        <p>
          {this.props.data.content}
        </p>
      </Media.Body>
    </Media>
  )
}

export default Msg
