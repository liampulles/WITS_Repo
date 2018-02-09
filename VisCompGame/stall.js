
function loadTexObj(obj3d, mtlName, objName) {
  THREE.Loader.Handlers.add( /\.dds$/i, new THREE.DDSLoader() );
	var mtlLoader = new THREE.MTLLoader();
	mtlLoader.load( mtlName, function( materials ) {
		materials.preload();
		var objLoader = new THREE.OBJLoader();
		objLoader.setMaterials( materials );
		objLoader.load( objName, function ( object ) {
			obj3d.add(object);
		});
	});
}

function stackObj(object, mtlName, objName, amount, height) {
  var startAng = 0;
  for (var i=0; i<amount; i++){
    var temp = new THREE.Object3D();
    loadTexObj(temp, mtlName, objName);
    temp.rotation.x = 3*Math.PI/2;
    temp.position.z = 11;
    temp.position.z += i*height;
    startAng = startAng + Math.random()*(Math.PI/4);
    temp.rotation.y = startAng;
    object.add( temp );
  }
}

  var stall1 = new THREE.Object3D() ;
  function makeStall1(pos){
    var boxstack1 = new THREE.Object3D() ;
    stackObj(boxstack1, 'models/stalls/plastic_crate.mtl', 'models/stalls/plastic_crate.obj', 2, 11);
    boxstack1.scale.multiplyScalar(0.05);
    stall1.add(boxstack1);
    var boxstack2 = new THREE.Object3D() ;
    stackObj(boxstack2, 'models/stalls/plastic_crate.mtl', 'models/stalls/plastic_crate.obj', 2, 11);
    boxstack2.scale.multiplyScalar(0.05);
    boxstack2.position.x += 3;
    stall1.add(boxstack2);
    var boxstack3 = new THREE.Object3D() ;
    stackObj(boxstack3, 'models/stalls/plastic_crate.mtl', 'models/stalls/plastic_crate.obj', 2, 11);
    boxstack3.scale.multiplyScalar(0.05);
    boxstack3.position.x += 3;
    boxstack3.position.y += 2;
    stall1.add(boxstack3);
    var boxstack4 = new THREE.Object3D() ;
    stackObj(boxstack4, 'models/stalls/plastic_crate.mtl', 'models/stalls/plastic_crate.obj', 2, 11);
    boxstack4.scale.multiplyScalar(0.05);
    boxstack4.position.y += 2;
    stall1.add(boxstack4);

    var pallet = new THREE.Object3D();
    loadTexObj(pallet, 'models/stalls/palette_euro_1200x800.mtl', 'models/stalls/palette_euro_1200x800.obj');
    pallet.position.z = 1.1;
    pallet.rotation.x = Math.PI/2;
    pallet.scale.multiplyScalar(2);
    stall1.add( pallet );

    //boxstack.traverse( function ( child ) {
    //  if ( child instanceof THREE.Object3D ) {
    //    child.rotation.x = 3*Math.PI/2;
    //  }
    //});

    //takeawaySign.position.set(pos.x-0.15,pos.y,pos.z-0.02);
    scene.add(stall1);
  }
