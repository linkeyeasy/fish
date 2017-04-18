/**
 * Created by fengqiang on 2017/2/6.
 */
import React, {Component} from 'react';
import './msg.css';
import {
  Media,
  Row,
  Image,
  Col
} from 'react-bootstrap';

class User extends Component {
  constructor(props) {
    super(props);
    this.state = {
      active: true
    };
  }

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
            </Col>
          </Row>
        </Media.Heading>
        <div>
          <div>
            OpenID： {this.props.data.openid}
          </div>
          <div>
            性别： {this.props.data.sex === '1' ? '男' : '女' }
          </div>
          <div>
            地址： {this.props.data.location}
          </div>
          <div>
            备注： {this.props.data.remark}
          </div>
          <div>
            更新时间： {this.props.data.update_time}
          </div>
          <div>
            创建时间： {this.props.data.creation_time}
          </div>
        </div>
      </Media.Body>
    </Media>
  )
}

export default User