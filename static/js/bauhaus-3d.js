/**
 * ==============================================================================
 * BAUHAUS 3D ANIMATION ENGINE (Three.js)
 * Trekking Management Application
 * Form Follows Function • Topographic Alpine Geometry • Zero-Bug Architecture
 * ==============================================================================
 */

(function(window, document) {
    'use strict';

    // 1. WebGL Feature Detection
    function isWebGLAvailable() {
        try {
            var canvas = document.createElement('canvas');
            return !!(window.WebGLRenderingContext && 
                (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
        } catch (e) {
            return false;
        }
    }

    // 2. Reduced Motion Accessibility Detection
    function isReducedMotion() {
        return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    // 3. Theme Color Schemes
    var THEMES = {
        light: {
            bg: 0xF7F5EE,       // Bauhaus Canvas Cream
            canvasHex: '#F7F5EE',
            wire: 0x121212,     // Stark Ink Black
            wireSecondary: 0x1A365D, // Cobalt Blue
            accentRed: 0xD92525,     // Carmine Red
            accentYellow: 0xF6AE2D,  // Warm Chrome Yellow
            accentGreen: 0x2D6A4F,   // Alpine Green
            surface: 0xFFFFFF,
            facet: 0xEDE9DF,
            fog: 0xF7F5EE
        },
        dark: {
            bg: 0x0F0F12,       // Bauhaus Obsidian
            canvasHex: '#0F0F12',
            wire: 0xE63946,     // Neon Signal Red
            wireSecondary: 0x3A86FF, // Electric Cobalt
            accentRed: 0xFF4D5C,     // High-Vis Red
            accentYellow: 0xFFBE0B,  // Electric Yellow
            accentGreen: 0x06D6A0,   // Neon Mint Green
            surface: 0x18181D,
            facet: 0x15151B,
            fog: 0x0F0F12
        }
    };

    function getCurrentTheme() {
        var theme = document.documentElement.getAttribute('data-bs-theme') ||
                    document.documentElement.getAttribute('data-theme') ||
                    (window.localStorage && window.localStorage.getItem('bh-theme')) || 'light';
        return theme === 'dark' ? 'dark' : 'light';
    }

    // Global Registry
    var Bauhaus3D = {
        instances: [],
        currentTheme: getCurrentTheme(),

        register: function(inst) {
            this.instances.push(inst);
        },

        syncTheme: function(newTheme) {
            this.currentTheme = newTheme === 'dark' ? 'dark' : 'light';
            for (var i = 0; i < this.instances.length; i++) {
                if (typeof this.instances[i].updateTheme === 'function') {
                    try {
                        this.instances[i].updateTheme(this.currentTheme);
                    } catch (err) {
                        console.warn('Bauhaus3D theme update error:', err);
                    }
                }
            }
        }
    };

    // Auto-listen to HTML theme attribute changes
    if (window.MutationObserver) {
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.attributeName === 'data-bs-theme' || mutation.attributeName === 'data-theme') {
                    var updated = getCurrentTheme();
                    Bauhaus3D.syncTheme(updated);
                }
            });
        });
        observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-bs-theme', 'data-theme'] });
    }

    /* ==============================================================================
       MODULE 1: AMBIENT HERO MOUNTAIN TERRAIN (Auth & Landing Views)
       ============================================================================== */
    Bauhaus3D.initHeroTerrain = function(canvasId) {
        if (!isWebGLAvailable() || !window.THREE) return null;

        var canvas = document.getElementById(canvasId);
        if (!canvas) return null;

        var theme = getCurrentTheme();
        var colors = THEMES[theme];
        var reducedMotion = isReducedMotion();

        var scene = new THREE.Scene();
        scene.background = new THREE.Color(colors.bg);
        scene.fog = new THREE.Fog(colors.fog, 20, 95);

        var camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 10, 32);
        camera.lookAt(0, 2, 0);

        var renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            antialias: true,
            alpha: false,
            powerPreference: 'low-power'
        });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

        // Ambient & Directional Lighting
        var ambientLight = new THREE.AmbientLight(0xffffff, theme === 'dark' ? 0.7 : 0.9);
        scene.add(ambientLight);

        var dirLight = new THREE.DirectionalLight(colors.accentYellow, 0.6);
        dirLight.position.set(20, 40, 20);
        scene.add(dirLight);

        // Low-Poly Terrain Geometry
        var gridX = 48, gridY = 36;
        var planeWidth = 70, planeHeight = 55;
        var geometry = new THREE.PlaneGeometry(planeWidth, planeHeight, gridX, gridY);
        geometry.rotateX(-Math.PI * 0.42);

        var posAttr = geometry.attributes.position;
        var initialZ = new Float32Array(posAttr.count);

        // Algorithmic Elevation Function
        function elevation(x, y) {
            var dist = Math.sqrt(x * x + y * y);
            var ridge1 = Math.sin(x * 0.18) * Math.cos(y * 0.18) * 3.2;
            var ridge2 = Math.cos(x * 0.35 + 1.2) * Math.sin(y * 0.28) * 2.0;
            var summit = Math.exp(-0.018 * (x * x + (y - 4) * (y - 4))) * 9.5;
            var foothills = Math.sin(x * 0.1) * 1.5;
            return ridge1 + ridge2 + summit + foothills;
        }

        for (var i = 0; i < posAttr.count; i++) {
            var vx = posAttr.getX(i);
            var vy = posAttr.getY(i);
            var h = elevation(vx, vy);
            posAttr.setZ(i, h);
            initialZ[i] = h;
        }
        geometry.computeVertexNormals();

        // Shaded Facet Mesh
        var facetMaterial = new THREE.MeshLambertMaterial({
            color: colors.facet,
            flatShading: true,
            polygonOffset: true,
            polygonOffsetFactor: 1,
            polygonOffsetUnits: 1
        });
        var terrainMesh = new THREE.Mesh(geometry, facetMaterial);
        scene.add(terrainMesh);

        // Bauhaus Wireframe Edges Overlay
        var wireframeGeom = new THREE.WireframeGeometry(geometry);
        var wireMaterial = new THREE.LineBasicMaterial({
            color: colors.wire,
            linewidth: 1,
            transparent: true,
            opacity: theme === 'dark' ? 0.75 : 0.45
        });
        var wireSegments = new THREE.LineSegments(wireframeGeom, wireMaterial);
        terrainMesh.add(wireSegments);

        // Summit Geometric Beacons (Bauhaus Tetrahedrons)
        var beaconGeom = new THREE.OctahedronGeometry(0.7, 0);
        var beaconColors = [colors.accentRed, colors.accentYellow, colors.wireSecondary];
        var beacons = [];
        var beaconCoords = [
            { x: 0, y: 4, z: 9.8, color: colors.accentRed },
            { x: -12, y: 8, z: 6.2, color: colors.accentYellow },
            { x: 14, y: 2, z: 5.8, color: colors.wireSecondary }
        ];

        for (var b = 0; b < beaconCoords.length; b++) {
            var bMat = new THREE.MeshBasicMaterial({
                color: beaconCoords[b].color,
                wireframe: true
            });
            var beaconMesh = new THREE.Mesh(beaconGeom, bMat);
            beaconMesh.position.set(beaconCoords[b].x, beaconCoords[b].z + 1.2, -beaconCoords[b].y);
            scene.add(beaconMesh);
            beacons.push({ mesh: beaconMesh, baseY: beaconMesh.position.y });
        }

        // Parallax Mouse Interaction
        var targetCamX = 0, targetCamY = 10;
        var currentCamX = 0, currentCamY = 10;
        var windowHalfX = window.innerWidth / 2;
        var windowHalfY = window.innerHeight / 2;

        function onMouseMove(e) {
            var mouseX = e.clientX - windowHalfX;
            var mouseY = e.clientY - windowHalfY;
            targetCamX = (mouseX / windowHalfX) * 4.5;
            targetCamY = 10 - (mouseY / windowHalfY) * 2.5;
        }
        window.addEventListener('mousemove', onMouseMove, { passive: true });

        // Resize Listener
        function onResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
            windowHalfX = window.innerWidth / 2;
            windowHalfY = window.innerHeight / 2;
        }
        window.addEventListener('resize', onResize);

        // Animation Loop with Visibility Pause
        var animId = null;
        var isVisible = true;
        var clock = new THREE.Clock();

        function render() {
            if (!isVisible) return;
            animId = requestAnimationFrame(render);

            var elapsed = clock.getElapsedTime();

            // Gentle camera lerp (parallax)
            if (!reducedMotion) {
                currentCamX += (targetCamX - currentCamX) * 0.05;
                currentCamY += (targetCamY - currentCamY) * 0.05;
                camera.position.x = currentCamX;
                camera.position.y = currentCamY;
                camera.lookAt(0, 3, 0);

                // Subtle vertex wave (breathing mountains)
                for (var v = 0; v < posAttr.count; v++) {
                    var ox = posAttr.getX(v);
                    var oy = posAttr.getY(v);
                    var wave = Math.sin(ox * 0.25 + elapsed * 0.8) * Math.cos(oy * 0.25 + elapsed * 0.6) * 0.35;
                    posAttr.setZ(v, initialZ[v] + wave);
                }
                posAttr.needsUpdate = true;
                geometry.computeVertexNormals();

                // Beacons rotation and floating hover
                for (var k = 0; k < beacons.length; k++) {
                    beacons[k].mesh.rotation.y += 0.02;
                    beacons[k].mesh.rotation.z += 0.01;
                    beacons[k].mesh.position.y = beacons[k].baseY + Math.sin(elapsed * 2 + k) * 0.4;
                }
            }

            renderer.render(scene, camera);
        }

        document.addEventListener('visibilitychange', function() {
            isVisible = !document.hidden;
            if (isVisible && !animId) {
                render();
            } else if (!isVisible && animId) {
                cancelAnimationFrame(animId);
                animId = null;
            }
        });

        render();

        var instance = {
            updateTheme: function(nextTheme) {
                var c = THEMES[nextTheme];
                scene.background.set(c.bg);
                scene.fog.color.set(c.fog);
                facetMaterial.color.set(c.facet);
                wireMaterial.color.set(c.wire);
                wireMaterial.opacity = nextTheme === 'dark' ? 0.75 : 0.45;
                ambientLight.intensity = nextTheme === 'dark' ? 0.7 : 0.9;
                dirLight.color.set(c.accentYellow);
                if (beacons[0]) beacons[0].mesh.material.color.set(c.accentRed);
                if (beacons[1]) beacons[1].mesh.material.color.set(c.accentYellow);
                if (beacons[2]) beacons[2].mesh.material.color.set(c.wireSecondary);
            },
            destroy: function() {
                if (animId) cancelAnimationFrame(animId);
                window.removeEventListener('mousemove', onMouseMove);
                window.removeEventListener('resize', onResize);
                geometry.dispose();
                wireframeGeom.dispose();
                facetMaterial.dispose();
                wireMaterial.dispose();
                renderer.dispose();
            }
        };

        Bauhaus3D.register(instance);
        return instance;
    };

    /* ==============================================================================
       MODULE 2: INTERACTIVE 3D TOPOGRAPHIC ELEVATION RADAR (Dashboard)
       ============================================================================== */
    Bauhaus3D.initTopoRadar = function(canvasId, hudId) {
        if (!isWebGLAvailable() || !window.THREE) return null;

        var canvas = document.getElementById(canvasId);
        if (!canvas) return null;

        var hud = hudId ? document.getElementById(hudId) : null;
        var theme = getCurrentTheme();
        var colors = THEMES[theme];
        var reducedMotion = isReducedMotion();

        var scene = new THREE.Scene();
        scene.background = new THREE.Color(colors.surface);

        var container = canvas.parentElement;
        var width = container ? container.clientWidth : 600;
        var height = 300;

        var camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 500);
        camera.position.set(16, 14, 20);
        camera.lookAt(0, 2, 0);

        var renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            antialias: true,
            alpha: false,
            powerPreference: 'low-power'
        });
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

        // Lighting
        var ambientLight = new THREE.AmbientLight(0xffffff, theme === 'dark' ? 0.8 : 1.0);
        scene.add(ambientLight);

        var keyLight = new THREE.DirectionalLight(0xffffff, 0.5);
        keyLight.position.set(15, 25, 15);
        scene.add(keyLight);

        // Circular Topographic Base Ring
        var ringGeom = new THREE.RingGeometry(11.8, 12.2, 48);
        ringGeom.rotateX(-Math.PI / 2);
        var ringMat = new THREE.MeshBasicMaterial({ color: colors.accentYellow, side: THREE.DoubleSide });
        var compassRing = new THREE.Mesh(ringGeom, ringMat);
        compassRing.position.y = -0.05;
        scene.add(compassRing);

        // Mountain Mesh (Contour Wireframe + Low-poly facets)
        var segments = 32;
        var terrainSize = 20;
        var geometry = new THREE.PlaneGeometry(terrainSize, terrainSize, segments, segments);
        geometry.rotateX(-Math.PI / 2);

        var pos = geometry.attributes.position;
        var currentZ = new Float32Array(pos.count);
        var targetZ = new Float32Array(pos.count);

        // Terrain Profiles Generator
        function computeProfile(x, z, difficulty) {
            var r = Math.sqrt(x * x + z * z);
            var falloff = Math.max(0, 1 - (r / 9.5));
            if (falloff <= 0) return 0;

            if (difficulty === 'Easy') {
                return (Math.sin(x * 0.4) * Math.cos(z * 0.4) * 1.5 + 2.0) * falloff;
            } else if (difficulty === 'Moderate') {
                return (Math.sin(x * 0.6) * Math.cos(z * 0.5) * 2.8 + 
                        Math.exp(-0.06 * (x * x + z * z)) * 4.5) * falloff;
            } else { // Hard / Alpine Summit
                return (Math.sin(x * 0.8) * Math.cos(z * 0.8) * 3.2 + 
                        Math.exp(-0.08 * (x * x + z * z)) * 8.2 + 
                        Math.sin(x * 1.5) * 1.0) * falloff;
            }
        }

        function setDifficulty(diff) {
            for (var i = 0; i < pos.count; i++) {
                var vx = pos.getX(i);
                var vz = pos.getZ(i);
                targetZ[i] = computeProfile(vx, vz, diff);
            }
            if (hud) {
                var stats = {
                    'Easy': { alt: '2,150M', delta: '+450M', gradient: '8%', peaks: 'ROLLING HILLS' },
                    'Moderate': { alt: '3,480M', delta: '+1,120M', gradient: '16%', peaks: 'ALPINE SADDLE' },
                    'Hard': { alt: '4,650M', delta: '+1,890M', gradient: '27%', peaks: 'RAZOR SUMMIT' }
                };
                var cur = stats[diff] || stats['Moderate'];
                hud.innerHTML = 'DIFFICULTY: <span class="fw-bold text-uppercase">' + diff + '</span> • SUMMIT: <span class="font-mono fw-bold">' + cur.alt + '</span> • ASCENT: <span class="font-mono">' + cur.delta + '</span> • GRADIENT: <span class="font-mono">' + cur.gradient + '</span>';
            }
        }

        // Initialize with Moderate
        setDifficulty('Moderate');
        for (var idx = 0; idx < pos.count; idx++) {
            currentZ[idx] = targetZ[idx];
            pos.setY(idx, currentZ[idx]);
        }
        geometry.computeVertexNormals();

        // Shaded Facet Mesh
        var facetMat = new THREE.MeshLambertMaterial({
            color: colors.facet,
            flatShading: true,
            polygonOffset: true,
            polygonOffsetFactor: 1,
            polygonOffsetUnits: 1
        });
        var terrain = new THREE.Mesh(geometry, facetMat);
        scene.add(terrain);

        // Bauhaus Wireframe Edges
        var wireGeom = new THREE.WireframeGeometry(geometry);
        var wireMat = new THREE.LineBasicMaterial({
            color: colors.wire,
            linewidth: 1,
            transparent: true,
            opacity: theme === 'dark' ? 0.8 : 0.5
        });
        var wireLine = new THREE.LineSegments(wireGeom, wireMat);
        terrain.add(wireLine);

        // Waypoint Markers
        var waypointGeom = new THREE.SphereGeometry(0.35, 8, 8);
        var summitMarkerMat = new THREE.MeshBasicMaterial({ color: colors.accentRed });
        var summitMarker = new THREE.Mesh(waypointGeom, summitMarkerMat);
        summitMarker.position.set(0, 6.0, 0);
        terrain.add(summitMarker);

        // Mouse Drag / Orbit Rotation Controls
        var isDragging = false;
        var prevX = 0, prevY = 0;
        var rotSpeed = 0.007;
        var velX = 0.003, velY = 0;

        function onMouseDown(e) {
            isDragging = true;
            prevX = e.clientX;
            prevY = e.clientY;
            velX = 0;
            velY = 0;
        }

        function onMouseMove(e) {
            if (!isDragging) return;
            var dx = e.clientX - prevX;
            var dy = e.clientY - prevY;
            terrain.rotation.y += dx * rotSpeed;
            compassRing.rotation.z += dx * rotSpeed;
            velX = dx * rotSpeed;
            prevX = e.clientX;
            prevY = e.clientY;
        }

        function onMouseUp() {
            isDragging = false;
        }

        canvas.addEventListener('mousedown', onMouseDown);
        window.addEventListener('mousemove', onMouseMove);
        window.addEventListener('mouseup', onMouseUp);

        // Responsive Resizing
        function handleResize() {
            if (!container) return;
            var w = container.clientWidth;
            camera.aspect = w / height;
            camera.updateProjectionMatrix();
            renderer.setSize(w, height);
        }
        window.addEventListener('resize', handleResize);

        // Morphing & Animation Loop
        var animId = null;
        var isVisible = true;

        function render() {
            if (!isVisible) return;
            animId = requestAnimationFrame(render);

            // Smooth vertex morphing towards target profile
            var needsUpdate = false;
            for (var m = 0; m < pos.count; m++) {
                if (Math.abs(currentZ[m] - targetZ[m]) > 0.01) {
                    currentZ[m] += (targetZ[m] - currentZ[m]) * 0.08;
                    pos.setY(m, currentZ[m]);
                    needsUpdate = true;
                }
            }
            if (needsUpdate) {
                pos.needsUpdate = true;
                geometry.computeVertexNormals();
                wireGeom.dispose();
                wireGeom = new THREE.WireframeGeometry(geometry);
                wireLine.geometry = wireGeom;
                summitMarker.position.y = targetZ[Math.floor(pos.count / 2)] + 0.6;
            }

            // Inertial smooth rotation
            if (!isDragging && !reducedMotion) {
                terrain.rotation.y += 0.004;
                compassRing.rotation.z += 0.004;
            } else if (!isDragging && Math.abs(velX) > 0.0001) {
                terrain.rotation.y += velX;
                compassRing.rotation.z += velX;
                velX *= 0.95;
            }

            renderer.render(scene, camera);
        }

        document.addEventListener('visibilitychange', function() {
            isVisible = !document.hidden;
            if (isVisible && !animId) render();
            else if (!isVisible && animId) {
                cancelAnimationFrame(animId);
                animId = null;
            }
        });

        render();

        var instance = {
            setDifficulty: setDifficulty,
            updateTheme: function(nextTheme) {
                var c = THEMES[nextTheme];
                scene.background.set(c.surface);
                facetMat.color.set(c.facet);
                wireMat.color.set(c.wire);
                wireMat.opacity = nextTheme === 'dark' ? 0.8 : 0.5;
                ringMat.color.set(c.accentYellow);
                summitMarkerMat.color.set(c.accentRed);
                ambientLight.intensity = nextTheme === 'dark' ? 0.8 : 1.0;
            },
            destroy: function() {
                if (animId) cancelAnimationFrame(animId);
                canvas.removeEventListener('mousedown', onMouseDown);
                window.removeEventListener('mousemove', onMouseMove);
                window.removeEventListener('mouseup', onMouseUp);
                window.removeEventListener('resize', handleResize);
                geometry.dispose();
                wireGeom.dispose();
                ringGeom.dispose();
                waypointGeom.dispose();
                facetMat.dispose();
                wireMat.dispose();
                ringMat.dispose();
                summitMarkerMat.dispose();
                renderer.dispose();
            }
        };

        Bauhaus3D.register(instance);
        return instance;
    };

    /* ==============================================================================
       MODULE 3: 3D HOLOGRAPHIC PERMIT TILT BADGE (Voucher / Pass)
       ============================================================================== */
    Bauhaus3D.initHoloBadge = function(canvasId) {
        if (!isWebGLAvailable() || !window.THREE) return null;

        var canvas = document.getElementById(canvasId);
        if (!canvas) return null;

        var theme = getCurrentTheme();
        var colors = THEMES[theme];
        var size = 110;

        var scene = new THREE.Scene();
        var camera = new THREE.PerspectiveCamera(40, 1, 0.1, 100);
        camera.position.set(0, 0, 7);

        var renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            antialias: true,
            alpha: true
        });
        renderer.setSize(size, size);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

        // Group
        var group = new THREE.Group();
        scene.add(group);

        // Outer Octagon Ring
        var ringGeom = new THREE.RingGeometry(2.1, 2.3, 8);
        var ringMat = new THREE.MeshBasicMaterial({ color: colors.accentYellow, side: THREE.DoubleSide });
        var ring = new THREE.Mesh(ringGeom, ringMat);
        group.add(ring);

        // Inner 3D Rotating Octahedron Star
        var starGeom = new THREE.OctahedronGeometry(1.3, 0);
        var starMat = new THREE.MeshBasicMaterial({ color: colors.accentRed, wireframe: true });
        var star = new THREE.Mesh(starGeom, starMat);
        group.add(star);

        // Central Gold Core
        var coreGeom = new THREE.OctahedronGeometry(0.55, 0);
        var coreMat = new THREE.MeshBasicMaterial({ color: colors.wire });
        var core = new THREE.Mesh(coreGeom, coreMat);
        group.add(core);

        var targetRotX = 0, targetRotY = 0;
        function onDocMouseMove(e) {
            var rect = canvas.getBoundingClientRect();
            var centerX = rect.left + rect.width / 2;
            var centerY = rect.top + rect.height / 2;
            var dx = (e.clientX - centerX) / (window.innerWidth / 2);
            var dy = (e.clientY - centerY) / (window.innerHeight / 2);
            targetRotY = dx * 0.8;
            targetRotX = dy * 0.8;
        }
        window.addEventListener('mousemove', onDocMouseMove, { passive: true });

        var animId = null;
        var isVisible = true;

        function render() {
            if (!isVisible) return;
            animId = requestAnimationFrame(render);

            group.rotation.x += (targetRotX - group.rotation.x) * 0.1;
            group.rotation.y += (targetRotY - group.rotation.y) * 0.1;

            star.rotation.y += 0.02;
            star.rotation.z += 0.01;
            core.rotation.x -= 0.03;

            renderer.render(scene, camera);
        }

        render();

        var instance = {
            updateTheme: function(nextTheme) {
                var c = THEMES[nextTheme];
                ringMat.color.set(c.accentYellow);
                starMat.color.set(c.accentRed);
                coreMat.color.set(c.wire);
            },
            destroy: function() {
                if (animId) cancelAnimationFrame(animId);
                window.removeEventListener('mousemove', onDocMouseMove);
                ringGeom.dispose();
                starGeom.dispose();
                coreGeom.dispose();
                ringMat.dispose();
                starMat.dispose();
                coreMat.dispose();
                renderer.dispose();
            }
        };

        Bauhaus3D.register(instance);
        return instance;
    };

    // Export to global window
    window.Bauhaus3D = Bauhaus3D;

})(window, document);
