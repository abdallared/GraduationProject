import { useEffect, useState } from 'react';
import Lenis from 'lenis';
import 'lenis/dist/lenis.css';
import { gsap, ScrollTrigger } from './utils/animations';

import Navbar from './components/Navbar';
import Hero from './components/Hero';
import ProblemStatement from './components/ProblemStatement';
import Technology from './components/Technology';
import Features from './components/Features';
import About from './components/About';
import Team from './components/Team';
import Contact from './components/Contact';
import Footer from './components/Footer';
import ScrollProgress from './components/ScrollProgress';
import ResearchPapers from './components/ResearchPapers';

import heroImage from './assets/hero-device.png';
import lifestyleImage from './assets/lifestyle-navigation.jpg';

function App() {
  const [lenis, setLenis] = useState(null);
  const [currentPage, setCurrentPage] = useState(() => {
    return window.location.hash === '#research' ? 'research' : 'home';
  });

  // Listen to hashchange for seamless bookmarking/back button navigation
  useEffect(() => {
    const onHashChange = () => {
      if (window.location.hash === '#research') {
        setCurrentPage('research');
      } else {
        setCurrentPage('home');
      }
    };

    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  const handleNavigate = (page) => {
    setCurrentPage(page);
    window.location.hash = page === 'research' ? '#research' : '#hero';
  };

  // Synchronize scrolling, Lenis and GSAP animations whenever page toggles
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' });

    if (lenis) {
      lenis.scrollTo(0, { immediate: true });
      lenis.resize();
    }

    // Ensure all reveal elements are fully visible and not stuck with opacity: 0
    const makeElementsVisible = () => {
      document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach((el) => {
        el.classList.add('visible');
      });
      ScrollTrigger.refresh();
    };

    // Run immediately and after a short tick for layout recalculation
    makeElementsVisible();
    const timer = setTimeout(makeElementsVisible, 100);

    return () => clearTimeout(timer);
  }, [currentPage, lenis]);

  useEffect(() => {
    // 1. Initialize Lenis Smooth Scrolling
    const lenisInstance = new Lenis({
      duration: 1.15,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 1,
      touchMultiplier: 2,
    });

    setLenis(lenisInstance);

    // Sync GSAP ScrollTrigger with Lenis scroll updates
    lenisInstance.on('scroll', ScrollTrigger.update);

    const rafCallback = (time) => {
      lenisInstance.raf(time * 1000);
    };

    gsap.ticker.add(rafCallback);
    gsap.ticker.lagSmoothing(0);

    // 2. Smooth anchor navigation for in-page section links
    const handleAnchorClick = (e) => {
      const anchor = e.target.closest('a');
      if (!anchor) return;
      const href = anchor.getAttribute('href');
      if (href && href.startsWith('#') && href.length > 1 && href !== '#research') {
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          lenisInstance.scrollTo(target, { offset: -70, duration: 1.2 });
        }
      }
    };

    document.addEventListener('click', handleAnchorClick);

    // 3. Scroll-triggered reveal animations
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          }
        });
      },
      { threshold: 0.05, rootMargin: '0px 0px -20px 0px' }
    );

    document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach((el) => {
      observer.observe(el);
    });

    return () => {
      observer.disconnect();
      document.removeEventListener('click', handleAnchorClick);
      gsap.ticker.remove(rafCallback);
      lenisInstance.destroy();
    };
  }, []);

  return (
    <>
      <ScrollProgress lenisInstance={lenis} />
      <Navbar currentPage={currentPage} onNavigate={handleNavigate} />

      {/* Main Landing Page — preserved in DOM to prevent animation state loss */}
      <main
        style={{
          display: currentPage === 'home' ? 'block' : 'none',
          minHeight: '100vh',
        }}
      >
        <Hero heroImage={heroImage} />
        <ProblemStatement />
        <Technology />
        <Features />
        <About aboutImage={lifestyleImage} />
        <Team />
        <Contact />
      </main>

      {/* Research Papers Deduplication Page */}
      <div
        style={{
          display: currentPage === 'research' ? 'block' : 'none',
          minHeight: '100vh',
        }}
      >
        <ResearchPapers onBack={() => handleNavigate('home')} />
      </div>

      <Footer onNavigate={handleNavigate} />
    </>
  );
}

export default App;
