import { useState } from "react";
import { api } from "./api";

export default function Login({onLogin}){
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)

    async function handleSubmit(e) {
        e.preventDefault();
        setError("");
        setLoading(true);
        
        try{
            const data = await api("/auth/login",{
                method: "POST",
                form: {username: email, password: password}
            })

            onLogin(data.access_token)
        }catch(err){
            setError(
                err.status === 429
                    ? "Too many failed attempts. Try again in 15 minutes."
                    : err.message
            )
        }finally{
            setLoading(false)
        }
    }

    return(
        <form onSubmit={handleSubmit} style={{ maxWidth: 360, margin: "80px auto" }}>
            <h1>Sign in</h1>
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                style={{ display: "block", width: "100%", marginBottom: 12 }}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{ display: "block", width: "100%", marginBottom: 12 }}
            />
            {error && <p style={{ color: "crimson" }}>{error}</p>}
            <button type="submit" disabled={loading}>
                {loading ? "Signing in..." : "Sign in"}
            </button>
        </form>
    );
}