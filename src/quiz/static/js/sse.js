const sse = new EventSource("/events/");

sse.addEventListener("update", async (e) => {
	let ev = JSON.parse(e.data);
	if (ev.type == "room_update") {
		console.log(`Changing rooms`);
		changeRoom();
	}
	else {
		console.log(`Got unrecognised event type: ${ev.type}`);
	}
});


const changeRoom = () => {
	window.location.reload(true);
}
