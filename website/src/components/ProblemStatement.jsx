import { useEffect, useRef, useState } from 'react';
import { EyeIcon, GlobeIcon, WalkIcon, BulbIcon, TargetIcon } from './Icons';
import './ProblemStatement.css';

function AnimatedCounter({ target, suffix = '' }) {
  const [count, setCount] = useState(0);
  const ref = useRef(null);
  const animated = useRef(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !animated.current) {
          animated.current = true;
          let start = 0;
          const duration = 2000;
          const startTime = performance.now();

          const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            setCount(Math.floor(eased * target));
            if (progress < 1) requestAnimationFrame(animate);
          };

          requestAnimationFrame(animate);
        }
      },
      { threshold: 0.5 }
    );

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [target]);

  return <h3 ref={ref}>{count}{suffix}</h3>;
}

export default function ProblemStatement() {
  return (
    <section className="section problem" id="problem">
      <div className="container problem-content">
        <div className="problem-stats reveal-left">
          <div className="problem-stat-card">
            <div className="stat-icon">
              <EyeIcon size={28} color="#1B4D7A" />
            </div>
            <AnimatedCounter target={285} suffix="M+" />
            <p>Visually Impaired Worldwide</p>
          </div>
          <div className="problem-stat-card">
            <div className="stat-icon">
              <GlobeIcon size={28} color="#27AE60" />
            </div>
            <AnimatedCounter target={90} suffix="%" />
            <p>Live in Developing Countries</p>
          </div>
          <div className="problem-stat-card">
            <div className="stat-icon">
              <WalkIcon size={28} color="#E67E22" />
            </div>
            <AnimatedCounter target={70} suffix="%" />
            <p>Face Mobility Challenges</p>
          </div>
          <div className="problem-stat-card">
            <div className="stat-icon">
              <BulbIcon size={28} color="#8E44AD" />
            </div>
            <AnimatedCounter target={43} suffix="M" />
            <p>Completely Blind</p>
          </div>
        </div>

        <div className="problem-text reveal-right">
          <h2>
            The Challenge We<br />
            <span className="accent">Set Out to Solve</span>
          </h2>
          <p>
            Millions of visually impaired individuals struggle to navigate their
            environments safely and independently. Traditional aids like white canes
            and guide dogs, while valuable, have significant limitations in detecting
            obstacles at varying heights and distances.
          </p>
          <p>
            Modern assistive technologies remain expensive, bulky, or require complex
            training — leaving a gap in practical, accessible solutions.
          </p>
          <div className="problem-highlight">
            <span className="problem-highlight-icon">
              <TargetIcon size={24} color="#27AE60" />
            </span>
            <p>
              Ally Vision bridges this gap with an affordable, wearable system
              that provides real-time spatial awareness through intuitive haptic feedback.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
