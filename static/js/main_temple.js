let scene, camera, renderer, controls, modelGroup, shadowLight;

function init() {
  console.log("Initializing Three.js scene...");

  // Scene with no background => transparent
  scene = new THREE.Scene();
  scene.background = null;

  // Camera Setup
  camera = new THREE.PerspectiveCamera(
    30,
    window.innerWidth / window.innerHeight,
    0.1,
    100
  );
  camera.position.set(-15, 10, 30);

  // Get canvas & container
  const canvas = document.getElementById("threejs-canvas");
  const container = document.querySelector(".model-container");

  // Renderer with alpha for transparency
  renderer = new THREE.WebGLRenderer({
    antialias: true,
    canvas: canvas,
    alpha: true
  });
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  // Match container's size
  renderer.setSize(container.clientWidth, container.clientHeight);

  // ===== Lighting Setup =====
  const beigeTone = 0xd2b48c;

  // Ambient Light
  const ambientLight = new THREE.AmbientLight(beigeTone, 1.2);
  scene.add(ambientLight);

  // Directional Light for shadows
  shadowLight = new THREE.DirectionalLight(beigeTone, 1.1);
  shadowLight.position.set(5, 15, 10);
  shadowLight.castShadow = true;
  shadowLight.shadow.mapSize.width = 4096;
  shadowLight.shadow.mapSize.height = 4096;
  scene.add(shadowLight);

  // Additional Lights
  const frontLight = new THREE.DirectionalLight(beigeTone, 0.9);
  frontLight.position.set(0, 8, 15);
  scene.add(frontLight);

  const rightLight = new THREE.PointLight(beigeTone, 0.8, 50);
  rightLight.position.set(12, 6, 5);
  scene.add(rightLight);

  const backLight = new THREE.DirectionalLight(beigeTone, 0.9);
  backLight.position.set(-5, 10, -15);
  scene.add(backLight);

  const leftLight = new THREE.PointLight(beigeTone, 0.8, 50);
  leftLight.position.set(-12, 6, 0);
  scene.add(leftLight);

  // ===== Here's an extra bright white light to make the temple brighter =====
  const brightLight = new THREE.DirectionalLight(0xffffff, 1.5);
  brightLight.position.set(10, -20, 10);
  scene.add(brightLight);

  // Model Group
  modelGroup = new THREE.Group();
  scene.add(modelGroup);

  // Load the 3D Model
  const loader = new THREE.GLTFLoader();
  loader.load("/static/models/animated-temple3.glb", (gltf) => {
    console.log("✅ 3D Model Loaded!");
    const model = gltf.scene;

    // Center the model
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    model.position.sub(center);

    // ===== Scale the model =====
    // Tweak these numbers to make it smaller or bigger:
    model.scale.set(1.36, 0.85, 1.36);

    // ===== Position the model =====
    // For example, move it up or sideways by changing these:
    model.position.y += 5;   // or 2, 5, etc.
    //model.position.x += -4.6;   // or -3, etc. 

    modelGroup.add(model);

    // Cast/receive shadows
    model.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;
      }
    });

    animate();
  }, undefined, (error) => {
    console.error("❌ Error loading model:", error);
  });

  // Orbit Controls so you can drag/rotate the camera
  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.rotateSpeed = 0.5;

  // Handle resizing
  window.addEventListener("resize", onWindowResize);
}

function animate() {
  requestAnimationFrame(animate);

  if (modelGroup) {
    // Slowly rotate model
    modelGroup.rotation.y += 0.002;

    // Bob the model up and down
    modelGroup.position.y = Math.sin(Date.now() * 0.002) * 0.1;
    modelGroup.position.x = Math.sin(Date.now() * 0.002) * 0.1;
    modelGroup.position.z = Math.sin(Date.now() * 0.002) * 0.1;
  }

  controls.update();
  renderer.render(scene, camera);
}

function onWindowResize() {
  const container = document.querySelector(".model-container");
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
}

// Start the scene on page load
window.onload = init;