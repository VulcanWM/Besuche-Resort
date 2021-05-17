AFRAME.registerComponent('floatie', {
  tick: function (time, timeDelta) {
    document.getElementById("floatie").setAttribute("position", "3.818 " + Math.sin(time * 0.002) * 0.1 + " -2.385")
		document.getElementById("floatie").setAttribute("rotation", 90 + Math.cos(time * 0.002) * 5 + " 0 0")
  }
});