import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff);
scene.fog = new THREE.Fog(0xffffff, 12, 30);

const camera = new THREE.PerspectiveCamera(
	45,
	window.innerWidth / window.innerHeight,
	0.1,
	100,
);
camera.position.set(-1, 5.5, -7.5);

const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.5;
document.body.appendChild(renderer.domElement);

const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(window.innerWidth, window.innerHeight);
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.top = '0';
labelRenderer.domElement.style.pointerEvents = 'none';
document.body.appendChild(labelRenderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.target.set(0, 0, 0);
controls.minDistance = 4;
controls.maxDistance = 24;

const ambientLight = new THREE.AmbientLight(0xffffff, 0.95);
scene.add(ambientLight);

const pointLight = new THREE.PointLight(0xbfe7ff, 60, 80, 1.6);
pointLight.position.set(5, 9, 6);
scene.add(pointLight);

const secondaryLight = new THREE.PointLight(0xffd9b3, 18, 60, 2);
secondaryLight.position.set(-6, 4, -5);
scene.add(secondaryLight);

function potentialEnergy(x, z) {
	// A much shallower bowl so the edges don't skyrocket
	const bowl = 0.34 * (x * x + z * z);

	// Deeper, wider global minimum
	const globalWell = -2.5 * Math.exp(-(((x + 2) ** 2) / 1.2 + ((z + 2) ** 2) / 1.2));

	// Sharper local minimum
	const localWell = -1.5 * Math.exp(-(((x - 2) ** 2) / 0.8 + ((z - 2) ** 2) / 0.8));

	// A central "mountain" creating a saddle point between the two wells
	const mountain = 1.2 * Math.exp(-(x ** 2 + z ** 2) / 1.5);

	return bowl + globalWell + localWell + mountain;
}

function buildSurfaceGeometry() {
	const geometry = new THREE.PlaneGeometry(4.5, 4.5, 30, 30);
	const positions = geometry.attributes.position;
	const colors = [];
	let minHeight = Infinity;
	let maxHeight = -Infinity;

	for (let i = 0; i < positions.count; i += 1) {
		const x = positions.getX(i);
		const z = positions.getY(i);
		const y = potentialEnergy(x, -z);
		positions.setZ(i, y);
		minHeight = Math.min(minHeight, y);
		maxHeight = Math.max(maxHeight, y);
	}

	for (let i = 0; i < positions.count; i += 1) {
		const y = positions.getZ(i);
		const t = THREE.MathUtils.clamp((y - minHeight) / (maxHeight - minHeight), 0, 1);
		const color = new THREE.Color();
		color.setHSL(0.666 - 0.666 * t, 0.90, 0.36 + 0.18 * t);
		colors.push(color.r, color.g, color.b);
	}

	geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
	geometry.computeVertexNormals();
	geometry.rotateX(-Math.PI / 2);

	return geometry;
}

const surfaceGeometry = buildSurfaceGeometry();

const surfaceMaterial = new THREE.MeshStandardMaterial({
	vertexColors: true,
	roughness: 0.4,
	metalness: 0.2,
	flatShading: false,
});

const surface = new THREE.Mesh(surfaceGeometry, surfaceMaterial);
scene.add(surface);

const wireframe = new THREE.LineSegments(
	new THREE.WireframeGeometry(surfaceGeometry),
	new THREE.LineBasicMaterial({
		color: 0x333333,
		transparent: true,
		opacity: 0.4,
	}),
);
wireframe.position.y = 0.01;
scene.add(wireframe);

// Create topography map plane
const topoCanvas = createTopographyMap();
const topoTexture = new THREE.CanvasTexture(topoCanvas);
topoTexture.magFilter = THREE.LinearFilter;
topoTexture.minFilter = THREE.LinearFilter;

const topoPlaneGeometry = new THREE.PlaneGeometry(4.5, 4.5);
const topoPlaneMaterial = new THREE.MeshStandardMaterial({
	map: topoTexture,
	roughness: 0.8,
	metalness: 0.1,
	side: THREE.FrontSide,
});

const topoPlane = new THREE.Mesh(topoPlaneGeometry, topoPlaneMaterial);
topoPlane.rotation.x = -Math.PI / 2;
topoPlane.position.y = -2.8;
scene.add(topoPlane);

function createTopographyMap() {
	const canvas = document.createElement('canvas');
	canvas.width = 2000;
	canvas.height = 2000;
	const ctx = canvas.getContext('2d');
	const imageData = ctx.createImageData(canvas.width, canvas.height);
	const data = imageData.data;

	// Sample the surface and find min/max heights
	let minHeight = Infinity;
	let maxHeight = -Infinity;

	const samples = {};
	for (let py = 0; py < canvas.height; py++) {
		for (let px = 0; px < canvas.width; px++) {
			const x = (px / canvas.width) * 4.5 - 2.25;
			const z = (py / canvas.height) * 4.5 - 2.25;
			const y = potentialEnergy(x, z);
			minHeight = Math.min(minHeight, y);
			maxHeight = Math.max(maxHeight, y);
			samples[`${px},${py}`] = y;
		}
	}

	// Create heatmap by coloring based on height
	for (let py = 0; py < canvas.height; py++) {
		for (let px = 0; px < canvas.width; px++) {
			const idx = (py * canvas.width + px) * 4;
			const y = samples[`${px},${py}`];
			const t = (y - minHeight) / (maxHeight - minHeight);
			const hue = 0.666 - 0.666 * t;
			const rgb = hslToRgb(hue, 0.90, 0.36 + 0.18 * t);

			data[idx] = rgb[0];
			data[idx + 1] = rgb[1];
			data[idx + 2] = rgb[2];
			data[idx + 3] = 255;
		}
	}

	ctx.putImageData(imageData, 0, 0);

	// Draw contour lines
	ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
	ctx.lineWidth = 1;
	const contourStep = (maxHeight - minHeight) / 10;

	for (let contourLevel = minHeight; contourLevel < maxHeight; contourLevel += contourStep) {
		ctx.beginPath();
		let first = true;

		for (let angle = 0; angle < Math.PI * 2; angle += 0.01) {
			for (let radius = 0; radius < 3; radius += 0.1) {
				const x = Math.cos(angle) * radius;
				const z = Math.sin(angle) * radius;
				const y = potentialEnergy(x, -z);

				if (Math.abs(y - contourLevel) < contourStep * 0.2) {
					const px = ((x + 2.25) / 4.5) * canvas.width;
					const py = ((z + 2.25) / 4.5) * canvas.height;

					if (first) {
						ctx.moveTo(px, py);
						first = false;
					} else {
						ctx.lineTo(px, py);
					}
				}
			}
		}
		ctx.stroke();
	}

	// Draw grid
	ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
	ctx.lineWidth = 1;
	for (let i = 0; i <= 9; i++) {
		const x = (i / 9) * canvas.width;
		ctx.beginPath();
		ctx.moveTo(x, 0);
		ctx.lineTo(x, canvas.height);
		ctx.stroke();

		const y = (i / 9) * canvas.height;
		ctx.beginPath();
		ctx.moveTo(0, y);
		ctx.lineTo(canvas.width, y);
		ctx.stroke();
	}

	return canvas;
}

function hslToRgb(h, s, l) {
	const c = (1 - Math.abs(2 * l - 1)) * s;
	const x = c * (1 - Math.abs((h * 6) % 2 - 1));
	const m = l - c / 2;
	let r, g, b;
	if (h < 1 / 6) {
		[r, g, b] = [c, x, 0];
	} else if (h < 2 / 6) {
		[r, g, b] = [x, c, 0];
	} else if (h < 3 / 6) {
		[r, g, b] = [0, c, x];
	} else if (h < 4 / 6) {
		[r, g, b] = [0, x, c];
	} else if (h < 5 / 6) {
		[r, g, b] = [x, 0, c];
	} else {
		[r, g, b] = [c, 0, x];
	}
	return [
		Math.round((r + m) * 255),
		Math.round((g + m) * 255),
		Math.round((b + m) * 255),
	];
}

function surfacePoint(x, z) {
	return new THREE.Vector3(x, potentialEnergy(x, -z), -z);
}

function makeLabel(text, background, borderColor) {
	const element = document.createElement('div');
	element.textContent = text;
	element.style.padding = '5px 9px';
	element.style.borderRadius = '999px';
	element.style.background = background;
	element.style.border = `1px solid ${borderColor}`;
	element.style.color = '#f7fcff';
	element.style.font = '600 12px/1.2 system-ui, sans-serif';
	element.style.letterSpacing = '0.02em';
	element.style.whiteSpace = 'nowrap';
	element.style.boxShadow = '0 0 18px rgba(0, 0, 0, 0.35)';
	return element;
}

function addMarker(position, color, labelText, background, borderColor) {
	const group = new THREE.Group();
	group.position.copy(position);

	const sphere = new THREE.Mesh(
		new THREE.SphereGeometry(0.08, 24, 24),
		new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: 0.35, roughness: 0.35 }),
	);
	sphere.position.y += 0.04;
	group.add(sphere);

	const halo = new THREE.Mesh(
		new THREE.SphereGeometry(0.18, 24, 24),
		new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.14 }),
	);
	group.add(halo);

	const label = new CSS2DObject(makeLabel(labelText, background, borderColor));
	label.position.set(0, 0.35, 0);
	group.add(label);

	scene.add(group);
	return group;
}

// Re-centered coordinates based on the 0.34 bowl strength
const globalMin = surfacePoint(-1.78, 1.78); 
const localMin = surfacePoint(1.62, -1.62);    
const localMax = surfacePoint(0.0, 0.0);
const saddle = surfacePoint(0.0, -1.15);

addMarker(globalMin, 0x3cff7b, 'Global Min', 'rgba(42, 122, 63, 0.75)', 'rgba(100, 255, 156, 0.95)');
addMarker(localMin, 0xff5b5b, 'Local Min', 'rgba(128, 36, 36, 0.78)', 'rgba(255, 130, 130, 0.95)');
addMarker(localMax, 0xffffff, 'Local Max', 'rgba(100, 100, 100, 0.78)', 'rgba(200, 200, 200, 0.95)');
addMarker(saddle, 0xffd84d, 'Saddle Point', 'rgba(124, 101, 25, 0.8)', 'rgba(255, 222, 120, 0.95)');

const pathCoords = [
    {x: -2,   z: -2},   // High corner start
    {x: -1.5,   z: -1.8},   // Stepping down the ridge
    {x: -1,   z: -1.5}, // Approaching the center
    {x: -0.7,    z: -1.15},// Touching the Saddle Point area
    {x: -1, z: -0.75},  // Turning away from the mountain
    {x: -1.2, z: -0.3},  // Dropping into the deep well
    {x: -1.5, z: 0.7},  // Dropping into the deep well
    {x: -1.78, z: 1.78} // Final Global Min destination
];

// Map with a tiny "cushion" offset of 0.05
const pathPoints = pathCoords.map(coord => {
    return new THREE.Vector3(
        coord.x, 
		potentialEnergy(coord.x, -coord.z) + 0.05, 
		-coord.z
    );
});

const pathCurve = new THREE.CatmullRomCurve3(pathPoints, false, 'catmullrom', 0.5);

const haloTube = new THREE.Mesh(
	new THREE.TubeGeometry(pathCurve, 160, 0.1, 16, false),
	new THREE.MeshBasicMaterial({ color: 0x4d6b55, transparent: true, opacity: 0.12 }),
);
scene.add(haloTube);

const coreTube = new THREE.Mesh(
	new THREE.TubeGeometry(pathCurve, 160, 0.045, 16, false),
	new THREE.MeshStandardMaterial({
		color: 0x55374C,
		emissive: 0x7bfc03,
		emissiveIntensity: 1.35,
		roughness: 0.25,
		metalness: 0.15,
	}),
);
scene.add(coreTube);

const pathGlow = new THREE.PointLight(0x101010, 18, 8, 2);
pathGlow.position.copy(pathCurve.getPoint(0.55));
scene.add(pathGlow);

function onWindowResize() {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize(window.innerWidth, window.innerHeight);
	labelRenderer.setSize(window.innerWidth, window.innerHeight);
}

window.addEventListener('resize', onWindowResize);

function animate() {
	requestAnimationFrame(animate);
	controls.update();

	const pulse = 1 + 0.1 * Math.sin(performance.now() * 0.002);
	pathGlow.intensity = 15 + 3 * pulse;
	haloTube.material.opacity = 0.1 + 0.03 * Math.sin(performance.now() * 0.0025);

	renderer.render(scene, camera);
	labelRenderer.render(scene, camera);
    // In your renderer setup:
}

animate();
