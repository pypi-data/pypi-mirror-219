import React, { useState } from "react"

export default function DeleteIcon({ onClick, width, height, leaveColor = 'white' }) {
    const enterColor = '#42b983'
    const [deleteIconFill, setDeleteIconFill] = useState(leaveColor);
    const flashIcon = (setFn) => {
        setFn("red");
        setTimeout(() => setFn(enterColor), 50);
    }
    return <svg
        onMouseEnter={() => setDeleteIconFill(enterColor)}
        onMouseLeave={() => setDeleteIconFill(leaveColor)}
        onClick={(e) => {
            flashIcon(setDeleteIconFill);
            onClick(e)
        }}
        width={width}
        height={height}
    >
        <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" fill={deleteIconFill} />
            <path d="M0 0h24v24H0z" fill="none" />
        </svg>
    </svg>
}