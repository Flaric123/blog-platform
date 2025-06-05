import React from 'react'
import { useSelector } from 'react-redux';
import Login from '../pages/Login.jsx';
import {ROLES} from '../consts.js'

function withAccessCheck(element,allowedRoles) {
  return function(props) {
    const user = useSelector(state => state.userReducer);
    let response
    if (!user){
      response=<Login/>
    }
    else
      response=allowedRoles.includes && allowedRoles.includes(user.role) ? element(props) : <Login/>

    return response
  }
}

export default withAccessCheck