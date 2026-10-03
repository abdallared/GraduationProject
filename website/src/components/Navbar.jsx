import { useState, useEffect } from 'react';
import { SunIcon, MoonIcon } from './Icons';
import './Navbar.css';

const Logo = () => (
  <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="18" cy="18" r="16" stroke="currentColor" strokeWidth="2.5" fill="none" className="logo-ring" />
    <circle cx="18" cy="18" r="7" fill="#5ECDD9" />
    <circle cx="18" cy="18" r="3" fill="currentColor" className="logo-dot" />
    <path d="M2 18C2 18 8 8 18 8C28 8 34 18 34 18C34 18 28 28 18 28C8 28 2 18 2 18Z" stroke="currentColor" strokeWidth="2" fill="none" className="logo-eye" />
  </svg>
);

export default function Navbar({ currentPage = 'home', onNavigate }) {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('ally_theme') || 'dark';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('ally_theme', theme);
  }, [theme]);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  const handleLinkClick = (e, targetHash) => {
    setMenuOpen(false);
    if (currentPage !== 'home' && targetHash) {
      if (onNavigate) onNavigate('home');
      setTimeout(() => {
        const el = document.querySelector(targetHash);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }
  };

  const handleNavigatePage = (page) => {
    setMenuOpen(false);
    if (onNavigate) onNavigate(page);
  };

  return (
    <nav className={`navbar${scrolled ? ' scrolled' : ''}`}>
      <div className="container navbar-inner">
        <a
          href="#hero"
          className="navbar-logo"
          onClick={(e) => {
            if (currentPage !== 'home') {
              e.preventDefault();
              handleNavigatePage('home');
            }
          }}
        >
          <Logo />
          <span>Ally Vision</span>
        </a>

        <div className="navbar-right">
          <div className={`navbar-links${menuOpen ? ' open' : ''}`}>
            <a href="#technology" onClick={(e) => handleLinkClick(e, '#technology')}>Technology</a>
            <a href="#features" onClick={(e) => handleLinkClick(e, '#features')}>Features</a>
            <a href="#about" onClick={(e) => handleLinkClick(e, '#about')}>About</a>
            <a href="#team" onClick={(e) => handleLinkClick(e, '#team')}>Team</a>

            {/* Research Papers Dedicated Page Button */}
            <button
              type="button"
              className={`navbar-research-btn ${currentPage === 'research' ? 'active' : ''}`}
              onClick={() => handleNavigatePage('research')}
              style={{
                background: currentPage === 'research' ? 'rgba(94, 205, 217, 0.15)' : 'transparent',
                border: '1px solid ' + (currentPage === 'research' ? 'var(--accent)' : 'rgba(94, 205, 217, 0.25)'),
                color: currentPage === 'research' ? 'var(--accent)' : 'var(--text-primary)',
                padding: '0.45rem 1rem',
                borderRadius: 'var(--radius-pill)',
                fontSize: '0.85rem',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.4rem',
                transition: 'all 0.2s ease',
              }}
            >
              <span>Research</span>
              <span
                style={{
                  background: 'var(--accent)',
                  color: '#111114',
                  fontSize: '0.65rem',
                  padding: '0.15rem 0.4rem',
                  borderRadius: '100px',
                  fontWeight: 700,
                  letterSpacing: '0.5px',
                }}
              >
                AI Dedup
              </span>
            </button>

            <a href="#contact" onClick={(e) => handleLinkClick(e, '#contact')} className="navbar-cta">Contact Us</a>
          </div>

          <button
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          >
            {theme === 'dark' ? <SunIcon size={19} /> : <MoonIcon size={19} />}
          </button>

          <button
            className={`navbar-toggle${menuOpen ? ' active' : ''}`}
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="Toggle menu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </div>
    </nav>
  );
}
