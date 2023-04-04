function titleCase(st) {
    return st.split(" ").reduce( (s, c) => s +""+(c.charAt(0).toUpperCase() + c.slice(1) +" "), '');
}

const socket = io("http://192.168.1.234:5050", {
    auth: {
        id: "webclient"
    }});

socket.on('connect', function () {
    return true;
});