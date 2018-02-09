//=========================================================================================
//-------------------------------------SOME METHODS----------------------------------------
//=========================================================================================

//array of functions which take frameNumber.
var neonAnimations = [];
var lastFrameNum = 0;
function neonAnimate(frameNumber){
  //console.log(frameNumber);
  for (var i=0; i<neonAnimations.length; i++){
    neonAnimations[i](frameNumber);
  }
}

function dimMaterial(material, amount){
  material.emissiveIntensity = material.emissiveIntensity*amount;
  material.needsUpdate = true;
}

function dimLight(light,amount){
  light.intensity = light.intensity*amount;
}

function dimLights(object, amount){
  object.traverse( function(child) {
    if (child instanceof THREE.PointLight) {
      dimLight(child, amount);
    }
  });
}

function switchNeonTex(mat1, mat2){
  var temp = mat1.emissiveMap;
  mat1.emissiveMap = mat2.emissiveMap;
  mat2.emissiveMap = temp;
  mat1.needsUpdate;
  mat2.needsUpdate;
}

//loader and constructor for external neon shapes.
function loadNeon(object3d,material,model) {
  var neonLoader = new THREE.OBJLoader();
  neonLoader.load( model, function ( object ) {
    object.traverse( function ( child ) {
      if ( child instanceof THREE.Mesh ) {
        child.material = material;
      }
    });
    object3d.add( object );
  });
}

function mixColors(colors) {
  //mkae sure colors is an array
  colors = [].concat( colors );

  var result = new THREE.Color(colors[0]);
  for (var i=1; i<colors.length; i++) {
    var temp = new THREE.Color(colors[i]);
    result.add(temp);
  }
  return result;
}

var testSphere = new THREE.Mesh( new THREE.SphereGeometry( 0.05, 32, 32 ), new THREE.MeshBasicMaterial( {color: 0xffffff} ));

function makeNeonPoints(object, colors, startPos, width, height, number, intensity, distance, testSphere) {
  if (number < 1) {number = 1;}

  //base light
  var mixColor = mixColors( colors );
  var ptLight = new THREE.PointLight( mixColor, intensity, distance );
  ptLight.position.copy( startPos );
  object.add( ptLight );

  //add new lights along a line between startPos and (width,startPos.y,height).
  for ( var i=1; i<number; i++ ) {
    var tempLight = ptLight.clone();
    tempLight.position.x = tempLight.position.x + ((width)/(number-1))*i;
    tempLight.position.z = tempLight.position.z - ((height)/(number-1))*i;
    object.add(tempLight);
  }

  //If only one light, set to average of startPos and endPos.
  if (number==1) {
    ptLight.position.x += width/2;
    ptLight.position.z -= height/2;
  }

  //testSpheres - for placment
  if (testSphere) {
    for ( var i=0; i<number; i++ ) {
      var tempSphere = new THREE.Mesh( new THREE.SphereGeometry( 0.05, 32, 32 ), new THREE.MeshBasicMaterial( {color: 0xffffff} ));
      tempSphere.position.copy( startPos );
      tempSphere.position.x = tempSphere.position.x + ((width)/(number-1))*i;
      tempSphere.position.z = tempSphere.position.z - ((height)/(number-1))*i;
      object.add(tempSphere);
    }
  }
}

function makeBacking(object,mat,startPos,width,height){
  var plane = new THREE.Mesh(
    new THREE.PlaneGeometry(width,height),
    mat
  );
  plane.rotation.x = Math.PI/2;
  plane.position.z += height/2;
  plane.position.x += width/2;
  plane.position.add(startPos);
  object.add(plane);
}

function makeNeonBorder(object, material, color, startPos, width, height, radius, light) {
  var left = new THREE.Mesh( new THREE.CylinderGeometry(radius, radius, height+(radius*1.6), 6), material );
  left.rotation.x = Math.PI/2;
  left.position.z += height/2;
  left.position.add(startPos);
  object.add(left);
  var right = left.clone();
  right.position.x += width;
  object.add(right);

  var bottom = new THREE.Mesh( new THREE.CylinderGeometry(radius, radius, width+(radius*1.6), 6), material );
  bottom.rotation.z = Math.PI/2;
  bottom.position.x += width/2;
  bottom.position.add(startPos);
  object.add(bottom);
  var top = bottom.clone();
  top.position.z += height;
  object.add(top);

  if (light){
    makeNeonPoints(object, color, startPos.add(new THREE.Vector3(width/5,0.1,height/5)), width*(4/5), height*(4/5), 1, 0.2, 10);
  }
}

function defaultNeonMaterial(color,augment){
  var white = new THREE.Color('white');
  if (augment!=undefined) {
    white.multiplyScalar(augment);
  }
  return new THREE.MeshLambertMaterial({
    color: color,
    //specular: color,
    emissive: mixColors([color,white]),
    emissiveIntensity: 0.9
  });
}

function defaultBackingMaterial(colors, texLoc){
  var color = mixColors(colors);
  var tex = new THREE.TextureLoader().load( texLoc );
  tex.flipY = false;
  return new THREE.MeshPhongMaterial({
    emissive: mixColors([color,0xffffff]),
    emissiveMap: tex,
    emissiveIntensity:0.6,
    color: 0xCCCCCC,
    side:THREE.DoubleSide,
  });
}
//=========================================================================================

//=========================================================================================
//--------------------------------------ACTUAL SIGNS---------------------------------------
//=========================================================================================

  var fruitSign = new THREE.Object3D();
  var fruitSignState = 0;
  var makeFruitSign = function(pos) {
    var redMat = defaultNeonMaterial('red');
    loadNeon(fruitSign,redMat,'models/neon/fruit_1.obj');

    //Rotate sign up.
    fruitSign.traverse( function ( child ) {
      if ( child instanceof THREE.Object3D ) {
        child.rotation.x = Math.PI;
      }
    });

    //Add siding, lights and backplate
    var redLights = new THREE.Object3D();
    fruitSign.add(redLights);
    makeNeonPoints(redLights, 'red', new THREE.Vector3(0.8,0.1,-0.3), 3, 0, 2, 0.3, 10);
    var blueMat = defaultNeonMaterial('blue');
    makeNeonBorder(fruitSign, blueMat, 'blue', new THREE.Vector3(-0.05,0,-0.85), 4.35, 1, 0.007, true);
    var backing1 = defaultBackingMaterial( ['red','blue'],'models/neon/fruit_1.png' );
    var backing2 = defaultBackingMaterial( 'blue','models/neon/fruit_2.png' );
    makeBacking(fruitSign,backing1,new THREE.Vector3(-0.05,-0.02,-0.85), 4.35, 1);

    //Define animation function. Blink the red part.
    neonAnimations.push( function(frameNumber) {
      var loopNumber = Math.floor(frameNumber*100)%200;
      if ((loopNumber>=100)&&(fruitSignState==0)) {
        dimMaterial(redMat,1/5);
        dimLights(redLights,1/10000);
        switchNeonTex(backing1, backing2);
        fruitSignState=1;
      }
      if ((loopNumber>=104)&&(fruitSignState==1)) {
        dimMaterial(redMat,5);
        dimLights(redLights,10000);
        switchNeonTex(backing1, backing2);
        fruitSignState=2;
      }
      if ((loopNumber>=150)&&(fruitSignState==2)) {
        dimMaterial(redMat,1/5);
        dimLights(redLights,1/10000);
        switchNeonTex(backing1, backing2);
        fruitSignState=3;
      }
      if ((loopNumber>=154)&&(fruitSignState==3)) {
        dimMaterial(redMat,5);
        dimLights(redLights,10000);
        switchNeonTex(backing1, backing2);
        fruitSignState=0;
      }
    });

    //Adjust position
    fruitSign.position.set(pos.x - 2.3,pos.y,pos.z + 0.15);
    scene.add( fruitSign );
  }

  var stirFrySign = new THREE.Object3D();
  var makeStirFrySign = function(pos) {
    var redMat = defaultNeonMaterial('red');
    loadNeon(stirFrySign,redMat,'models/neon/stirfry_text.obj');
    var greenMat = defaultNeonMaterial('green');
    loadNeon(stirFrySign,greenMat,'models/neon/stirfry_inborder.obj');
    loadNeon(stirFrySign,greenMat,'models/neon/stirfry_outborder.obj');

    //Rotate sign up.
    stirFrySign.traverse( function ( child ) {
      if ( child instanceof THREE.Object3D ) {
        child.rotation.x = Math.PI;
      }
    });

    var redLights = new THREE.Object3D();
    stirFrySign.add(redLights);
    makeNeonPoints(redLights, ['red','green'], new THREE.Vector3(0.4,0.1,-0.4), 3.3, 0, 1, 0.4, 10);
    //var greenLights = new THREE.Object3D();
    //stirFrySign.add(greenLights);
    //makeNeonPoints(greenLights, 'green', new THREE.Vector3(0.0,0.1,-0.4), 3.7, 0, 3, 0.3, 10);

    var backing = defaultBackingMaterial( ['red','green'],"models/neon/strifry_1.png" );
    makeBacking(stirFrySign,backing,new THREE.Vector3(-0.110,-0.02,-0.87), 3.972, 1.11);

    stirFrySign.position.set(pos.x - 1.9,pos.y,pos.z + 0.26);
    scene.add(stirFrySign);
  }

  var takeawaySign = new THREE.Object3D();
  var makeTakeawaySign = function(pos) {
    var yellowMat = defaultNeonMaterial('yellow');
    loadNeon(takeawaySign,yellowMat,'models/neon/takeaway_text.obj');
    var redMat = defaultNeonMaterial('red');
    loadNeon(takeawaySign,yellowMat,'models/neon/takeaway_border.obj');

    //Rotate sign up.
    takeawaySign.traverse( function ( child ) {
      if ( child instanceof THREE.Object3D ) {
        child.rotation.x = Math.PI;
      }
    });

    var yellowLights = new THREE.Object3D();
    takeawaySign.add(yellowLights);
    makeNeonPoints(yellowLights,['yellow','red'],new THREE.Vector3(0.16,0.1,-0.4),0,2,1,0.3,10);
    //var redLights = new THREE.Object3D();
    //takeawaySign.add(redLights);
    //makeNeonPoints(redLights,'red',new THREE.Vector3(0.16,0.1,-0.4),0,2,4,0.1,10);

    var backing = defaultBackingMaterial( ['red','yellow'],"models/neon/takeaway_1.png" );
    backing.emissiveIntensity = 0.5;
    makeBacking(takeawaySign,backing,new THREE.Vector3(-0.009,-0.02,-2.61), 0.341, 2.58);

    takeawaySign.position.set(pos.x-0.15,pos.y,pos.z-0.02);
    scene.add(takeawaySign);
  }
//=========================================================================================
