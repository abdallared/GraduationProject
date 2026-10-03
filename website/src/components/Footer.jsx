import './Footer.css';

const Logo = () => (
  <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="18" cy="18" r="16" stroke="currentColor" strokeWidth="2.5" fill="none"/>
    <circle cx="18" cy="18" r="7" fill="#5ECDD9"/>
    <circle cx="18" cy="18" r="3" fill="currentColor"/>
    <path d="M2 18C2 18 8 8 18 8C28 8 34 18 34 18C34 18 28 28 18 28C8 28 2 18 2 18Z" stroke="currentColor" strokeWidth="2" fill="none"/>
  </svg>
);

export default function Footer({ onNavigate }) {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-brand">
            <div className="footer-logo">
              <Logo />
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
