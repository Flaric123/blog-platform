import { useState , useEffect } from "react";
import {useNavigate} from 'react-router'
import {
    Button,
    Input,
    Form,
    Alert,
    message,
} from 'antd'
import { EyeInvisibleOutlined, EyeTwoTone } from '@ant-design/icons';
import useAPI from "../api/useAPI";
import { useDispatch } from "react-redux";
import { useMutation } from "@tanstack/react-query";
import { setUserData } from "../../store/slices/userSlice";


function Login(){
    const [username, setUsername]=useState()
    const [password , setPassword]=useState()

    const api=useAPI()
    const dispatch=useDispatch()
    const navigate=useNavigate()

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
                message.success('success')
                dispatch(setUserData(data))
                navigate(`/${data.role}`)
            }
        })
    }

    useEffect(()=>{
        if (mutationError){
            message.error(mutationError.message)
        }
    }, [mutationError])

    return (
        <div style={{height:'100vh',display:'flex', placeContent:'center', placeItems:'center'}}>
            <Form onFinish={()=>onSubmit()} layout="vertical" style={{width:'100%', maxWidth:'600px', display:'flex', flexDirection:'column', padding:'5px'}} size="large">
                
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
                    <Input.Password value={password} variant="filled" onChange={(e)=>setPassword(e.currentTarget.value)} required
                    iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}/>
                </Form.Item>

                <Button htmlType="submit" style={{alignSelf:'center'}} loading={isMutationPending}>Войти</Button>
            </Form>
        </div>
    )
}

export default Login