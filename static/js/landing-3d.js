/**
 * ==============================================================================
 * BAUHAUS 3D LANDING ENGINE (Ultra-Smooth Scroll-Optimized WebGL & Carousel)
 * 1919 Weimar Aesthetic • GPU Accelerated • Zero CPU Vertex Loops • 60-120 FPS
 * ==============================================================================
 */

(function(window, document) {
    'use strict';

    function isWebGLAvailable() {
        try {
            var canvas = document.createElement('canvas');
            return !!(window.WebGLRenderingContext && 
                (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
        } catch (e) {
            return false;
        }
    }

    function isReducedMotion() {
        return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    var THEMES = {
        light: {
            bg: 0xF7F5EE,
            gridMajor: 0xD0CCC0,
            gridMinor: 0xE6E2D8,
            primaryLine: 0x121212,
            accentRed: 0xD92525,
            accentYellow: 0xF6AE2D,
            accentBlue: 0x1A365D,
            particle: 0x8C887B,
            fog: 0xF7F5EE
        },
        dark: {
            bg: 0x0C0C0F,
            gridMajor: 0x22222B,
            gridMinor: 0x181820,
            primaryLine: 0xE63946,
            accentRed: 0xFF4D5C,
            accentYellow: 0xFFBE0B,
            accentBlue: 0x3A86FF,
            particle: 0x6C757D,
            fog: 0x0C0C0F
        }
    };

    function getCurrentTheme() {
        var theme = document.documentElement.getAttribute('data-bs-theme') ||
                    document.documentElement.getAttribute('data-theme') ||
                    (window.localStorage && window.localStorage.getItem('bh-theme')) || 'light';
        return theme === 'dark' ? 'dark' : 'light';
    }

    var LandingEngine = {
        /**
         * Ultra-Smooth Scroll-Coupled 3D Bauhaus Topo-Vector Flight
         */
        initTerrain: function(canvasId) {
            if (!isWebGLAvailable() || !window.THREE) return null;

            var canvas = document.getElementById(canvasId);
            if (!canvas) return null;

            var theme = getCurrentTheme();
            var colors = THEMES[theme];
            var reducedMotion = isReducedMotion();

            // Scene & Fog Setup
            var scene = new THREE.Scene();
            scene.background = new THREE.Color(colors.bg);
            scene.fog = new THREE.FogExp2(colors.fog, 0.015);

            // Camera Setup
            var camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(0, 8, 28);
            camera.lookAt(0, 0, 0);

            // WebGL Renderer Setup (Hardware Acceleration)
            var renderer = new THREE.WebGLRenderer({
                canvas: canvas,
                antialias: true,
                alpha: false,
                powerPreference: 'high-performance'
            });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

            var worldGroup = new THREE.Group();
            scene.add(worldGroup);

            // -------------------------------------------------------------
            // 1. DUAL INFINITE BAUHAUS TOPOGRAPHIC GROUND GRIDS
            // -------------------------------------------------------------
            var gridHelper1 = new THREE.GridHelper(180, 45, colors.gridMajor, colors.gridMinor);
            gridHelper1.position.set(0, -6, 0);
            worldGroup.add(gridHelper1);

            var gridHelper2 = new THREE.GridHelper(180, 45, colors.gridMajor, colors.gridMinor);
            gridHelper2.position.set(0, 18, 0);
            worldGroup.add(gridHelper2);

            // -------------------------------------------------------------
            // 2. BAUHAUS CONSTRUCTIVIST FLOATING GEOMETRIC MONOLITHS
            // -------------------------------------------------------------
            var polyGroup = new THREE.Group();
            worldGroup.add(polyGroup);

            var polyList = [];

            // A. Primary Bauhaus Icosahedron (Rotating Core Radar)
            var icoGeom = new THREE.IcosahedronGeometry(3.6, 0);
            var icoWireGeom = new THREE.WireframeGeometry(icoGeom);
            var icoMat = new THREE.LineBasicMaterial({
                color: colors.primaryLine,
                linewidth: 2,
                transparent: true,
                opacity: theme === 'dark' ? 0.85 : 0.65
            });
            var icoMesh = new THREE.LineSegments(icoWireGeom, icoMat);
            icoMesh.position.set(0, 2.5, -4);
            polyGroup.add(icoMesh);
            polyList.push({ mesh: icoMesh, rx: 0.004, ry: 0.007, rz: 0.002, speedScale: 1.0 });

            // B. Concentric Contour Rings (Elevation Altitude Circles)
            var ringGeom1 = new THREE.RingGeometry(5.2, 5.26, 64);
            var ringMat1 = new THREE.LineBasicMaterial({ color: colors.accentRed, transparent: true, opacity: 0.75 });
            var ringMesh1 = new THREE.LineSegments(new THREE.WireframeGeometry(ringGeom1), ringMat1);
            ringMesh1.position.set(0, 2.5, -4);
            ringMesh1.rotation.x = Math.PI / 2;
            polyGroup.add(ringMesh1);
            polyList.push({ mesh: ringMesh1, rx: 0.002, ry: 0.003, rz: 0.008, speedScale: 1.2 });

            var ringGeom2 = new THREE.RingGeometry(7.0, 7.06, 64);
            var ringMat2 = new THREE.LineBasicMaterial({ color: colors.accentYellow, transparent: true, opacity: 0.6 });
            var ringMesh2 = new THREE.LineSegments(new THREE.WireframeGeometry(ringGeom2), ringMat2);
            ringMesh2.position.set(0, 2.5, -4);
            ringMesh2.rotation.x = Math.PI / 3;
            polyGroup.add(ringMesh2);
            polyList.push({ mesh: ringMesh2, rx: -0.003, ry: 0.005, rz: -0.004, speedScale: 0.8 });

            // C. Floating Alpine Beacons (Dispersed in Deep 3D Space)
            var beaconDefinitions = [
                { geom: new THREE.OctahedronGeometry(1.8, 0), pos: [-16, 7, -15], color: colors.accentRed, rx: 0.01, ry: 0.015 },
                { geom: new THREE.TetrahedronGeometry(2.0, 0), pos: [18, 5, -20], color: colors.accentYellow, rx: -0.012, ry: 0.008 },
                { geom: new THREE.DodecahedronGeometry(1.5, 0), pos: [-22, -2, -35], color: colors.accentBlue, rx: 0.006, ry: -0.01 },
                { geom: new THREE.OctahedronGeometry(2.2, 0), pos: [20, -1, -45], color: colors.primaryLine, rx: 0.009, ry: 0.012 },
                { geom: new THREE.IcosahedronGeometry(2.5, 0), pos: [-12, 12, -60], color: colors.accentRed, rx: -0.007, ry: -0.009 },
                { geom: new THREE.TetrahedronGeometry(2.8, 0), pos: [14, 8, -75], color: colors.accentYellow, rx: 0.008, ry: 0.014 }
            ];

            beaconDefinitions.forEach(function(def) {
                var bWire = new THREE.WireframeGeometry(def.geom);
                var bMat = new THREE.LineBasicMaterial({ color: def.color, transparent: true, opacity: 0.65 });
                var bMesh = new THREE.LineSegments(bWire, bMat);
                bMesh.position.set(def.pos[0], def.pos[1], def.pos[2]);
                polyGroup.add(bMesh);
                polyList.push({ mesh: bMesh, rx: def.rx, ry: def.ry, rz: 0.005, speedScale: 1.0 });
            });

            // -------------------------------------------------------------
            // 3. GPU ALPINE ALTITUDE PARTICLE CONSTELLATION
            // -------------------------------------------------------------
            var particleCount = 650;
            var particleGeom = new THREE.BufferGeometry();
            var particlePositions = new Float32Array(particleCount * 3);

            for (var p = 0; p < particleCount; p++) {
                particlePositions[p * 3] = (Math.random() - 0.5) * 120;
                particlePositions[p * 3 + 1] = (Math.random() - 0.5) * 50;
                particlePositions[p * 3 + 2] = (Math.random() - 0.5) * 160;
            }

            particleGeom.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

            var particleMat = new THREE.PointsMaterial({
                color: colors.particle,
                size: 1.4,
                transparent: true,
                opacity: theme === 'dark' ? 0.75 : 0.45,
                sizeAttenuation: true
            });

            var particleSystem = new THREE.Points(particleGeom, particleMat);
            worldGroup.add(particleSystem);

            // -------------------------------------------------------------
            // 4. SMOOTH INTERPOLATED SCROLL & PARALLAX PHYSICS
            // -------------------------------------------------------------
            var scrollTarget = 0;
            var scrollCurrent = 0;
            var scrollVelocity = 0;
            var lastScrollY = window.scrollY || 0;
            var mouseX = 0, mouseY = 0;
            var targetMouseX = 0, targetMouseY = 0;

            function onScroll() {
                var docH = document.documentElement.scrollHeight - window.innerHeight;
                var curY = window.scrollY || window.pageYOffset || 0;
                scrollTarget = docH > 0 ? Math.min(Math.max(curY / docH, 0), 1) : 0;
                scrollVelocity = (curY - lastScrollY) * 0.0025;
                lastScrollY = curY;
            }

            window.addEventListener('scroll', onScroll, { passive: true });

            window.addEventListener('mousemove', function(e) {
                targetMouseX = (e.clientX - window.innerWidth / 2) / (window.innerWidth / 2);
                targetMouseY = (e.clientY - window.innerHeight / 2) / (window.innerHeight / 2);
            }, { passive: true });

            window.addEventListener('resize', function() {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
                onScroll();
            });

            // -------------------------------------------------------------
            // 5. BUTTERY 60-120 FPS RAF RENDER LOOP
            // -------------------------------------------------------------
            var animId = null;
            var isVisible = true;
            var clock = new THREE.Clock();

            function render() {
                if (!isVisible) return;
                animId = requestAnimationFrame(render);

                var delta = Math.min(clock.getDelta(), 0.1);
                var elapsed = clock.getElapsedTime();

                // Smooth Damping Lerps (Zero Stutter)
                scrollCurrent += (scrollTarget - scrollCurrent) * 0.08;
                scrollVelocity *= 0.90;
                mouseX += (targetMouseX - mouseX) * 0.06;
                mouseY += (targetMouseY - mouseY) * 0.06;

                if (!reducedMotion) {
                    // Continuous forward flight + scroll acceleration
                    var flightSpeed = (0.35 + Math.abs(scrollVelocity) * 12.0) * delta;
                    
                    // Grid looping for infinite smooth glide
                    gridHelper1.position.z = (gridHelper1.position.z + flightSpeed * 8) % 8;
                    gridHelper2.position.z = (gridHelper2.position.z + flightSpeed * 8) % 8;

                    // Camera position dynamically smoothly follows scroll progression
                    var camTargetZ = 28 - (scrollCurrent * 55);
                    var camTargetY = 8 - (scrollCurrent * 4) + (-mouseY * 1.5);
                    var camTargetX = (scrollCurrent * 8) * Math.sin(scrollCurrent * Math.PI) + (mouseX * 2.5);

                    camera.position.x += (camTargetX - camera.position.x) * 0.07;
                    camera.position.y += (camTargetY - camera.position.y) * 0.07;
                    camera.position.z += (camTargetZ - camera.position.z) * 0.07;

                    // Dynamic Camera Pitch/Yaw tilt responding to scroll & mouse
                    var lookZ = camera.position.z - 30;
                    var lookY = 2 + (scrollCurrent * 3) + (-mouseY * 0.8);
                    var lookX = (mouseX * 1.5);
                    camera.lookAt(lookX, lookY, lookZ);

                    // Polyhedra smooth orbital rotation
                    var dynamicRotScale = 1.0 + Math.abs(scrollVelocity) * 6.0;
                    for (var i = 0; i < polyList.length; i++) {
                        var p = polyList[i];
                        p.mesh.rotation.x += p.rx * p.speedScale * dynamicRotScale;
                        p.mesh.rotation.y += p.ry * p.speedScale * dynamicRotScale;
                        p.mesh.rotation.z += p.rz * p.speedScale * dynamicRotScale;
                    }

                    // Gentle global group drift
                    worldGroup.rotation.y = Math.sin(elapsed * 0.12) * 0.03 + (mouseX * 0.02);
                    worldGroup.rotation.x = Math.cos(elapsed * 0.15) * 0.02 + (-mouseY * 0.02);
                }

                renderer.render(scene, camera);
            }

            // Tab visibility throttling to preserve CPU/Battery
            document.addEventListener('visibilitychange', function() {
                isVisible = !document.hidden;
                if (isVisible && !animId) {
                    clock.start();
                    render();
                } else if (!isVisible && animId) {
                    cancelAnimationFrame(animId);
                    animId = null;
                }
            });

            // Theme Switcher Sync
            function syncTheme(nextTheme) {
                var c = THEMES[nextTheme];
                scene.background.set(c.bg);
                scene.fog.color.set(c.fog);
                icoMat.color.set(c.primaryLine);
                icoMat.opacity = nextTheme === 'dark' ? 0.85 : 0.65;
                ringMat1.color.set(c.accentRed);
                ringMat2.color.set(c.accentYellow);
                particleMat.color.set(c.particle);
                particleMat.opacity = nextTheme === 'dark' ? 0.75 : 0.45;
                
                // Re-tint grids
                scene.remove(worldGroup);
                worldGroup.remove(gridHelper1);
                worldGroup.remove(gridHelper2);
                gridHelper1 = new THREE.GridHelper(180, 45, c.gridMajor, c.gridMinor);
                gridHelper1.position.set(0, -6, 0);
                gridHelper2 = new THREE.GridHelper(180, 45, c.gridMajor, c.gridMinor);
                gridHelper2.position.set(0, 18, 0);
                worldGroup.add(gridHelper1);
                worldGroup.add(gridHelper2);
                scene.add(worldGroup);
            }

            if (window.MutationObserver) {
                var observer = new MutationObserver(function() {
                    syncTheme(getCurrentTheme());
                });
                observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-bs-theme', 'data-theme'] });
            }

            onScroll();
            render();
        },

        /**
         * 3D Card Feature Carousel Controller
         */
        initCarousel: function(carouselId) {
            var container = document.getElementById(carouselId);
            if (!container) return;

            var slides = container.querySelectorAll('.bh-carousel-slide');
            var prevBtn = container.querySelector('.bh-carousel-prev');
            var nextBtn = container.querySelector('.bh-carousel-next');
            var dots = container.querySelectorAll('.bh-carousel-dot');
            var progressBar = container.querySelector('.bh-carousel-progress-bar');
            var counter = container.querySelector('.bh-carousel-counter');

            var currentIndex = 0;
            var totalSlides = slides.length;
            var timer = null;
            var duration = 6000;
            var isPaused = false;

            function updateUI() {
                for (var i = 0; i < totalSlides; i++) {
                    var s = slides[i];
                    var offset = (i - currentIndex + totalSlides) % totalSlides;
                    if (offset > totalSlides / 2) offset -= totalSlides;

                    s.classList.remove('active', 'prev', 'next', 'far-prev', 'far-next');

                    if (offset === 0) s.classList.add('active');
                    else if (offset === -1 || (currentIndex === 0 && i === totalSlides - 1)) s.classList.add('prev');
                    else if (offset === 1 || (currentIndex === totalSlides - 1 && i === 0)) s.classList.add('next');
                    else if (offset < 0) s.classList.add('far-prev');
                    else s.classList.add('far-next');
                }

                for (var d = 0; d < dots.length; d++) {
                    dots[d].classList.toggle('active', d === currentIndex);
                }

                if (counter) {
                    var cur = (currentIndex + 1) < 10 ? '0' + (currentIndex + 1) : (currentIndex + 1);
                    var tot = totalSlides < 10 ? '0' + totalSlides : totalSlides;
                    counter.textContent = cur + ' // ' + tot;
                }

                resetProgress();
            }

            function goTo(idx) {
                currentIndex = (idx + totalSlides) % totalSlides;
                updateUI();
            }

            function next() { goTo(currentIndex + 1); }
            function prev() { goTo(currentIndex - 1); }

            function resetProgress() {
                if (progressBar) {
                    progressBar.style.transition = 'none';
                    progressBar.style.width = '0%';
                    void progressBar.offsetWidth;
                    if (!isPaused) {
                        progressBar.style.transition = 'width ' + duration + 'ms linear';
                        progressBar.style.width = '100%';
                    }
                }
                if (timer) clearInterval(timer);
                if (!isPaused) {
                    timer = setInterval(next, duration);
                }
            }

            if (prevBtn) prevBtn.addEventListener('click', prev);
            if (nextBtn) nextBtn.addEventListener('click', next);

            for (var d = 0; d < dots.length; d++) {
                (function(idx) {
                    dots[idx].addEventListener('click', function() { goTo(idx); });
                })(d);
            }

            for (var s = 0; s < slides.length; s++) {
                (function(idx) {
                    slides[idx].addEventListener('click', function(e) {
                        if (!slides[idx].classList.contains('active')) {
                            e.preventDefault();
                            goTo(idx);
                        }
                    });
                })(s);
            }

            container.addEventListener('mouseenter', function() {
                isPaused = true;
                if (timer) clearInterval(timer);
            });
            container.addEventListener('mouseleave', function() {
                isPaused = false;
                resetProgress();
            });

            window.addEventListener('keydown', function(e) {
                if (document.activeElement && ['INPUT', 'TEXTAREA'].indexOf(document.activeElement.tagName) !== -1) return;
                if (e.key === 'ArrowRight') next();
                else if (e.key === 'ArrowLeft') prev();
            });

            updateUI();
        }
    };

    window.LandingEngine = LandingEngine;

})(window, document);
