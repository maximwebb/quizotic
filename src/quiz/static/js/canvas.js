const canvas = document.querySelector("#cv");
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

const quantise = (x, y) => {
    return [(Math.round(x * (gridWidth/renderWidth))) * cellWidth, (Math.round(y * (gridHeight/renderHeight))) * cellHeight];
}

const getRGBA = (x, y) => {
    let data = ctx.getImageData(x, y, 1, 1).data;
    return JSON.stringify([data[0], data[1], data[2], data[3]]);
}


const draw = (e) => {
    const [x, y] = getXY(e);
    const [qX, qY] = quantise(x, y);

    
    let [w, h] = [cellWidth * brushWidth, cellHeight * brushWidth];
    while (prevX != qX || prevY != qY) {
        if (prevX == null || prevY == null) {
            [prevX, prevY] = [qX, qY];
        }
        if (Math.abs(prevX - qX) > 0) {
            prevX -= Math.sign(prevX - qX);
        }
        if (Math.abs(prevY - qY) > 0) {
            prevY -= Math.sign(prevY - qY);
        }

        ctx.fillRect(prevX - w/2, prevY - h/2, w, h);
    }


    [prevX, prevY] = [qX, qY];
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
    console.log("Clearing");
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
