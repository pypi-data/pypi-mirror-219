import React, { useRef } from "react"

export default function LockIcon({ id, width, height, initlock = false, onChange, leaveColor = "white" }) {
    const pathRef = useRef(null)
    const lockRef = useRef(initlock)
    const enterColor = '#42b983'

    const lockD = "m177.66966,107.17221l0,-20.4573l-0.00914,0c-0.00914,-25.25039 -25.90876,-45.71491 -57.86534,-45.71491s-57.86534,20.47173 -57.86534,45.72213l0,0l0,20.45008l-20.92983,0l0,87.82778l157.59035,0l0,-87.82778l-20.92069,0zm-97.45935,-20.45008c0,0 0,0 0,0c0,-17.25227 17.75974,-31.28508 39.58487,-31.28508c21.84339,0 39.60314,14.03281 39.60314,31.27786c0,0 0,0 0,0l0,20.4573l-79.18801,0l0,-20.45008z"
    const unlockD = "m147.00933,108.89097l-13.57534,0l0,-20.98125c0,0 0,0 0,-0.00741c0,-17.69298 11.95294,-32.09028 26.63446,-32.09028c14.69382,0 26.64061,14.3973 26.64061,32.09028c0,0 0,0 0,0l0,20.98866l12.29094,0l0,-20.98866l-0.00615,0c-0.00615,-25.90625 -17.42855,-46.90231 -38.9254,-46.90231s-38.9254,21.00347 -38.9254,46.90972l0,20.98125l-80.14305,0l0,90.10902l106.00933,0l0,-90.10902z"

    const getDByLock = (lock) => {
        return lock ? lockD : unlockD
    }
    const setLock = (v) => {
        if (!pathRef.current) {
            return
        }
        const element = pathRef.current as unknown as SVGPathElement
        element.setAttribute("d", getDByLock(v))
        element.setAttribute("data-lock", v)
        lockRef.current = v
        if (onChange) {
            onChange(v)
        }
    }
    const setIconFill = (color) => {
        if (!pathRef.current) {
            return
        }
        const element = pathRef.current as unknown as SVGPathElement
        element.setAttribute("fill", color)
    }


    return <svg
        id={`lock_${id}`}
        onMouseEnter={() => setIconFill(enterColor)}
        onMouseLeave={() => setIconFill(leaveColor)}
        onClick={(e) => {
            setLock(!lockRef.current)
        }}
        width={width}
        height={height}
    >
        <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 240 240">
            <path
                d={getDByLock(initlock)}
                ref={pathRef}
                data-lock={initlock}
                fill="white"
            />
        </svg>
    </svg>
}