//Make the scene, camera, renderer:
  var scene = new THREE.Scene();

    var FOV = 75;
    var ASPECT = window.innerWidth / window.innerHeight;
    var NEAR = 0.1;
    var FAR = 1000;
  var camera = new THREE.PerspectiveCamera( FOV, ASPECT, NEAR, FAR );

  var renderer = new THREE.WebGLRenderer({antialias: true});
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild( renderer.domElement );

    // CONTROLS
    var clock = new THREE.Clock(true);
    var controls = new THREE.TrackballControls( camera );
    controls.rotateSpeed = 0.6;
    controls.zoomSpeed = 0.1;
    controls.panSpeed = 0.2;
    controls.noZoom = false;
    controls.noPan = false;
    controls.staticMoving = false;
    controls.dynamicDampingFactor = 0.15;
    controls.keys = [ 65, 83, 68 ];

    function animate()
    {
      requestAnimationFrame( animate );
      update();
      render();
    }

    function update()
    {
    	neonAnimate(clock.getElapsedTime());

    	controls.update();
    }

    function render() {
      renderer.render( scene, camera );
    }
