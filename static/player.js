class FTMP3 {
    constructor() {
        this._shuffleList = Array.prototype.map.call(this._songElements, function() { return false });;
        var me = this;
        this.player.addEventListener('ended', function(){ me.next() });
        this.player.addEventListener('loadeddata', function(){ me._activateSong() });
        this.player.addEventListener('canplaythrough', this.player.play);
    }

    /// properties

    get _songElements() {
        return document.getElementsByClassName("song");
    }

    get player() {
        return document.getElementsByTagName("audio")[0];
    }

    get _titleElement() {
        return document.getElementById("title")
    }

    get title() {
        return this._titleElement.innerHTML;
    }

    set title(songTitle) {
        this._titleElement.innerHTML = songTitle;
    }

    get _coverElement() {    
        return document.getElementsByClassName("cover");
    }

    set cover(dataUrl) {
        this._coverElement[0].src = dataUrl;
        this._coverElement[1].src = dataUrl;
    }

    get activeSong() {
        return document.getElementsByClassName("song playing")[0];
    }

    set activeSong(index) {
        if (index == null) {
            return;
        }
        var self = this;
        var player = this.player;
        // update the shuffle list
        if (index instanceof HTMLElement) {
            var song = index;
            this.reshuffle();
            index = Array.prototype.indexOf.call(this._songElements, index);
            this._shuffleList[index] = true;
        } else {
            var song = this._songElements[index];
            this._shuffleList[index] = true;
        }
        //safely pause and load the new song
        setTimeout(function(){
            player.src = song.getAttribute('data-url');
            player.setAttribute('data-url', song.getAttribute('data-url'));
            self.cover = song.getAttribute('data-img');
            player.load();
        }, 150);
        // update the title on the interface
        this.title = song.getAttribute('data-title');
    }

    /**
     * Get a list of song indexes that haven't been played yet in the shuffle
     */
    get _notPlayed() {
        var notPlayed = [];
        for (var s in this._shuffleList) {
            if (!this._shuffleList[s]) {
                notPlayed.push(s);
            }
        }
        return notPlayed;
    }

    ///// CONTROLS 

    get _controls() {
        return document.getElementById("controls").elements;
    }

    get _repeatElement() {
        return this._controls['repeat']
    }

    get repeatMode() {
        return this._repeatElement.value;
    }

    get _shuffleElement() {
        return this._controls['shuffle'];
    }

    get shuffle() {
        return this._shuffleElement.checked;
    }

    get autoplay() {
        return this._controls['autoplay'].checked;
    }

    /**
     * Disables all controls if autoplay is turned off
     */
    toggleControls() {
        this._shuffleElement.disabled = !this.autoplay;
        for (var r of this._repeatElement) {
            r.disabled = !this.autoplay;
        }
    }

    /**
     * Marks all songs as playable again in the smart shuffle
     */
    reshuffle() {
        this._shuffleList.fill(false);
    }

    /**
     * Get a song from the list that hasn't been played yet this cycle
     * pops the song by index from the shuffle and returns a new one
     */
    _smartShuffle(index) {
        var available = this._notPlayed;
        if (available.length == 0 && this.repeatMode == "all") {
            this.reshuffle();
            available = this._notPlayed;
        }
        if (available.length > 0) {
            return available[Math.floor(Math.random() * available.length)];
        }
        return null;
    }

    /**
     * Plays the next track.  Invoked when a song is over and autoplay is enabled
     */
    next() {
        if (this.player.src && this.autoplay) {
            var active = Array.prototype.indexOf.call(this._songElements, this.activeSong);
            var nextSong;
            if (this.repeatMode == "one") {
                this.player.play();
            }
            else if (!this.shuffle) {
                var next = active + 1;
                if (this.repeatMode == "all") {
                    next %= this._songElements.length;
                }
                else if (next > this._songElements.length) {
                    return;
                }
                nextSong = next;
            }
            else {
                nextSong = this._smartShuffle(active);
            }
            this.activeSong = nextSong;
        }
    }

    _activateSong(){
        // only play once we know we can
        for (var s of this._songElements) {
            s.classList.remove("playing");
            if (this.player.getAttribute('data-url') == s.getAttribute('data-url')) {
                s.classList.add("playing");
            }
        }
    };
}