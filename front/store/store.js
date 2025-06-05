import {configureStore} from '@reduxjs/toolkit' 
import { userReducer } from './slices/userSlice'

export const APP_STORE = configureStore({
    reducer:{
        userReducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: false,
        }),
})