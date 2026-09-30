import { useEffect, useRef } from 'react';
import { RadarIcon, CameraIcon, DistanceIcon, CpuIcon, HapticIcon, BatteryIcon } from './Icons';
import TiltCard from './TiltCard';
import { animateStaggeredReveal } from '../utils/animations';
import './Features.css';

const features = [
  {
    icon: <RadarIcon size={26} color="#5ECDD9" />,
    iconColor: 'blue',
    spotlight: 'rgba(94, 205, 217, 0.12)',
    title: 'Object Detection',
    description: 'mmWave radar technology detects obstacles and objects up to 6 meters away, even in darkness or poor visibility conditions.',
  },
  {
    icon: <CameraIcon size={26} color="#5ECDD9" />,
    iconColor: 'green',
    spotlight: 'rgba(94, 205, 217, 0.12)',
    title: 'Depth Perception',
    description: 'Stereo camera system creates real-time depth maps, providing accurate distance measurements for safe navigation.',
  },
  {
    icon: <DistanceIcon size={26} color="#D4A853" />,
    iconColor: 'orange',
    spotlight: 'rgba(212, 168, 83, 0.12)',
    title: 'Distance Sensing',
    description: 'Time-of-Flight sensors deliver precise proximity data, enabling detection of close-range obstacles and surfaces.',
  },
  {
    icon: <CpuIcon size={26} color="#9C9CA4" />,
    iconColor: 'purple',
    spotlight: 'rgba(156, 156, 164, 0.12)',
    title: 'Real-time Processing',
    description: 'Edge computing processes sensor data with minimal latency, ensuring instant feedback for dynamic environments.',
  },
  {
    icon: <HapticIcon size={26} color="#5ECDD9" />,
    iconColor: 'green',
    spotlight: 'rgba(94, 205, 217, 0.12)',
    title: 'Tactile Pin Matrix',
    description: 'Precision micro linear stepper motors actuate dynamic tactile pins to render 3D tactile contours and real-time obstacle depth.',
  },
  {
    icon: <BatteryIcon size={26} color="#5ECDD9" />,
    iconColor: 'blue',
    spotlight: 'rgba(94, 205, 217, 0.12)',
    title: 'Portable Design',
    description: 'Lightweight, ergonomic form factor designed for comfortable all-day wear with long battery life.',
  },
];

export default function Features() {
  const sectionRef = useRef(null);

  useEffect(() => {
    animateStaggeredReveal('.feature-tilt-wrapper', sectionRef.current, 0.1);
  }, []);

  return (
    <section className="section features section-alt" id="features" ref={sectionRef}>
      <div className="container">
        <div className="section-header reveal">
          <span className="section-badge">Features</span>
          <h2>Built for Independence</h2>
          <p>
            Every feature is designed to maximize spatial awareness while
            maintaining comfort and ease of use.
          </p>
        </div>

        <div className="features-grid">
          {features.map((feature, i) => (
            <div key={i} className="feature-tilt-wrapper">
              <TiltCard
                className="feature-card"
                spotlightColor={feature.spotlight}
                maxTilt={6}
                scale={1.02}
              >
                <div className={`feature-icon feature-icon-${feature.iconColor}`}>
                  {feature.icon}
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </TiltCard>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
