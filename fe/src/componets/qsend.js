/**
 * Created by fengqiang on 2017/2/13.
 */

import React, {Component} from 'react';
// import $ from 'jquery';
import './qsend.css';
import ReactMarkdown from 'react-markdown';
import 'codemirror/lib/codemirror.css';
import CodeMirror from 'react-codemirror';
require('codemirror/mode/markdown/markdown');


class QSend extends Component {

  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      code: '',
      data: '# this is a demo \n\n this is a paragram'
    };
  }

  componentDidMount() {
    this.setState({
      loading: false
    });
  }

  updateCode = (newCode) => {
    this.setState({code: newCode})
  };

  render() {
    if (this.state.loading) {
      return <div style={{color:`red`, textAlign:`center`}}>努力加载中...</div>;
    } else {
      const options = {
        lineNumbers: true,
        mode:'markdown'
      };
      return <div>
        <CodeMirror value={this.state.code} onChange={this.updateCode} options={options}></CodeMirror>
        <ReactMarkdown autoSave={true} source={this.state.code}></ReactMarkdown>
      </div>;

    }
  }
}

export default QSend