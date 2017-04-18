/**
 * Created by fengqiang on 2017/2/13.
 */

import React, {Component} from 'react';
import $ from 'jquery';

const uri = 'http://localhost:5000/materials';

class Material extends Component {

  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      data: []
    };
  }

  componentDidMount = () => {
    this.setState({loading: true});
    $.get(uri, function (r) {
      this.setState({
        loading: false
      });
      if (r.r === true) {
        this.setState({
          data: r.data
        });
      }

    }.bind(this));
  };

  updateCode = (newCode) => {
    this.setState({code: newCode})
  };

  render() {
    if (this.state.loading) {
      return <div style={{color:`red`, textAlign:`center`}}>努力加载中...</div>;
    } else {
      return <div>{this.state.data}</div>

    }
  }
}

export default Material