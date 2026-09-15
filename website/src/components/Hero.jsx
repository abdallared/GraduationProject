import './Hero.css';
import SpatialRadarCanvas from './SpatialRadarCanvas';
import AnimatedCounter from './AnimatedCounter';

export default function Hero({ heroImage }) {
  return (
    <section className="hero" id="hero">
      <SpatialRadarCanvas />

      <div className="hero-bg-shapes">
        <div className="hero-circle hero-circle-1"></div>
        <div className="hero-circle hero-circle-2"></div>
        <div className="hero-circle hero-circle-3"></div>
      </div>

      <div className="container hero-content">
        <div className="hero-text reveal">
          <div className="hero-badge">
            <span></span>
            Assistive Spatial AI
          </div>

          <h1>
            See Beyond<br />
            <span className="highlight">Sight</span>
          </h1>

          <p className="hero-subtitle">
            Empowering visually impaired individuals to perceive the world
            through intelligent sensors and real-time haptic feedback —
            turning invisible obstacles into tangible awareness.
          </p>

          <div className="hero-buttons">
            <a href="#technology" className="btn btn-primary btn-magnetic">
              Explore Technology
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </a>
            <a href="#about" className="btn btn-outline btn-magnetic">
              Learn More
            </a>
          </div>

          <div className="hero-stats">
            <div className="hero-stat">
              <h3>
                <AnimatedCounter end={285} suffix="M+" />
              </h3>
              <p>Visually Impaired</p>
            </div>
            <div className="hero-stat">
              <h3>
                <AnimatedCounter end={15} prefix="<" suffix="ms" />
              </h3>
              <p>Sensor Latency</p>
            </div>
            <div className="hero-stat">
              <h3>
                <AnimatedCounter end={360} suffix="°" />
              </h3>
              <p>Spatial Awareness</p>
            </div>
          </div>
        </div>

        <div className="hero-visual reveal-right">
          <div className="hero-image-wrapper">
            {/* Sonar echo rings around visor device */}
            <div className="hero-sonar-ring ring-1"></div>
            <div className="hero-sonar-ring ring-2"></div>
            <div className="hero-sonar-ring ring-3"></div>

            {heroImage && (
              <img
                src={heroImage}
                alt="Ally Vision Assistive Visor"
                className="hero-floating-device"
              />
            )}
            <div className="hero-glow"></div>
          </div>
        </div>
      </div>
    </section>
  );
}
