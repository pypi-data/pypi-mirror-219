import React, { useState } from "react"

export default function NewIcon({ onClick, width, height }) {
    const enterColor = '#42b983'
    const leaveColor = 'white'
    const [iconFill, setIconFill] = useState(leaveColor);
    const flashIcon = (setFn) => {
        setFn("red");
        setTimeout(() => setFn(enterColor), 50);
    }
    return <svg
        onMouseEnter={() => setIconFill(enterColor)}
        onMouseLeave={() => setIconFill(leaveColor)}
        onClick={(e) => {
            flashIcon(setIconFill);
            onClick(e)
        }}
        width={width}
        height={height}
    >
        <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24">
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" fill={iconFill} />
        </svg>
    </svg>
}