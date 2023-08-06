import React, { useState } from "react"

export default function ExportIcon({ onClick, width, height, leaveColor = 'white' }) {
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
            <path stroke="#000" stroke-width="2" id="svg_5" d="m173.32693,150.69569c-10.63352,18.30417 -30.41599,30.64612 -53.15582,30.68728c-33.96835,-0.0588 -61.42699,-27.47096 -61.49179,-61.35691c0.06481,-33.90358 27.52344,-61.30988 61.49179,-61.37456c22.73394,0.04116 42.51051,12.37722 53.14993,30.68139l23.34072,13.42973l0.84244,0.48215c-7.72329,-35.57348 -39.38821,-62.23302 -77.33308,-62.24478c-43.72998,0.01176 -79.16524,35.37945 -79.17113,79.02606c0.01179,43.62897 35.44703,78.99666 79.17113,79.00841c37.95076,-0.01176 69.62746,-26.68305 77.33308,-62.26242l-0.83065,0.47627l-23.34661,13.44737l-0.00001,0.00001zm25.41441,-30.66963l-42.1217,-24.27817l0,13.50616l-64.65533,0l0,21.52636l64.65533,0l0,13.50616l42.1217,-24.26053l0,0.00001z"
                fill={iconFill} />
        </svg>
    </svg>
}