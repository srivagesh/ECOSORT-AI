
import { useMemo, useRef, useState } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float, Html, Sparkles } from "@react-three/drei";
import * as THREE from "three";

function createGlobePoints() {
  const points = [];
  const count = 950;
  const goldenAngle = Math.PI * (3 - Math.sqrt(5));

  for (let i = 0; i < count; i++) {
    const y = 1 - (i / (count - 1)) * 2;
    const radius = Math.sqrt(1 - y * y);
    const angle = goldenAngle * i;

    points.push(
      Math.cos(angle) * radius * 1.45,
      y * 1.45,
      Math.sin(angle) * radius * 1.45
    );
  }

  return new Float32Array(points);
}

function DottedGlobe() {
  const globe = useRef();
  const positions = useMemo(() => createGlobePoints(), []);

  useFrame((state, delta) => {
    if (globe.current) {
      globe.current.rotation.y += delta * 0.12;
      globe.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.18) * 0.08;
    }
  });

  return (
    <group ref={globe}>
      <points>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            args={[positions, 3]}
          />
        </bufferGeometry>
        <pointsMaterial
          color="#b8f18b"
          size={0.018}
          transparent
          opacity={0.9}
          sizeAttenuation
          depthWrite={false}
        />
      </points>

      <mesh>
        <sphereGeometry args={[1.43, 32, 32]} />
        <meshBasicMaterial
          color="#73c991"
          wireframe
          transparent
          opacity={0.055}
        />
      </mesh>
    </group>
  );
}

function OrbitRings() {
  return (
    <group>
      <mesh rotation={[0.9, 0.2, -0.3]}>
        <torusGeometry args={[1.85, 0.008, 8, 180]} />
        <meshBasicMaterial color="#b8f18b" transparent opacity={0.65} />
      </mesh>

      <mesh rotation={[1.3, -0.45, 0.7]}>
        <torusGeometry args={[2.05, 0.005, 8, 180]} />
        <meshBasicMaterial color="#d2e7ca" transparent opacity={0.32} />
      </mesh>

      <mesh rotation={[0.1, 0.4, 0.95]}>
        <torusGeometry args={[1.65, 0.006, 8, 180]} />
        <meshBasicMaterial color="#70dba1" transparent opacity={0.4} />
      </mesh>
    </group>
  );
}

function Phone({ position = [0, 0, 0], scale = 1 }) {
  const [hovered, setHovered] = useState(false);
  const ref = useRef();

  useFrame((_, delta) => {
    if (ref.current) {
      ref.current.rotation.y += delta * (hovered ? 0.65 : 0.12);
      ref.current.scale.lerp(
        new THREE.Vector3(
          hovered ? scale * 1.1 : scale,
          hovered ? scale * 1.1 : scale,
          hovered ? scale * 1.1 : scale
        ),
        0.12
      );
    }
  });

  return (
    <group
      ref={ref}
      position={position}
      scale={scale}
      onPointerOver={(e) => {
        e.stopPropagation();
        setHovered(true);
        document.body.style.cursor = "pointer";
      }}
      onPointerOut={() => {
        setHovered(false);
        document.body.style.cursor = "auto";
      }}
    >
      <mesh>
        <boxGeometry args={[0.44, 0.78, 0.075]} />
        <meshStandardMaterial
          color={hovered ? "#a9f879" : "#8da99a"}
          metalness={0.8}
          roughness={0.25}
        />
      </mesh>

      <mesh position={[0, 0, 0.041]}>
        <boxGeometry args={[0.37, 0.65, 0.012]} />
        <meshStandardMaterial
          color="#10251c"
          emissive="#2d8052"
          emissiveIntensity={hovered ? 1.4 : 0.45}
          roughness={0.25}
        />
      </mesh>

      <mesh position={[0, 0.31, 0.05]}>
        <boxGeometry args={[0.09, 0.018, 0.008]} />
        <meshBasicMaterial color="#b8f18b" />
      </mesh>

      <mesh position={[0, -0.25, 0.05]}>
        <circleGeometry args={[0.035, 24]} />
        <meshBasicMaterial color="#b8f18b" />
      </mesh>
    </group>
  );
}

function CircuitBoard({ position = [0, 0, 0] }) {
  const [hovered, setHovered] = useState(false);
  const ref = useRef();

  useFrame((state) => {
    if (ref.current) {
      ref.current.rotation.y =
        Math.sin(state.clock.elapsedTime * 0.6) * 0.25;
      ref.current.rotation.x =
        Math.sin(state.clock.elapsedTime * 0.4) * 0.12;
    }
  });

  return (
    <group
      ref={ref}
      position={position}
      onPointerOver={(e) => {
        e.stopPropagation();
        setHovered(true);
        document.body.style.cursor = "pointer";
      }}
      onPointerOut={() => {
        setHovered(false);
        document.body.style.cursor = "auto";
      }}
    >
      <mesh>
        <boxGeometry args={[0.62, 0.48, 0.055]} />
        <meshStandardMaterial
          color={hovered ? "#70dba1" : "#23734d"}
          metalness={0.45}
          roughness={0.35}
          emissive="#174a32"
          emissiveIntensity={hovered ? 1.1 : 0.25}
        />
      </mesh>

      {[
        [-0.17, 0.11, 0.04],
        [0.14, 0.1, 0.04],
        [-0.12, -0.12, 0.04],
        [0.16, -0.12, 0.04],
      ].map((p, i) => (
        <mesh key={i} position={p}>
          <boxGeometry args={[0.12, 0.12, 0.035]} />
          <meshStandardMaterial color="#c4d9b6" metalness={0.7} />
        </mesh>
      ))}

      {[-0.26, 0.26].map((x, i) => (
        <mesh key={i} position={[x, 0, 0.045]}>
          <boxGeometry args={[0.025, 0.25, 0.02]} />
          <meshBasicMaterial color="#b8f18b" />
        </mesh>
      ))}
    </group>
  );
}

function Battery({ position = [0, 0, 0] }) {
  const [hovered, setHovered] = useState(false);
  const ref = useRef();

  useFrame((_, delta) => {
    if (ref.current) ref.current.rotation.y += delta * 0.18;
  });

  return (
    <group
      ref={ref}
      position={position}
      onPointerOver={(e) => {
        e.stopPropagation();
        setHovered(true);
        document.body.style.cursor = "pointer";
      }}
      onPointerOut={() => {
        setHovered(false);
        document.body.style.cursor = "auto";
      }}
    >
      <mesh>
        <cylinderGeometry args={[0.15, 0.15, 0.52, 32]} />
        <meshStandardMaterial
          color={hovered ? "#c2ff92" : "#c4d2b8"}
          metalness={0.7}
          roughness={0.3}
          emissive="#8cce68"
          emissiveIntensity={hovered ? 0.8 : 0.08}
        />
      </mesh>

      <mesh position={[0, 0.28, 0]}>
        <cylinderGeometry args={[0.07, 0.07, 0.06, 24]} />
        <meshStandardMaterial color="#8da99a" metalness={0.8} />
      </mesh>

      <mesh position={[0, 0, 0.151]}>
        <boxGeometry args={[0.055, 0.22, 0.012]} />
        <meshBasicMaterial color="#173f2c" />
      </mesh>

      <mesh position={[0, 0, 0.153]}>
        <boxGeometry args={[0.16, 0.055, 0.012]} />
        <meshBasicMaterial color="#173f2c" />
      </mesh>
    </group>
  );
}

function SceneContent() {
  const rig = useRef();

  useFrame((state) => {
    if (rig.current) {
      rig.current.rotation.y = THREE.MathUtils.lerp(
        rig.current.rotation.y,
        state.pointer.x * 0.14,
        0.025
      );
      rig.current.rotation.x = THREE.MathUtils.lerp(
        rig.current.rotation.x,
        -state.pointer.y * 0.08,
        0.025
      );
    }
  });

  return (
    <>
      <color attach="background" args={["#10271d"]} />
      <fog attach="fog" args={["#10271d", 6, 12]} />

      <ambientLight intensity={1.3} />
      <directionalLight position={[3, 4, 5]} intensity={2.2} color="#d9ffca" />
      <pointLight position={[-3, 1, -2]} intensity={35} color="#4de49a" />
      <pointLight position={[2, -2, 3]} intensity={22} color="#b8f18b" />

      <Sparkles
        count={100}
        scale={7}
        size={2.4}
        speed={0.35}
        opacity={0.65}
        color="#b8f18b"
      />

      <group ref={rig}>
        <DottedGlobe />
        <OrbitRings />

        <Float speed={1.3} rotationIntensity={0.2} floatIntensity={0.5}>
          <Phone position={[-1.85, 0.55, 0.35]} scale={0.9} />
        </Float>

        <Float speed={1.6} rotationIntensity={0.3} floatIntensity={0.55}>
          <CircuitBoard position={[1.75, 0.6, 0.1]} />
        </Float>

        <Float speed={1.2} rotationIntensity={0.25} floatIntensity={0.65}>
          <Battery position={[0.8, -1.35, 0.65]} />
        </Float>

        <Float speed={1.5} rotationIntensity={0.3} floatIntensity={0.4}>
          <Phone position={[-1.05, -1.15, -0.7]} scale={0.56} />
        </Float>

        <mesh position={[0, -2.1, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <circleGeometry args={[2.15, 64]} />
          <meshBasicMaterial
            color="#397b53"
            transparent
            opacity={0.12}
            side={THREE.DoubleSide}
          />
        </mesh>
      </group>

      <Html position={[-2.05, 1.65, 0]} center transform={false}>
        <div className="eco-scene-tag">
          <span className="eco-tag-dot" />
          CIRCULAR BY DESIGN
        </div>
      </Html>
    </>
  );
}

export default function EcoScene() {
  return (
    <div className="eco-three-scene">
      <Canvas
        camera={{ position: [0, 0, 6.6], fov: 42 }}
        dpr={[1, 1.7]}
        gl={{ antialias: true, alpha: false }}
        onCreated={({ gl }) => {
          gl.setClearColor("#10271d", 1);
          gl.toneMapping = THREE.ACESFilmicToneMapping;
          gl.toneMappingExposure = 1.15;
        }}
      >
        <SceneContent />
      </Canvas>

      <div className="eco-scene-caption">
        <span className="eco-caption-pulse" />
        INTERACTIVE CIRCULAR ECOSYSTEM
      </div>
    </div>
  );
}
