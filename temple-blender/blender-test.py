from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Floating 3D Temple</title>

    <!-- Load Three.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three/examples/js/loaders/GLTFLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three/examples/js/controls/OrbitControls.js"></script>

    <style>
        body { margin: 0; overflow: hidden; background-color: black; }
        canvas { display: block; }
    </style>
</head>
<body>
    <script>
        let scene, camera, renderer, controls, model, softShadowLight;

        function init() {
            console.log("Initializing Three.js scene...");

            // Create Scene
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x222222);  // Dark gray background

            // Camera Setup
            camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
            camera.position.set(0, 5, 15);
            console.log("Camera position set.");

            // Renderer
            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.shadowMap.enabled = true; // Enable Shadows
            renderer.shadowMap.type = THREE.PCFSoftShadowMap; // Softer shadows
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);
            console.log("Renderer initialized.");

            // 🌟 Balanced Lighting Setup 🌟

            // 1️⃣ Ambient Light (Soft overall light)
            const ambientLight = new THREE.AmbientLight(0xBFB5A1, 2.5);  
            scene.add(ambientLight);

            // 2️⃣ Directional Light (Front) - Simulating Sunlight
            const frontLight = new THREE.DirectionalLight(0xA99E8B, 2.2);
            frontLight.position.set(5, 8, 10);
            frontLight.castShadow = true;
            scene.add(frontLight);

            // 3️⃣ Directional Light (Back) - Soft Glow
            const backLight = new THREE.DirectionalLight(0xA99E8B, 1.5);
            backLight.position.set(-5, 6, -10);
            scene.add(backLight);

            // 4️⃣ Side Lights (Low Intensity) - Avoids Dark Side Areas
            const leftLight = new THREE.PointLight(0xBFB5A1, 1.0, 50);  
            leftLight.position.set(-10, 4, 0);
            scene.add(leftLight);

            const rightLight = new THREE.PointLight(0xBFB5A1, 1.0, 50);  
            rightLight.position.set(10, 4, 0);
            scene.add(rightLight);

            // 5️⃣ Bottom Soft Light - Gentle upward glow
            const bottomLight = new THREE.PointLight(0xA99E8B, 1.5, 50);
            bottomLight.position.set(0, -3, 5);
            scene.add(bottomLight);

            // 6️⃣ **Soft Moving Shadow Light**
            softShadowLight = new THREE.DirectionalLight(0xA99E8B, 0.8); // Very soft
            softShadowLight.position.set(3, 10, 5);
            softShadowLight.castShadow = true;
            softShadowLight.shadow.mapSize.width = 2048;  // High-quality shadow resolution
            softShadowLight.shadow.mapSize.height = 2048;
            softShadowLight.shadow.camera.near = 0.1;
            softShadowLight.shadow.camera.far = 50;
            softShadowLight.shadow.blurSamples = 8;  // Extra soft shadow edges
            scene.add(softShadowLight);

            console.log("Lighting setup completed.");

            // Load the 3D Model
            const loader = new THREE.GLTFLoader();
            loader.load("/static/animated-temple2.glb", function(gltf) {
                console.log("✅ 3D Model Loaded!");
                model = gltf.scene;
                scene.add(model);

                // Enable Shadows for Depth
                model.traverse((child) => {
                    if (child.isMesh) {
                        child.castShadow = true;
                        child.receiveShadow = true;
                    }
                });

                // Animate Model (Floating + Rotation + Slow Moving Shadows)
                function animate() {
                    requestAnimationFrame(animate);
                    model.rotation.y += 0.001;  // Slower rotation
                    model.position.y = Math.sin(Date.now() * 0.0003) * 0.4;  // Smoother floating effect

                    // 🟢 **Soft Moving Light for Subtle Shadow Changes (Super Slow)**
                    softShadowLight.position.x = Math.sin(Date.now() * 0.00002) * 3; // Extremely slow
                    softShadowLight.position.z = Math.cos(Date.now() * 0.00002) * 3;

                    controls.update();
                    renderer.render(scene, camera);
                }
                animate();
            }, undefined, function(error) {
                console.error("❌ Error loading model:", error);
            });

            // Controls (User Interaction)
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.rotateSpeed = 0.5;
        }

        window.onload = init;
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)