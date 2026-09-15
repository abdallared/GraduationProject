import { useEffect, useRef } from 'react';
import TiltCard from './TiltCard';
import { animateStaggeredReveal } from '../utils/animations';
import './Team.css';

const teamMembers = [
  {
    name: 'Farah Tamer',
    initials: 'FT',
    gradient: 'linear-gradient(135deg, #0284C7 0%, #38BDF8 100%)',
    color: '#38BDF8',
  },
  {
    name: 'Taha Mohamed',
    initials: 'TM',
    gradient: 'linear-gradient(135deg, #16A34A 0%, #4ADE80 100%)',
    color: '#4ADE80',
  },
  {
    name: 'Mostafa Mohamed',
    initials: 'MM',
    gradient: 'linear-gradient(135deg, #7C3AED 0%, #A78BFA 100%)',
    color: '#A78BFA',
  },
  {
    name: 'David Hany',
    initials: 'DH',
    gradient: 'linear-gradient(135deg, #EA580C 0%, #FB923C 100%)',
    color: '#FB923C',
  },
  {
    name: 'Salma Mohamed',
    initials: 'SM',
    gradient: 'linear-gradient(135deg, #0D9488 0%, #2DD4BF 100%)',
    color: '#2DD4BF',
  },
  {
    name: 'Fathy Ahmed',
    initials: 'FA',
    gradient: 'linear-gradient(135deg, #2563EB 0%, #60A5FA 100%)',
    color: '#60A5FA',
  },
  {
    name: 'Abdallah Reda',
    initials: 'AR',
    gradient: 'linear-gradient(135deg, #475569 0%, #94A3B8 100%)',
    color: '#94A3B8',
  },
  {
    name: 'Mohamed Mohsen',
    initials: 'MM',
    gradient: 'linear-gradient(135deg, #DC2626 0%, #F87171 100%)',
    color: '#F87171',
  },
  {
    name: 'Ahmed Ragab',
    initials: 'AR',
    gradient: 'linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%)',
    color: '#3B82F6',
  },
  {
    name: 'Habiba Saad',
    initials: 'HS',
    gradient: 'linear-gradient(135deg, #9333EA 0%, #C084FC 100%)',
    color: '#C084FC',
  },
  {
    name: 'Hend Elsayed',
    initials: 'HE',
    gradient: 'linear-gradient(135deg, #059669 0%, #34D399 100%)',
    color: '#34D399',
  },
];

export default function Team() {
  const sectionRef = useRef(null);

  useEffect(() => {
    animateStaggeredReveal('.team-tilt-wrapper', sectionRef.current, 0.08);
  }, []);

  return (
    <section className="section team section-alt" id="team" ref={sectionRef}>
      <div className="container">
        <div className="section-header reveal">
          <span className="section-badge">Graduation Team</span>
          <h2>Meet the Minds Behind Ally Vision</h2>
          <p>
            An ambitious 11-engineer team from the Egyptian-Chinese University (ECU)
            collaborating across hardware, AI, embedded systems, and haptics.
          </p>
        </div>

        <div className="team-grid">
          {teamMembers.map((member, i) => (
            <div key={i} className="team-tilt-wrapper">
              <TiltCard
                className="team-card"
                spotlightColor={`${member.color}25`}
                maxTilt={8}
                scale={1.03}
                style={{
                  '--member-gradient': member.gradient,
                  '--member-color': member.color,
                }}
              >
                <div className="team-card-glow" />
                <div className="team-card-sheen" />

                <div className="team-card-header">
                  <span className="team-card-number">#{String(i + 1).padStart(2, '0')}</span>
                  <span className="team-card-chip">ECU</span>
                </div>

                <div className="team-avatar-wrapper">
                  <div className="team-avatar-aura" />
                  <div className="team-avatar-circle">
                    <span className="team-initials">{member.initials}</span>
                  </div>
                </div>

                <div className="team-card-info">
                  <h3 className="team-member-name">{member.name}</h3>
                  <span className="team-member-status">
                    <span className="team-status-dot" />
                    Engineering Team
                  </span>
                </div>
              </TiltCard>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
