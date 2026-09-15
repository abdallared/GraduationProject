import { useState, useEffect } from 'react';
import { SunIcon, MoonIcon } from './Icons';
import './Navbar.css';

const Logo = () => (
  <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="18" cy="18" r="16" stroke="currentColor" strokeWidth="2.5" fill="none" className="logo-ring" />
    <circle cx="18" cy="18" r="7" fill="#22C55E"/>
    <circle cx="18" cy="18" r="3" fill="currentColor" className="logo-dot" />
    <path d="M2 18C2 18 8 8 18 8C28 8 34 18 34 18C34 18 28 28 18 28C8 28 2 18 2 18Z" stroke="currentColor" strokeWidth="2" fill="none" className="logo-eye" />
  </svg>
);

export default function Navbar() {
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

  const handleLinkClick = () => setMenuOpen(false);

  return (
    <nav className={`navbar${scrolled ? ' scrolled' : ''}`}>
      <div className="container navbar-inner">
        <a href="#hero" className="navbar-logo">
          <Logo />
          <span>Ally Vision</span>
        </a>

        <div className="navbar-right">
          <div className={`navbar-links${menuOpen ? ' open' : ''}`}>
            <a href="#technology" onClick={handleLinkClick}>Technology</a>
            <a href="#features" onClick={handleLinkClick}>Features</a>
            <a href="#about" onClick={handleLinkClick}>About</a>
            <a href="#team" onClick={handleLinkClick}>Team</a>
            <a href="#contact" onClick={handleLinkClick} className="navbar-cta">Contact Us</a>
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
