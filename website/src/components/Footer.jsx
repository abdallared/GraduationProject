import logoImg from '../assets/logo.png';
import './Footer.css';

export default function Footer({ onNavigate }) {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-brand">
            <div className="footer-logo">
              <img src={logoImg} alt="Ally Vision Logo" className="footer-logo-img" />
              <span>Ally Vision</span>
            </div>
            <p>
              Empowering visually impaired individuals through intelligent
              sensor-based assistive technology and haptic feedback systems.
            </p>
          </div>

          <nav className="footer-nav">
            <h4>Navigation</h4>
            <ul>
              <li><a href="#hero" onClick={() => onNavigate && onNavigate('home')}>Home</a></li>
              <li><a href="#technology" onClick={() => onNavigate && onNavigate('home')}>Technology</a></li>
              <li><a href="#features" onClick={() => onNavigate && onNavigate('home')}>Features</a></li>
              <li><a href="#about" onClick={() => onNavigate && onNavigate('home')}>About</a></li>
              <li><a href="#team" onClick={() => onNavigate && onNavigate('home')}>Team</a></li>
              <li>
                <a
                  href="#research"
                  onClick={(e) => {
                    e.preventDefault();
                    if (onNavigate) onNavigate('research');
                  }}
                  style={{ color: 'var(--accent)', fontWeight: 600 }}
                >
                  Research Papers (AI Dedup)
                </a>
              </li>
              <li><a href="#contact" onClick={() => onNavigate && onNavigate('home')}>Contact</a></li>
            </ul>
          </nav>

          <nav className="footer-nav">
            <h4>Technology</h4>
            <ul>
              <li><a href="#technology">mmWave Radar</a></li>
              <li><a href="#technology">Stereo Camera</a></li>
              <li><a href="#technology">ToF Sensors</a></li>
              <li><a href="#technology">Haptic Feedback</a></li>
              <li><a href="#technology">Edge AI</a></li>
            </ul>
          </nav>
        </div>

        <div className="footer-bottom">
          <p>© 2026 Ally Vision — ECU Graduation Project. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
