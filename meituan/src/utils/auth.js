const USER_KEY = "USER_KEY"
const TOKEN_KEY = "JWT_TOKEN_KEY"

class Auth{
    constructor(){
        // 在构造函数内，直接获取localStorage的token和user
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
        // 可以调用这个方法，保存user，token到localStorage
        this.user = user
        this.token = token
        localStorage.setItem(USER_KEY, JSON.stringify(user))
        localStorage.setItem(TOKEN_KEY, token)
    }

    clearUserToken(){
        // 用户退出登录的时候，调用这个方法清理localStorage
        this.user = null;
        this.token = null;
        localStorage.removeItem(USER_KEY)
        localStorage.removeItem(TOKEN_KEY)
    }

    get is_authenticated(){
        // 判断localStorage里面是否有用户信息，也就是说用户是否登录
        if(this.user && this.token){
            return true
        }else{
            return false
        }
    }
}


export default Auth.getInstance()