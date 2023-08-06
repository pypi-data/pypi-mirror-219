
import React, { useState } from "react"

export default function YesIcon({ onClick, width, height }) {
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
            <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"
                fill={runIconFill} />
        </svg>
    </svg>
}