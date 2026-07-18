const sse = new EventSource("/events/");

sse.addEventListener("refresh", async (e) => {
	let ev = JSON.parse(e.data);
	if (ev.type == "room_change") {
		console.log("changing rooms");
		reloadPage();
	}
    else if (ev.type == "question_change") {
		console.log("changing questions");
        reloadPage();
    }
	else {
		console.log(`Got unrecognised event type: ${ev.type}`);
	}
});


const reloadPage = () => {
	window.location.reload(true);
}
