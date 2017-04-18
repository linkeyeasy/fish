/**
 * Created by fengqiang on 2017/2/5.
 */

import React, {Component} from 'react';
import AsyncUser from './async';
import User from './user';
import $ from 'jquery';

class Users extends Component {

  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      data: []
    };
  }

  componentDidMount() {
    const uri = 'http://localhost:5000/users';
    $.get(uri, function (r) {
      this.setState({
        data: r.data,
        loading: false
      });
    }.bind(this));

  }

  render() {
    if (this.state.loading) {
      return <div style={{color:`red`, textAlign:`center`}}>努力加载中...</div>;
    } else {
      return <div>
        <AsyncUser />
        {this.state.data.map((d) => <User key={d.openid} data={d}></User>)}
      </div>;

    }
  }
}

export default Users
