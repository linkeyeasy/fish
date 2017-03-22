import React from 'react';
import ReactDOM from 'react-dom';
import {browserHistory, Router, Route, IndexRoute} from 'react-router';
import App from './App';
import Message from './componets/messages';
import Users from './componets/users';
import QSend from './componets/qsend';
import Home from './componets/home';
import Material from './componets/materials';
import './index.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';

ReactDOM.render((
  <Router history={browserHistory}>
    <Route path="/" component={App}>
      <IndexRoute component={Home}/>
      <Route path="/msg" component={Message}>
      </Route>
      <Route path="/users" component={Users}>
      </Route>
      <Route path="/qsend" component={QSend}>
      </Route>
      <Route path="/materials" component={Material}>
      </Route>
    </Route>
  </Router>
), document.getElementById('root'));