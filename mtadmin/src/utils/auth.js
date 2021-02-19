const USER_KEY = "USER_KEY"
const TOKEN_KEY = "JWT_TOKEN_KEY"

class Auth{
    constructor(){
        // get user obj and token from browser localStorage
        this.token = null
        this.user = null
        this.token = localStorage.getItem(TOKEN_KEY)
        const userJson = localStorage.getItem(USER_KEY)
        if(userJson){
            this.user = JSON.parse(userJson)
        }
    }

    //实现单实例
    static getInstance(){
        if(!this._instance){
            this._instance = new Auth()
        }
        return this._instance
    }

    setUserToken(user, token){
        // save user obj and token to browser localStorage
        this.user = user
        this.token = token
        localStorage.setItem(USER_KEY, JSON.stringify(user))
        localStorage.setItem(TOKEN_KEY, token)
    }

    clearUserToken(){
        // for user loggin out to clear local storage
        this.user = null;
        this.token = null;
        localStorage.removeItem(USER_KEY)
        localStorage.removeItem(TOKEN_KEY)
    }

    get is_authenticated(){
        // to judge if the user is logged in or not
        if(this.user && this.token){
            return true
        }else{
            return false
        }
    }
}


export default Auth.getInstance()