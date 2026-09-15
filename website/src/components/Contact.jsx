import { useState } from 'react';
import confetti from 'canvas-confetti';
import { MailIcon, SchoolIcon, MapPinIcon } from './Icons';
import './Contact.css';

export default function Contact() {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.65 },
      colors: ['#22C55E', '#38BDF8', '#F59E0B', '#60A5FA', '#10B981'],
    });
    setTimeout(() => setSubmitted(false), 3500);
    setFormData({ name: '', email: '', message: '' });
  };

  return (
    <section className="section contact" id="contact">
      <div className="container contact-content">
        <div className="contact-info reveal-left">
          <h2>
            Get In <span className="accent">Touch</span>
          </h2>
          <p>
            Interested in Ally Vision? Have feedback or want to collaborate?
            We'd love to hear from you.
          </p>

          <div className="contact-channels">
            <div className="contact-channel">
              <span className="contact-channel-icon">
                <MailIcon size={22} color="#1B4D7A" />
              </span>
              <div>
                <h4>Email</h4>
                <p>
                  <a href="mailto:contact@allyvision.org">contact@allyvision.org</a>
                </p>
              </div>
            </div>
            <div className="contact-channel">
              <span className="contact-channel-icon">
                <SchoolIcon size={22} color="#27AE60" />
              </span>
              <div>
                <h4>University</h4>
                <p>Egyptian-Chinese University (ECU)</p>
              </div>
            </div>
            <div className="contact-channel">
              <span className="contact-channel-icon">
                <MapPinIcon size={22} color="#E74C3C" />
              </span>
              <div>
                <h4>Location</h4>
                <p>Cairo, Egypt</p>
              </div>
            </div>
          </div>
        </div>

        <form className="contact-form reveal-right" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="contact-name">Full Name</label>
            <input
              type="text"
              id="contact-name"
              name="name"
              placeholder="Your name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="contact-email">Email</label>
            <input
              type="email"
              id="contact-email"
              name="email"
              placeholder="you@example.com"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="contact-message">Message</label>
            <textarea
              id="contact-message"
              name="message"
              placeholder="Tell us about your interest..."
              value={formData.message}
              onChange={handleChange}
              required
            ></textarea>
          </div>
          <button type="submit" className="btn btn-primary form-submit">
            {submitted ? '✓ Message Sent!' : 'Send Message'}
          </button>
        </form>
      </div>
    </section>
  );
}
