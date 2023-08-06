
import React, { useState } from "react"

export default function RunIcon({ onClick, width, height }) {
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
            <path d="M8 5v14l11-7z" fill={runIconFill} />
            <path d="M0 0h24v24H0z" fill="none" />
        </svg>
    </svg>
}