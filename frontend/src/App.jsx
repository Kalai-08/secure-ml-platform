import { useEffect, useState} from "react";
import { api } from "./api"
import Login from "./Login"

export default function App(){
    const [token, setToken] = useState(() => sessionStorage.getItem("token"))
    const [user, setUser] = useState(null)

    useEffect(()=>{
        if(!token) return;
        api("/auth/me", {token})
         .then(setUser)
         .catch(() => {
            sessionStorage.removeItem("token");
            setToken(null)
         })
    },[token])

    function handleLogin(newToken){
        sessionStorage.setItem("token", newToken)
        setToken(newToken)
    }

    function logout(){
        sessionStorage.removeItem("token")
        setToken(null)
        setUser(null)
    }

    if(!token) return <Login onLogin={handleLogin} />
    if(!user) return <p>Loading...</p>

    return(
        <div style={{maxWidth:600, margin: "80px auto"}}>
            <h1>Welcome, {user.email}</h1>
            <p>Role: {user.role}</p>
            <button onClick={logout}>Log out</button>
        </div>
    )
}