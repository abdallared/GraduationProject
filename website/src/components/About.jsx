import { TargetIcon, ScienceIcon, HeartIcon, GlobeIcon } from './Icons';
import './About.css';

export default function About({ aboutImage }) {
  return (
    <section className="section about" id="about">
      <div className="container about-content">
        <div className="about-image reveal-left">
          {aboutImage && (
            <img src={aboutImage} alt="Ally Vision Real-world Assistive Navigation" className="about-image-main" />
          )}
          <div className="about-image-badge">
            <h4>ECU</h4>
            <p>Graduation Project</p>
          </div>
        </div>

        <div className="about-text reveal-right">
          <h2>
            Our <span className="accent">Mission</span>
          </h2>
          <p>
            Ally Vision was born from a simple yet powerful belief: technology should
            empower everyone to navigate the world with confidence and independence,
            regardless of their visual ability.
          </p>
          <p>
            As an Egyptian-Chinese University graduation project, we are combining
            cutting-edge sensor technology with innovative haptic feedback systems
            to create an accessible, affordable assistive device that can transform
            the daily lives of visually impaired individuals.
          </p>

          <div className="about-values">
            <div className="about-value">
              <span className="about-value-icon">
                <TargetIcon size={22} color="#1B4D7A" />
              </span>
              <div>
                <h4>Accessibility</h4>
                <p>Affordable for everyone</p>
              </div>
            </div>
            <div className="about-value">
              <span className="about-value-icon">
                <ScienceIcon size={22} color="#27AE60" />
              </span>
              <div>
                <h4>Innovation</h4>
                <p>Cutting-edge technology</p>
              </div>
            </div>
            <div className="about-value">
              <span className="about-value-icon">
                <HeartIcon size={22} color="#E74C3C" />
              </span>
              <div>
                <h4>Empathy</h4>
                <p>User-centered design</p>
              </div>
            </div>
            <div className="about-value">
              <span className="about-value-icon">
                <GlobeIcon size={22} color="#2E86C1" />
              </span>
              <div>
                <h4>Impact</h4>
                <p>Changing lives globally</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
