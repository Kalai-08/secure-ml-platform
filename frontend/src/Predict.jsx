import { useState } from "react";
import { api } from "./api";

const FIELDS = [
    ["mean_radius", "Mean radius"],
    ["mean_texture", "Mean texture"],
    ["mean_perimeter", "Mean perimeter"],
    ["mean_area", "Mean area"]
]

export default function Predict({token}){
    const [values, setValues] = useState({
        mean_radius: "",
        mean_texture: "",
        mean_perimeter: "",
        mean_area: ""
    })

    const [result, setResult] = useState(null)
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)

    async function handleSubmit(e){
        e.preventDefault()
        setLoading(true)
        setError(null)

        try {
            const body = Object.fromEntries(
                FIELDS.map(([key]) => [key, Number(values[key])])
            )

            const data = await api("/predict",
                 {
                    method : "POST",
                    body,
                    token
                 }
            )

            setResult(data)
        } catch (err) {
            setError(
                err.status === 403
                    ? "You don't have permission to run prediction."
                    : err.message
            )
        }finally{
            setLoading(false)
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <h2>Tumor prediction</h2>
            {FIELDS.map(([key, label]) => (
                <label key={key} style={{ display: "block", marginBottom: 12 }}>
                {label}
                <input
                    type="number"
                    step="any"
                    required
                    value={values[key]}
                    onChange={(e) => setValues({ ...values, [key]: e.target.value })}
                    style={{ display: "block", width: "100%" }}
                />
                </label>
            ))}
            {error && <p style={{ color: "crimson" }}>{error}</p>}
            <button type="submit" disabled={loading}>
                {loading ? "Predicting..." : "Predict"}
            </button>
            {result && (
                <p>
                Result: <b>{result.prediction}</b> (probability benign:{" "}
                {(result.probability_benign * 100).toFixed(2)}%)
                </p>
            )}
        </form>
    );
}
