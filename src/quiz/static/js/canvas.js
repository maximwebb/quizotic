const canvas = document.querySelector("#cv");
canvas.width = canvas.clientWidth;
canvas.height = canvas.clientHeight;
const ctx = canvas.getContext("2d");
const [gridWidth, gridHeight] = [100, 100];
const [renderWidth, renderHeight] = [canvas.width, canvas.height];
const [cellWidth, cellHeight] = [renderWidth/gridWidth, renderHeight/gridHeight];

const Mode = {
    BRUSH: "brush",
    FILL: "fill",
    from_str(s) {
        if (s == Mode.BRUSH) {
            return Mode.BRUSH;
        }
        else if (s == Mode.FILL) {
            return Mode.FILL;
        }
        return null;
    },
};


let brushWidth = 1;
let drawMode = Mode.BRUSH;

const widthSelect = document.querySelector("#lineWidth");
const colorSelect = document.querySelector("#lineColor");
const modeSelect = document.querySelector("#drawMode");

let [prevX, prevY] = [null, null];

const getXY = (e) => {
    const rect = canvas.getBoundingClientRect();
    return [(e.clientX - rect.left), (e.clientY - rect.top)];
}

const toGridXY = (x, y) => {
    return [Math.round(x * (gridWidth/renderWidth)), Math.round(y * (gridHeight/renderHeight))];
}

const quantise = (x, y) => {
    return [x * cellWidth, y* cellHeight];
}

const getRGBA = (x, y) => {
    let data = ctx.getImageData(x, y, 1, 1).data;
    return JSON.stringify([data[0], data[1], data[2], data[3]]);
}


const draw = async (e) => {
    let [x0, y0] = [prevX, prevY];
    const [x, y] = getXY(e);
    const [gridX, gridY] = toGridXY(x, y);
    
    let [w, h] = [cellWidth * brushWidth, cellHeight * brushWidth];
    let i = 0;
    while (x0 != gridX || y0 != gridY) {
        console.log([gridX, gridY]);
        i += 1;
        if (x0 == null || y0 == null) {
            [x0, y0] = [gridX, gridY];
        }
        if (Math.abs(x0 - gridX) > 0) {
            x0 -= Math.sign(x0 - gridX);
        }
        if (Math.abs(y0 - gridY) > 0) {
            y0 -= Math.sign(y0 - gridY);
        }

        let [qX, qY] = quantise(x0, y0);
        ctx.fillRect(qX - w/2, qY - h/2, w, h);
        // Uncomment for some fun visual effects!
        // await new Promise(r => setTimeout(r, 100));
    }


    [prevX, prevY] = [gridX, gridY];
}

const test = (x, y, init_rgb, buf) => {
    if (!(x >= 0 && x < canvas.width && y >= 0 && y < canvas.height)) {
        return false;
    }

    if (y in buf) {
        for (const [l, r] of buf[y]) {
            if (l <= x && x <= r) {
                return false;
            }
        }
    }

    let rgb = getRGBA(x, y);
    return init_rgb == rgb;
}

const bufferLine = (l, r, y, buf) => {
    if (!(y in buf)) {
        buf[y] = [];
    }
    buf[y].push([l, r]);
}

const drawLineBuffer = (buf) => {
    const path = new Path2D();

    for (const y in buf) {
        for (const [l, r] of buf[y]) {
            path.rect(l, y, r - l + 1, cellHeight);
        }
    }

    ctx.fill(path);
};

const fill = async (e) => {
    const [x0, y0] = getXY(e);
    fillInner(x0, y0);
}

const fillInner = async (x0, y0) => {
    let init_rgb = getRGBA(x0, y0);

    let to_visit = [[x0, y0]];
    let line_buf = {};
    let seen = new Set();
    let step = Math.floor(cellHeight / 2);

    const scan = (lx, rx, y, s) => {
        let in_span = false;
        for (let x = lx; x <= rx; x++) {
            if (!test(x, y, init_rgb, line_buf)) {
                in_span = false;
            }
            else if (!in_span) {
                to_visit.push([x, y]);
                in_span = true;
            }
        }
    };

    console.time('scan')
    while (to_visit.length > 0) {
        const [x, y] = to_visit.pop();

        let [lx, rx] = [x, x];

        while (test(lx-1, y, init_rgb, line_buf)) {
            lx -= cellWidth;
        }

        while (test(rx+1, y, init_rgb, line_buf)) {
            rx += cellWidth;
        }

        bufferLine(lx, rx, y, line_buf);
        // ctx.fillRect(lx, y, rx - lx + 1, 1);

        scan(lx, rx, y+step, to_visit);
        scan(lx, rx, y-step, to_visit);

        // await new Promise(r => setTimeout(r, 1));
    }
    console.timeEnd('scan')

    drawLineBuffer(line_buf);
}

const updateStroke = () => {
    ctx.fillStyle = document.querySelector('input[name="lineColor"]:checked').value;
    brushWidth = document.querySelector('input[name="lineWidth"]:checked').value;
    drawMode = document.querySelector('input[name="drawMode"]:checked').value;}

const clearCanvas = () => {
    let fill = ctx.fillStyle;
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = fill;
}

const onFinish = (e) => {
    [prevX, prevY] = [null, null];
    canvas.removeEventListener("mousemove", draw);
    canvas.removeEventListener("mouseup", onFinish);
}


canvas.addEventListener("mousedown", (e) => {
    if (drawMode == Mode.BRUSH) {
        canvas.addEventListener("mousemove", draw);
        canvas.addEventListener("mouseup", onFinish);
    }
    else if (drawMode == Mode.FILL) {
        fill(e);
    }
    else {
        console.log(`Invalid draw mode: ${drawMode}`);
    }
});


widthSelect.addEventListener("change", updateStroke);
colorSelect.addEventListener("change", updateStroke);
modeSelect.addEventListener("change", updateStroke);
clearCanvas();
