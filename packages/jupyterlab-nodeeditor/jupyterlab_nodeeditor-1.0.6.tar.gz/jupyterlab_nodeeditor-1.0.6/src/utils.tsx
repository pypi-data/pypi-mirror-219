
export function getStringPix(s, fontsize) {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d") as any;
    ctx.font = `${fontsize}px sans-serif`;
    const { width } = ctx.measureText(s);
    return width
}

export function buildNodeWidth(name, fontsize, minWidth, maxWidth) {
    let width = getStringPix(name, fontsize)
    width = width + fontsize * 5
    width = Math.max(width, minWidth)
    width = Math.min(width, maxWidth)
    return width
}

export function cloneDeep(obj: any): any {
    if (obj === null) return null;
    if (typeof obj !== 'object') return obj;

    let clone = Array.isArray(obj) ? [] : {};
    for (let key in obj) {
        clone[key] = cloneDeep(obj[key]);
    }
    return clone;
}

export function nextFrame() {
    return new Promise(resolve => {
        requestAnimationFrame(() => {
            resolve(null);
        });
    });
}

export function wait(ms: number) {
    return new Promise(resolve => {
        setTimeout(resolve, ms);
    });
}

export async function findAll(s: string, r: RegExp, checkFn: Function | null = null) {
    const result: [string, number, number, number, number][] = [];
    let m: RegExpExecArray | null;
    while (m = r.exec(s)) {
        if (checkFn && !await checkFn()) {
            return result
        }
        const match = m[0];
        const start = m.index;
        const end = start + match.length;
        const startLine = s.slice(0, start).split('\n').length;
        const startCol = start - s.lastIndexOf('\n', start - 1) - 1;
        const endLine = s.slice(0, end).split('\n').length;
        const endCol = end - s.lastIndexOf('\n', end - 1) - 1;

        result.push([match, startLine, startCol, endLine, endCol]);
    }

    return result;
}

export function getDuiJiaoZuoBiao(rect) {
    let x1 = Math.min(rect.x, rect.x + rect.width);
    let y1 = Math.min(rect.y, rect.y + rect.height);
    let x2 = Math.max(rect.x, rect.x + rect.width);
    let y2 = Math.max(rect.y, rect.y + rect.height);
    return { x1, x2, y1, y2 }
}

export function rectsIntersect(rect1, rect2) {
    let duijiao1 = getDuiJiaoZuoBiao(rect1)
    let duijiao2 = getDuiJiaoZuoBiao(rect2)
    return duijiao1.x1 < duijiao2.x2
        && duijiao1.x2 > duijiao2.x1
        && duijiao1.y1 < duijiao2.y2
        && duijiao1.y2 > duijiao2.y1
}

export function removeAnsi(text: string): string {
    const ansiRegex = /[\u001B\u009B][[()#;?]*(?:[0-9]{1,4}(?:;[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]/g;
    return text.replace(ansiRegex, '');
}