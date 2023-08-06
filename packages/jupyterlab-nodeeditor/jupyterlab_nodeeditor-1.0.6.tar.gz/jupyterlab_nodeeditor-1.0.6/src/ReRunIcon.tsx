
import React, { useState } from "react"

export default function ReRunIcon({ onClick, width, height }) {
    const enterColor = '#42b983'
    const leaveColor = 'white'
    const [runIconFill, setRunIconFill] = useState(leaveColor);
    const flashIcon = (setFn) => {
        setFn("red");
        setTimeout(() => setFn(enterColor), 50);
    }
    return <svg
        onMouseEnter={() => setRunIconFill(enterColor)}
        onMouseLeave={() => setRunIconFill(leaveColor)}
        onClick={(e) => {
            flashIcon(setRunIconFill)
            onClick(e)
        }}
        width={width}
        height={height}
    >
        <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24">
            <path d="M4 18l8.5-6L4 6v12zm9-12v12l8.5-6L13 6z" fill={runIconFill}/>
        </svg>
    </svg>
}