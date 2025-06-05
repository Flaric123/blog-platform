import { useEffect, useState } from 'react'
import { Route, Navigate, RouterProvider, createBrowserRouter, createRoutesFromElements } from "react-router";
import {QueryClient, QueryClientProvider} from '@tanstack/react-query'
import {Provider, useDispatch} from 'react-redux'
import Login from './pages/Login.jsx'
import '@ant-design/v5-patch-for-react-19';
import { APP_STORE } from '../store/store.js';
import { clearUserData } from '../store/slices/userSlice.js';
import AdminLayout from './layouts/AdminLayout.jsx';
import AuthorLayout from './layouts/AuthorLayout.jsx';
import ReaderLayout from './layouts/ReaderLayout.jsx';

const REACT_QUERY=new QueryClient()

function App() {
  return (
    <AppWrappers>
      <AppOnLoad>
        <AppRouter/>
      </AppOnLoad>
    </AppWrappers>
  )
}

function AppOnLoad({children}){
  //useUserRefresh()
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

function AppRouter(){
  return <RouterProvider router={createBrowserRouter(createRoutesFromElements(
    <>
      <Route path="/admin" element={<AdminLayout />} >

      </Route>

      <Route path='/author' element={<AuthorLayout/>}>

      </Route>

      <Route path='/reader' element={<ReaderLayout/>}>

      </Route>

      <Route path="/" element={<Login />} />
    </>
  ))} />
}

function useUserRefresh(){
  const dispatch=useDispatch()
  dispatch(clearUserData())
  console.log('fdlfkj')
}

export default App