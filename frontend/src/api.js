const API_URL = import.meta.env.VITE_API_URL;

export async function api(path, {method = "GET", body, form, token} ={}){
    const headers = {}
    let payload

    if(form){
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        paylaod  = new URLSearchParams(form)
    }else if(body){
        headers["Content-Type"] = "application/json"
        payload = JSON.stringify(body)
    }

    if(token) headers.Authorization = `Bearer ${token}`

    const res = await fetch(`${API_URL}${path}`, {method, headers, body: payload})
    const data = await res.json().catch(() => null)

    if(!res.ok){
        const detail = Array.isArray(date?.detail)
        ? data.detail.map((d) => d.msg).join(", ")
        : data?.detail;

        const err = new Error(detail || "Request failed")
        err.status = res.status
        throw err
    }
    return data;
}