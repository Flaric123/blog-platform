import { useEffect, useState } from 'react'
import {QueryClient, QueryClientProvider} from '@tanstack/react-query'
import {Provider, useDispatch} from 'react-redux'
import Login from './Login.jsx'
import '@ant-design/v5-patch-for-react-19';
import './App.css'
import { APP_STORE } from '../store/store.js';
import { clearUserData } from '../store/slices/userSlice.js';

const REACT_QUERY=new QueryClient()

function App() {
  return (
    <AppWrappers>
      <AppOnLoad>
        <Login/>
      </AppOnLoad>
    </AppWrappers>
  )
}

function AppOnLoad({children}){
  useUserRefresh()
  return children;
}

function AppWrappers({children}){
  return(
    <QueryClientProvider client={REACT_QUERY}>
      <Provider store={APP_STORE}>
        {children}
      </Provider>
    </QueryClientProvider>
  )
}

function useUserRefresh(){
  const dispatch=useDispatch()
  dispatch(clearUserData())
  console.log('fdlfkj')
}

export default App