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

/**************************************************************************
** Emitter Handler **
***************************************************************************
    Any element with class 'emitter' will emit the event specified in the
    element's 'data-cs-emit' attribute. If the element also has the class
    'emitter-cmd' then a command event will be emitted instead with the
    command specified in the 'data-cs-emit' attribute.
**************************************************************************/
$('.emitter').on('click', (ev) => {
    const evElement = $(ev.currentTarget);
    const data = evElement.attr('data-cs-emit');
    if (typeof data === 'undefined') {
        console.error(`'data-cs-emit' undefined on emitter for '${evElement.text()}'`);
        return false;
    } else {
        if (evElement.hasClass('emitter-cmd')) {
            socket.emit('command', data);
            console.log(`An emitter sent command: '${data}'`);
            return false;
        } else {
            socket.emit(data);
            console.log(`An emitter sent event: '${data}'`);
            return false;
        }
    }
}).preventDefault();