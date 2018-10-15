class FTMP3 {
    constructor() {
        this._shuffleList = Array.prototype.map.call(this._songElements, function() { return false });
        var me = this;
        this.player.addEventListener('ended', function(){ me.next() });
        this.player.addEventListener('loadeddata', function(){ me._activateSong() });
        this.player.addEventListener('canplaythrough', this.player.play);
        this.player.addEventListener('timeupdate', function() { me._updateProgress() });
        this._playingIndex = -1;
        this._shuffleIndex = -1;
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
        if (this.shuffle) {
            if (index instanceof HTMLElement) {
                var song = index;
                this.reshuffle(false);
                index = Array.prototype.indexOf.call(this._shuffleList, index);
                this._shuffleList.pop(index);
                this._shuffleIndex = 0;
            } else {
                var song = this._shuffleList[index];
                this._shuffleIndex = index;
            }
        } else {
            if (index instanceof HTMLElement) {
                var song = index;
                this._index = Array.prototype.indexOf.call(this._songElements, index);
            } else {
                var song = this._songElements[index];
                this._index = index;
            }
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

    /**
     * Shuffles array in place.
     */
    reshuffle(inplace=true) {
        let a = Array.prototype.map.call(this._songElements, function(value) { return value });
        for (let i = a.length; i; i--) {
            let j = Math.floor(Math.random() * i);
            [a[i - 1], a[j]] = [a[j], a[i - 1]];
        }
        this._shuffleList = a;

        if (inplace) {
            let index = Array.prototype.indexOf.call(this._shuffleList, this.activeSong);
            this._shuffleList.pop(index);
            this._shuffleIndex = 0;
        }
    }

    /**
     * Plays the next track.
     */
    next(manual=false) {
        if (this.player.src) {
            var next;
            if (this.repeatMode == "one") {
                this.player.play();
                return;
            }
            
            if (!this.shuffle) {
                next = this._index + 1;
            }
            else {
                next = this._shuffleIndex + 1;
            }
            
            if (this.repeatMode == "all") {
                if (this.shuffle && next >= this._songElements.length) {
                    this.reshuffle(false);
                }
                next %= this._songElements.length;
            }
            else if (next > this._songElements.length) {
                return;
            }
            
            this.activeSong = next;
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

    /**
     * Toggles play and pause of the current song
     */
    play() {
        if (this.player.src) {
            if (!this.player.paused) {
                this.player.pause();
            } else {
                this.player.play();
            }
        }
    }

    /**
     * Seeks to a specified percentage into the song
     */
    skip(progress) {
        if (this.player.src) {
            this.player.currentTime = this.player.duration * progress;
            this.player.play();
        }
    }

    _updateProgress() {
        let progress = this.player.currentTime / this.player.duration;

        let es = document.getElementById("Progress").querySelectorAll('.meter');
        for (let i = 0, n = 0; i < es.length; i++, n = i / es.length) {
            if (progress > n) {
                es[i].classList.add('at');
            } else {
                es[i].classList.remove('at');
            }
        }

        document.getElementById("Playback").querySelector('label[name="time"]').textContent = 
            String("00" + Math.trunc(this.player.currentTime / 60)).slice(-2) + ":" +
            String("00" + Math.trunc(this.player.currentTime % 60)).slice(-2);
    }
}