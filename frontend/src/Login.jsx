import { useState } from "react";
import {useNavigate} from 'react-router'
import {
    Button,
    Input,
    Form,
    Alert,
    Space,
} from 'antd'
import useAPI from "./api/useAPI";
import { useDispatch } from "react-redux";
import { useMutation } from "@tanstack/react-query";


function Login(){
    const [username, setUsername]=useState()
    const [password , setPassword]=useState()

    const api=useAPI()
    const dispatch=useDispatch()
    //const navigate=useNavigate()

      const { mutate: authorizeUser, error: mutationError, isPending: isMutationPending } = useMutation({
            mutationFn: (data) => api.user.auth(data),
            mutationKey: ['api.user.auth'],
            })

    const getValues= ()=>{
        const formDetails=new URLSearchParams()
        formDetails.append('username',username)
        formDetails.append('password', password)
        return formDetails
    }

    const onSubmit= async ()=>{
        authorizeUser(getValues(),{
            onSuccess: (data)=>{
                console.log(data)
            }
        })
    }

    return (
        <Form onFinish={()=>onSubmit()} layout="vertical">
            <Form.Item
            label="Логин"
            name="username"
            >
                <Input value={username}  variant="filled" onChange={(e)=>setUsername(e.currentTarget.value)} required/>
            </Form.Item>

            <Form.Item
            label="Пароль"
            name={'password'}
            >
                <Input value={password} variant="filled" onChange={(e)=>setPassword(e.currentTarget.value)} required/>
            </Form.Item>
            
            {mutationError && <Alert message={mutationError.message} type="error" showIcon closable/>}

            <Button htmlType="submit" loading={isMutationPending}>Войти</Button>
        </Form>
    )
}

export default Login