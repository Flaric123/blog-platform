import {useSelector} from 'react-redux'
import { useMemo } from 'react';
import { USER_SERVICE } from "./userService";
import axios from 'axios'

function useAPI(){
    const user=useSelector(state => state.user)
    const apiAccessToken = user?user.apiAccessToken:''
    const BACKEND_BASE_URL='http://localhost:8000/'

    return useMemo(() => {
    const userService = USER_SERVICE;

    const services = {
      user: userService,
    }

    const http = axios.create({
      baseURL: BACKEND_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': apiAccessToken ? `Bearer ${apiAccessToken}` : '',
      }
    });

    // const prepareService = service => {
    //   service.services = services;
    //   service.http = http;
    // }

    userService.services=services
    userService.http=axios.create({
      baseURL: BACKEND_BASE_URL,
      headers:{
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    return services;
  }, [apiAccessToken]);
}

export default useAPI