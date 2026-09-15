import { useState } from 'react';
import sevenStageInfographic from '../assets/7stage.jpg';
import tactilePinMatrixImg from '../assets/tactile-pin-matrix.png';
import './Technology.css';

const matrixPresets = {
  center: {
    name: 'Approaching Obstacle (Center)',
    grid: [
      [0, 0, 3, 0, 0],
      [0, 2, 5, 2, 0],
      [1, 4, 6, 4, 1],
      [0, 2, 5, 2, 0],
      [0, 0, 3, 0, 0],
    ],
  },
  table: {
    name: 'Table Edge / Barrier Ahead',
    grid: [
      [0, 0, 0, 0, 0],
      [5, 5, 5, 5, 5],
      [6, 6, 6, 6, 6],
      [2, 2, 2, 2, 2],
      [0, 0, 0, 0, 0],
    ],
  },
  left: {
    name: 'Lateral Hazard (Left Wall/Door)',
    grid: [
      [5, 2, 0, 0, 0],
      [6, 4, 1, 0, 0],
      [6, 5, 2, 0, 0],
      [6, 4, 1, 0, 0],
      [5, 2, 0, 0, 0],
    ],
  },
  right: {
    name: 'Lateral Hazard (Right Obstacle)',
    grid: [
      [0, 0, 0, 2, 5],
      [0, 0, 1, 4, 6],
      [0, 0, 2, 5, 6],
      [0, 0, 1, 4, 6],
      [0, 0, 0, 2, 5],
    ],
  },
};

export default function Technology() {
  const [activePreset, setActivePreset] = useState('center');
  const [customGrid, setCustomGrid] = useState(null);
  const [hoveredPin, setHoveredPin] = useState(null);

  const currentGrid = customGrid || matrixPresets[activePreset].grid;

  const handlePresetClick = (key) => {
    setActivePreset(key);
    setCustomGrid(null);
  };

  const handleCellClick = (rIdx, cIdx) => {
    const nextGrid = currentGrid.map((row, r) =>
      row.map((val, c) => (r === rIdx && c === cIdx ? (val + 1) % 7 : val))
    );
    setCustomGrid(nextGrid);
    setActivePreset('custom');
  };

  return (
    <section className="section technology section-dark" id="technology">
      <div className="container">
        {/* Section Header */}
        <div className="section-header reveal">
          <span className="section-badge">Clinical Schematic</span>
          <h2>Engineering a New Sense: The 7-Stage Architecture</h2>
          <p>
            Translating sight into spatial awareness: A bio-inspired sensory substitution system
            abstracting high-density optical streams into a 5×5 tactile height matrix on the forehead.
          </p>
        </div>

        {/* 7-Stage Hero Infographic Showcase */}
        <div className="seven-stage-hero-wrapper reveal">
          <div className="seven-stage-image-frame">
            <img
              src={sevenStageInfographic}
              alt="Ally Vision 7-Stage Clinical Architecture: The Eye, Visual Cortex, Nervous System, and Muscle & Skin"
              className="seven-stage-main-img"
            />
          </div>

          <div className="seven-stage-columns-nav">
            <div className="stage-nav-card">
              <span className="stage-nav-badge badge-blue">Stage 1</span>
              <div className="stage-nav-info">
                <h4>The Eye</h4>
                <p>Dual-Stream Camera Sensor</p>
              </div>
            </div>

            <div className="stage-nav-card">
              <span className="stage-nav-badge badge-cyan">Stage 2</span>
              <div className="stage-nav-info">
                <h4>Visual Cortex</h4>
                <p>AI Neural Chip & 5×5 Matrix</p>
              </div>
            </div>

            <div className="stage-nav-card">
              <span className="stage-nav-badge badge-purple">Stages 3 & 4</span>
              <div className="stage-nav-info">
                <h4>Nervous System</h4>
                <p>Serial Bridge & Microcontroller</p>
              </div>
            </div>

            <div className="stage-nav-card">
              <span className="stage-nav-badge badge-pink">Stages 5–7</span>
              <div className="stage-nav-info">
                <h4>Muscle & Skin</h4>
                <p>Mechanical Linear Pin Matrix</p>
              </div>
            </div>
          </div>
        </div>

        {/* Interactive 5x5 Matrix Simulator & Core Philosophy Grid */}
        <div className="matrix-and-funnel-grid reveal">
          {/* 5x5 Matrix Simulator */}
          <div className="matrix-simulator-card">
            <div className="matrix-card-header">
              <span className="section-badge">Live Interactive Simulator</span>
              <h3>5×5 Tactile Height Matrix (0–6)</h3>
              <p>Real-time digital height levels mapping obstacle proximity to physical pin displacement</p>
            </div>

            <div className="matrix-preset-buttons">
              {Object.keys(matrixPresets).map((key) => (
                <button
                  key={key}
                  className={`matrix-preset-btn ${activePreset === key ? 'active' : ''}`}
                  onClick={() => handlePresetClick(key)}
                >
                  {matrixPresets[key].name}
                </button>
              ))}
              {activePreset === 'custom' && (
                <button
                  className="matrix-preset-btn active custom-preset"
                  onClick={() => handlePresetClick('center')}
                  title="Click to reset to Center preset"
                >
                  Custom Pattern (Click to Reset)
                </button>
              )}
            </div>

            <div className="matrix-display-container">
              <div className="matrix-grid-5x5">
                {currentGrid.map((row, rIdx) =>
                  row.map((val, cIdx) => (
                    <div
                      key={`${rIdx}-${cIdx}`}
                      className={`matrix-cell ${hoveredPin?.r === rIdx && hoveredPin?.c === cIdx ? 'hovered' : ''}`}
                      onClick={() => handleCellClick(rIdx, cIdx)}
                      onMouseEnter={() => setHoveredPin({ r: rIdx, c: cIdx, val })}
                      onMouseLeave={() => setHoveredPin(null)}
                      title={`Pin [${rIdx + 1}, ${cIdx + 1}]: Level ${val} (${(val * 0.83).toFixed(1)}mm). Click to increment.`}
                      style={{
                        background:
                          val === 0
                            ? 'rgba(255, 255, 255, 0.04)'
                            : `rgba(34, 197, 94, ${0.18 + (val / 6) * 0.72})`,
                        borderColor: val > 0 ? 'rgba(34, 197, 94, 0.65)' : 'rgba(255, 255, 255, 0.08)',
                        transform: val > 0 ? `scale(${1 + val * 0.035}) translateY(-${val * 1.2}px)` : 'scale(1)',
                        boxShadow: val > 0
                          ? `0 ${val * 2}px ${val * 4}px rgba(0,0,0,0.4), 0 0 ${val * 3}px rgba(34, 197, 94, ${val * 0.14})`
                          : 'none',
                      }}
                    >
                      <span className="matrix-cell-val">{val}</span>
                      <span className="matrix-cell-mm">{(val * 0.83).toFixed(1)}mm</span>
                    </div>
                  ))
                )}
              </div>

              <div className="matrix-legend">
                <div className="matrix-legend-scale">
                  <span>0 (Flush / Clear)</span>
                  <div className="matrix-legend-gradient"></div>
                  <span>6 (5.0mm Peak / Hazard)</span>
                </div>
                <p className="matrix-legend-note">
                  Each pin is driven by a dedicated micro linear stepper motor with sub-millimeter precision against the user's skin.
                </p>
              </div>
            </div>
          </div>

          {/* Philosophy & Tactile Features */}
          <div className="schematic-showcase-card">
            <span className="section-badge">Core Philosophy</span>
            <h3>"Abstract to Enhance"</h3>
            <p>
              Rather than overwhelming users with raw visual noise, Ally Vision converts complex 3D visual geometry into an intuitive, low-density tactile height matrix.
            </p>

            <div className="schematic-highlights">
              <div className="schematic-highlight-item">
                <strong>Zero Cognitive Overload:</strong> Abstracting high-density point clouds to a 5×5 matrix prevents sensory fatigue.
              </div>
              <div className="schematic-highlight-item">
                <strong>Forehead Optimal Haptics:</strong> Clinically proven as the optimal tactile perception zone for directional navigation.
              </div>
              <div className="schematic-highlight-item">
                <strong>Instant Sub-20ms Feedback:</strong> Hardware serial pipeline delivers zero-latency obstacle updates directly to the skin.
              </div>
              <div className="schematic-highlight-item">
                <strong>Silent Operation:</strong> 25× TMC2209 silent stepper motor drivers eliminate vibration hum and mechanical buzz.
              </div>
            </div>
          </div>
        </div>

        {/* Tactile Hardware Deep Dive Block */}
        <div className="tech-showcase reveal">
          <div className="tech-showcase-content">
            <span className="section-badge">Hardware Implementation</span>
            <h3>Precision Micro Stepper Linear Actuation</h3>
            <p>
              In direct alignment with the clinical schematic, each pin in the 5×5 matrix is paired with an independent micro linear stepper actuator and silent TMC2209 driver, delivering quiet, repeatable, and comfortable tactile relief without irritating vibration noise.
            </p>
            <ul className="tech-showcase-features">
              <li>
                <strong>25× Independent Actuators:</strong> Individual stepper motors driving lead screws with 0 to 5.0mm stroke displacement.
              </li>
              <li>
                <strong>TMC2209 SilentStep Technology:</strong> Whisper-quiet operation ensuring zero acoustic interference or user irritation.
              </li>
              <li>
                <strong>Rapid Neuro-Adaptation:</strong> Users learn obstacle recognition (chairs, doors, steps, approaching pedestrians) within minutes.
              </li>
              <li>
                <strong>Modular Architecture:</strong> Hot-swappable stages connecting commercially available sensors to edge AI and custom haptic array.
              </li>
            </ul>
          </div>
          <div className="tech-showcase-visual">
            <img
              src={tactilePinMatrixImg}
              alt="Ally Vision Tactile Pin Array Actuated by Linear Stepper Motors"
              className="tech-showcase-img"
            />
            <div className="tech-showcase-glow"></div>
          </div>
        </div>
      </div>
    </section>
  );
}
