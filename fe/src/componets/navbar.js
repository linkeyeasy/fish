/**
 * Created by fengqiang on 2017/2/5.
 */

import React, {Component} from 'react';
import logo from '../logo.svg';
import './navbar.css';
import {
  Grid,
  Navbar,
  NavItem,
  MenuItem,
  NavDropdown,
  Nav
} from 'react-bootstrap';
import {IndexLink} from 'react-router';
import {LinkContainer} from 'react-router-bootstrap';

class NavBar extends Component {
  constructor(props) {
    super(props);

    const manager = <NavDropdown title="管理" id="manager">
      <MenuItem header={true}>管理</MenuItem>
      <MenuItem divider/>
      <LinkContainer to='msg'><MenuItem>消息</MenuItem></LinkContainer>
      <LinkContainer to='users'><MenuItem>用户</MenuItem></LinkContainer>
      <LinkContainer to='materials'><MenuItem>素材</MenuItem></LinkContainer>
    </NavDropdown>
    const module =
      <NavDropdown title="功能" id="module">
        <MenuItem header={true}>功能</MenuItem>
        <MenuItem divider/>
        <LinkContainer to='qsend'><MenuItem>群发</MenuItem></LinkContainer>
        <MenuItem>自动回复</MenuItem>
        <MenuItem>投票管理</MenuItem>
        <MenuItem divider/>
        <MenuItem>自定义菜单</MenuItem>
      </NavDropdown>

    this.state = {manager: manager, module: module}
  }

  render() {
    return <Navbar fixedTop>
      <Grid>
        <Navbar.Header>
          <a className="app-logo-container">
            <img src={logo} className="App-logo" alt="logo"/>
          </a>
          <Navbar.Brand>
            <IndexLink to="/">微信公众号-管理平台</IndexLink>
          </Navbar.Brand>
        </Navbar.Header>
        <Navbar.Collapse>
          <Nav>
            {this.state.manager}
            {this.state.module}
          </Nav>
          <Nav pullRight>
            <NavItem>搜索xxx</NavItem>
          </Nav>
        </Navbar.Collapse>
      </Grid>
    </Navbar>
  }
}

export default NavBar