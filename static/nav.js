(function(){
    function switchTab() {
        var hash = location.hash.substr(1);
        var sections = document.getElementsByTagName("section");
        for (var s of sections) {
            s.classList.remove("visible");
            if (s.id == hash) {
                s.classList.add("visible");
            }
        }

        var tabs = document.getElementsByClassName("tab");
        for (var s of tabs) {
            s.classList.remove("active");
            if (s.attributes['href'] && s.attributes['href'].value == location.hash) {
                s.classList.add("active");
            }
        }

        if (!location.hash) {
            document.getElementsByTagName("section")[0].classList.add("visible");
            document.getElementsByClassName("tab")[0].classList.add("active");
        }
    }

    window.addEventListener("hashchange", switchTab, false);

    switchTab();
})()