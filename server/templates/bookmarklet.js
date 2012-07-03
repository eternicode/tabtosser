(function(){

var
    /* Saving a few bytes */
    w = window,
    ax = w.ActiveXObject,

    G = 'GET', P = 'POST', U = 'PUT', D = 'DELETE',

    settings = {
        api: "{{ host }}",
        id: "{{ location }}"
    },

    XMLHttpFactories = [
        function () {return new w.XMLHttpRequest()},
        function () {return new ax("Msxml2.XMLHTTP")},
        function () {return new ax("Msxml3.XMLHTTP")},
        function () {return new ax("Microsoft.XMLHTTP")}
    ];

function _XMLHttpRequest() {
    for (var i=0;i<XMLHttpFactories.length;i++) {
        try {
            return XMLHttpFactories[i]();
        }
        catch (e) {
            continue;
        }
    }
    return false;
}

function get_locations(){
    var x = _XMLHttpRequest();
    x.open(G, settings.api+'locations/', false);
    x.send();
    if (x.status == 200){
        var json = JSON.parse(x.responseText);
        return json;
    }
}

function Location(id){
    this.id = id;
    this.url = settings.api+'locations/'+this.id;
}
Location.prototype = {
    put: function(d){
        var s = [];
        for (var k in d)
            s.push(k + '=' + escape(d[k]));
        s = s.join('&')
        var x = _XMLHttpRequest();
        x.open(U, this.url, false);
        x.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        x.send(s);
    },
    save: function(url){
        this.put({add: url});
    },
    remove: function(url){
        this.put({remove: url});
    },
    list: function(){
        var x = _XMLHttpRequest();
        x.open(G, this.url, false);
        x.send();
        if (x.status == 200){
            var json = JSON.parse(x.responseText);
            return json;
        }
    }
}

function eventFire(el, etype){
  if (el.fireEvent) {
    (el.fireEvent('on' + etype));
  } else {
    var evObj = document.createEvent('Events');
    evObj.initEvent(etype, true, false);
    el.dispatchEvent(evObj);
  }
}

var a = prompt('"send" or "sync"?');
if (a == 'send'){
    var ls = get_locations();
    if (ls && ls.length){
        var p = 'Choose a destination: ' + ls.join(', ');
        var l = prompt(p);
        l = new Location(l);
        l.save(String(document.location));
    }
    else {
        alert('No locations available.');
    }
}
else if (a == 'sync'){
    var l = new Location(settings.id);
    var us = l.list();
    if (us && us.length){
        var p = 'Choose page:\n'
        for (var i=0; i<us.length; i++)
            p += i+': '+us[i]+'\n';
        var u = prompt(p);
        u = parseInt(u)
        if (!isNaN(u) && us.length > u){
            open(us[u], '_blank')
            l.remove(us[u]);
        }
    }
    else{
        alert('No pages to sync.');
    }
}

}());
