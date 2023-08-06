import React, { useState } from "react"

export default function ClearIcon({ onClick, width, height, leaveColor = 'white' }) {
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
    >
        <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 240 240">
            <path stroke="#000" stroke-width="2" id="svg_5" d="m120.00312,40.99999c-43.62794,0.01871 -78.9844,35.37239 -79.00312,79.00312c0,43.63073 35.36894,78.98441 79.00312,78.99689c43.62794,-0.01247 78.9844,-35.36615 78.99688,-78.99065c-0.00624,-43.63697 -35.36271,-79.00936 -78.99688,-79.00936zm60.27691,79.00312c-0.01871,12.1193 -3.6367,23.37784 -9.78728,32.83376l-83.32599,-83.30694c9.45043,-6.16257 20.70986,-9.78651 32.84259,-9.81146c33.28548,0.06861 60.21454,27.00178 60.27068,60.28463zm-120.56631,0c0.02495,-12.1193 3.64294,-23.39031 9.81223,-32.84624l83.30727,83.31318c-9.45667,6.15009 -20.70986,9.76779 -32.83635,9.78651c-33.27924,-0.03119 -60.21454,-26.97059 -60.28315,-60.25345z"
                fill={iconFill} />
        </svg>
    </svg>
}