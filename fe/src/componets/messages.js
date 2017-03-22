/**
 * Created by fengqiang on 2017/2/5.
 */

import React, {Component} from 'react';
import Msg from './msg';
import $ from 'jquery';

const uri = "http://localhost:5000/msgs";

class Message extends Component {

  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      data: []
    };
  }

  componentDidMount() {
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
      return <div>{this.state.data.map((d) => <Msg key={d.openid} data={d}></Msg>)}</div>;

    }
  }
}

export default Message