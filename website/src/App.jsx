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

import heroImage from './assets/hero-device.jpg';
import lifestyleImage from './assets/lifestyle-navigation.jpg';

function App() {
  const [lenis, setLenis] = useState(null);

  useEffect(() => {
    // 1. Initialize Lenis Buttery Smooth Momentum Scrolling
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

    // 2. Smooth anchor navigation for all in-page links
    const handleAnchorClick = (e) => {
      const anchor = e.target.closest('a');
      if (!anchor) return;
      const href = anchor.getAttribute('href');
      if (href && href.startsWith('#') && href.length > 1) {
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          lenisInstance.scrollTo(target, { offset: -70, duration: 1.2 });
        }
      }
    };

    document.addEventListener('click', handleAnchorClick);

    // 3. Scroll-triggered reveal animations fallback
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
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
      <Navbar />
      <Hero heroImage={heroImage} />
      <ProblemStatement />
      <Technology />
      <Features />
      <About aboutImage={lifestyleImage} />
      <Team />
      <Contact />
      <Footer />
    </>
  );
}

export default App;
