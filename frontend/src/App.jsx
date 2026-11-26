import {useEffect, useState} from "react";
import {api} from "./api";

export default function App(){
  const [status, setStatus] = useState("checking...")

  useEffect(()=>{
    api("/health")
    .then((d) => setStatus(JSON.stringify(d)))
    .catch((e) => setStatus("Error: " + e.message))
  },[])

  return <h1>Backend: {status}</h1>
}