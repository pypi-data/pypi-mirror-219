import React, { useState } from "react"

export default function ArrownIcon({ onClick, width, height, leaveColor = 'white', rotate = "0deg" }) {
    const enterColor = '#42b983'
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
        style={{
            transform:`rotate(${rotate})`
        }}
    >
        <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" fill={iconFill} stroke="2px" />
        </svg>
    </svg>
}