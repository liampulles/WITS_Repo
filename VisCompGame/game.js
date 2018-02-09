//Liam Pulles

//Create some basic shapes
  //makeFruitSign(new THREE.Vector3(0,0,2.2));
  makeStirFrySign(new THREE.Vector3(0,0,2.0));
  makeTakeawaySign(new THREE.Vector3(-2.2,0,2.0));
  makeStall1(new THREE.Vector3(-2.2,0,1.0));

  var texture = new THREE.TextureLoader().load( "textures/wood1_1.png" );
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set ( 40,40 );
  var floor = new THREE.Mesh(
    new THREE.PlaneGeometry( 100, 100 ),
    new THREE.MeshPhongMaterial({
      map: texture,
      color:0xffffff,
    })
  );
  floor.material.side = THREE.DoubleSide;
  floor.position.z = 0;
  scene.add( floor );

  var light = new THREE.AmbientLight( 0x101010 ); // soft white light
  scene.add( light );

  //var ptlight = new THREE.PointLight( 0xffffff, 3, 7 );
  //ptlight.position.z +=1;
	//scene.add( ptlight );

  camera.position.z = 0.5;
  camera.position.y = -1.5;
  camera.position.x = 0;
  camera.lookAt(stirFrySign.position);

animate();
