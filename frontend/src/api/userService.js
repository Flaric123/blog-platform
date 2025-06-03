export const USER_SERVICE={
    async auth(authData){
        //try{
            const response=await USER_SERVICE.http.post('/token', authData)
            return response.data
        // }
        // catch (error){
        //     console.log(error.message)
        // }
    }
}