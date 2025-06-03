import { createSlice } from '@reduxjs/toolkit'

const USER_DATA_LOCAL_STORAGE_KEY = "userSlice/user";

const GUEST_DATA_DEFAULT = Object.freeze({
  role: "non-user",
  apiAccessToken: undefined,
  id: undefined,
  phone: undefined,
  email: undefined,
  name: undefined,
  avatar: undefined, 
})

const readUserFromLocalStorage = () => {
  const user = localStorage.getItem(USER_DATA_LOCAL_STORAGE_KEY);
  return user ? JSON.parse(user) : null;
}

const writeUserToLocalStorage = (user) => {
  localStorage.setItem(USER_DATA_LOCAL_STORAGE_KEY, JSON.stringify(user));
}

const removeUserFromLocalStorage = () => {
  localStorage.removeItem(USER_DATA_LOCAL_STORAGE_KEY);
}

const USER_DATA_FROM_LOCAL_STORAGE = readUserFromLocalStorage();

const userSlice = createSlice({
  name: "user",
  initialState: USER_DATA_FROM_LOCAL_STORAGE ?? GUEST_DATA_DEFAULT,
  reducers: {
    setUserData: (state, action) => {
      writeUserToLocalStorage(action.payload);
      return action.payload;
    },
    clearUserData: (state, action) => {
      removeUserFromLocalStorage();
      return GUEST_DATA_DEFAULT;
    },
  }
})

export const { setUserData, clearUserData } = userSlice.actions;
export const userReducer = userSlice.reducer;