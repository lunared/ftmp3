var Visualizer = function(player){
    var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    var audioSrc = audioCtx.createMediaElementSource(player);
    var analyser = audioCtx.createAnalyser();
    analyser.fftSize = 128;

    // Bind our analyser to the media element source.
    audioSrc.connect(analyser);
    audioSrc.connect(audioCtx.destination);

    var frequencyData = new Uint8Array(analyser.frequencyBinCount);
    var freqScale = 300;
    var svgHeight = 200;
    var svgWidth = 1200;
    var barPadding = 1;

    var svg = document.getElementById('visualizer');
    var SVGNS = "http://www.w3.org/2000/svg";
    // populate visualizer with bars
    var bars = []
    frequencyData.forEach(function(feq, i){
        var bar = document.createElementNS(SVGNS, 'rect');
        bar.setAttribute('x', i * (svgWidth / frequencyData.length));
        bar.setAttribute('width', svgWidth / frequencyData.length - barPadding);
        svg.appendChild(bar);
        bars.push(bar);
    });

    // Render the visualizer at 60fps
    var updateVisualizer = setInterval(function(){
        // Copy frequency data
        analyser.getByteFrequencyData(frequencyData);

        // Update visualizer with new data.
        frequencyData.forEach(function(feq, i){
        var bar = bars[i];
        bar.setAttribute('y', svgHeight - ((svgHeight / freqScale) * feq));
        bar.setAttribute('height', (svgHeight / freqScale) * feq);
        });
    }, 1000/30.0);
}