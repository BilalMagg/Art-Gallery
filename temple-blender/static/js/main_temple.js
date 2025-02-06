let scene, camera, renderer, controls, modelGroup, shadowLight;

function init() {
    console.log("Initializing Three.js scene...");

    // Create Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a1a);  

    // Camera Setup (Adjust for better framing)
    camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.1, 100);
    camera.position.set(-15, 10, 30); 
    console.log("Camera position set.");

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, canvas: document.getElementById("threejs-canvas") });
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap; 
    renderer.setSize(window.innerWidth * 0.6, window.innerHeight);
    console.log("Renderer initialized.");

    // Lighting Setup
    const beigeTone = 0xD2B48C; 

    const ambientLight = new THREE.AmbientLight(beigeTone, 1.2);  
    scene.add(ambientLight);

    shadowLight = new THREE.DirectionalLight(beigeTone, 1.1);
    shadowLight.position.set(5, 15, 10);
    shadowLight.castShadow = true;
    shadowLight.shadow.mapSize.width = 4096; 
    shadowLight.shadow.mapSize.height = 4096;
    scene.add(shadowLight);

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

    // Model Group
    modelGroup = new THREE.Group();
    modelGroup.position.set(6.5, 20, 0);
    scene.add(modelGroup);

    // Load the 3D Model
    const loader = new THREE.GLTFLoader();
    loader.load("/static/models/animated-temple3.glb", function(gltf) {
        console.log("✅ 3D Model Loaded!");
        let model = gltf.scene;

        // Center model
        const box = new THREE.Box3().setFromObject(model);
        const center = box.getCenter(new THREE.Vector3());
        model.position.sub(center); 

        model.scale.set(1.3, 1, 1.3);
        modelGroup.add(model);

        model.traverse((child) => {
            if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
            }
        });

        // Animation Loop
        function animate() {
            requestAnimationFrame(animate);
            modelGroup.rotation.y += 0.002;  
            modelGroup.position.y = 3 + Math.sin(Date.now() * 0.002) * 0.4;  

            controls.update();
            renderer.render(scene, camera);
        }
        animate();
    }, undefined, function(error) {
        console.error("❌ Error loading model:", error);
    });

    // User Controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.rotateSpeed = 0.5;
}

window.onload = init;
