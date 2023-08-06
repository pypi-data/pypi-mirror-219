import React, { useState, useRef } from "react";
import ArrownIcon from "./arrownIcon";
// A simple component that displays an image and allows zooming in and out
function ImageViewer(props) {
    // The image source url
    const { src,
        startIndex = 0,
        maxScale = 100,
        minScale = 0.1
    } = props;

    const [index, setIndex] = useState(startIndex);
    const imgRef = useRef(null);
    const divRef = useRef(null);
    const scaling = useRef(false)
    const scaleStartMouseEvent = useRef<any>(null)

    // 判断src是字符串还是数组
    const isArray = Array.isArray(src);
    let urls = src
    if (!isArray) {
        urls = [src]
    }

    // The zoom level state
    const zoom = useRef(1)
    const prevZoom = useRef(zoom.current)
    const setZoom = (z: number) => {
        prevZoom.current = zoom.current
        zoom.current = z
        updateTransform()
    }

    // The image position state
    const position = useRef({ x: 0, y: 0 })
    function setPosition(pos) {
        position.current = pos
        updateTransform()
    }

    function updateTransform() {
        if (imgRef.current != null) {
            const element = imgRef.current as unknown as HTMLImageElement
            element.style.transform = `translate(${position.current.x}px, ${position.current.y}px) scale(${zoom.current})`
        }
    }

    const updateZoom = (newZoom, startMouseEvent) => {
        setZoom(newZoom);
        if (imgRef.current != null) {
            const element = imgRef.current as unknown as HTMLImageElement
            const pre = element.getBoundingClientRect()
            const zoomMousePosX = startMouseEvent.clientX
            const zoomMousePosY = startMouseEvent.clientY
            // 1.计算缩放前鼠标位置相对于图片中心的位置
            let imgCenterX = pre.x + pre.width / 2
            let imgCenterY = pre.y
            let offsetX = zoomMousePosX - imgCenterX
            let offsetY = zoomMousePosY - imgCenterY

            // 2.计算缩放后该位置应该在哪里
            let offsetXAfterZoom = offsetX / prevZoom.current * zoom.current
            let offsetYAfterZoom = offsetY / prevZoom.current * zoom.current

            // 3.计算应该移动多少
            let directX = offsetX - offsetXAfterZoom
            let directY = offsetY - offsetYAfterZoom

            // 4.设置position
            setPosition({
                x: position.current.x + directX,
                y: position.current.y + directY
            })
        }
    }

    // The drag state
    const handleWheel = (e: React.WheelEvent<HTMLImageElement>) => {
        const newZoom = filterScale(zoom.current + (e.deltaY < 0 ? 0.1 : -0.1))
        updateZoom(newZoom, e)
    }

    const filterScale = (factor) => {
        return Math.max(Math.min(factor, maxScale), minScale)
    }

    const dragging = useRef(false)
    const setDragging = (v) => {
        dragging.current = v
    }
    const startDrag = (e) => {
        setDragging(true);
        let element = imgRef.current as unknown as HTMLImageElement
        element.style.cursor = "grabbing";
        try {
            element.setPointerCapture(e.pointerId);
        } catch (error) {

        }
    }

    const stopDrag = (e) => {
        setDragging(false);
        let element = imgRef.current as unknown as HTMLImageElement
        element.style.cursor = "grab";
        try {
            element.releasePointerCapture(e.pointerId);
        } catch (error) {

        }
    }

    const handleMouseDown = (e) => {
        e.preventDefault();
        startDrag(e)
    };

    const handleMouseMove = (e) => {
        e.preventDefault();
        if (dragging.current) {
            setPosition({
                x: position.current.x + e.movementX,
                y: position.current.y + e.movementY,
            });
        }

        if (scaling.current) {
            if (!scaleStartMouseEvent.current) {
                scaleStartMouseEvent.current = e
            } else {
                let newZoom = filterScale(zoom.current + e.movementX * 0.01)
                updateZoom(newZoom, scaleStartMouseEvent.current)
            }
        }
    };

    const handleMouseUp = (e) => {
        e.preventDefault();
        stopDrag(e)
    };

    const initImageTranslateAndScale = () => {
        if (!(imgRef.current != null && divRef.current != null)) {
            return
        }
        let imgElement = imgRef.current as unknown as HTMLImageElement
        imgElement.style.transformOrigin = `50% 0`;
        setPosition({ x: 0, y: 0 })
        setZoom(1)
    }

    // 设置初始的缩放和位置
    const handleImageLoad = (e) => {
        initImageTranslateAndScale()
    }

    // 图片列表总长度
    const length = urls.length;
    const preImage = (e) => {
        setIndex(prevIndex => (prevIndex - 1 + length) % length)
    }

    const nextImage = (e) => {
        console.log(e)
        setIndex(prevIndex => (prevIndex + 1) % length)
    }

    function handleKeyDown(e: KeyboardEvent) {
        e.stopPropagation()
        e.preventDefault()
        switch (e.key) {
            case "a":
            case "ArrowLeft": {
                preImage(e)
            } break;
            case "d":
            case "ArrowRight": {
                nextImage(e)
            } break;
            case " ": {
                startDrag(e)
            } break;
            case "s": {
                scaling.current = true
            } break;
            case "g": {
                initImageTranslateAndScale()
            } break;
        }
    }

    function handleKeyUp(e: KeyboardEvent) {
        e.stopPropagation()
        e.preventDefault()
        switch (e.key) {
            case " ": {
                stopDrag(e)
            } break;
            case "s": {
                scaling.current = false
                scaleStartMouseEvent.current = null
            } break;
        }
    }

    React.useEffect(() => {
        document.addEventListener('keydown', handleKeyDown)
        document.addEventListener('keyup', handleKeyUp)
        return () => {
            document.removeEventListener('keydown', handleKeyDown)
            document.removeEventListener('keyup', handleKeyUp)
        }
    }, [])

    return (
        <div
            ref={divRef}
            style={{
                backgroundColor: "black",
                width: "100%",
                height: "100%",
                display:"flex",
                justifyContent:"center",
            }}
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
        >
            <img
                onWheel={handleWheel}
                src={urls[index]}
                alt="Image"
                ref={imgRef}
                onLoad={handleImageLoad}
            />
            <div style={{
                position: "absolute",
                left: 0,
                top: "calc(50% - 50px)"
            }} >
                <ArrownIcon onClick={preImage} width={"100px"} height={"100px"} />
            </div>
            <div style={{
                position: "absolute",
                right: 0,
                top: "calc(50% - 50px)"
            }}>
                <ArrownIcon onClick={nextImage} width={"100px"} height={"100px"} rotate="180deg" />
            </div>
        </div>

    );
}

export default ImageViewer;
