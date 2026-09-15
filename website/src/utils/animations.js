import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export { gsap, ScrollTrigger };

/**
 * Animate elements on scroll with a staggered fade up.
 */
export const animateStaggeredReveal = (selector, parentTrigger, stagger = 0.12) => {
  return gsap.fromTo(
    selector,
    {
      opacity: 0,
      y: 35,
    },
    {
      opacity: 1,
      y: 0,
      duration: 0.8,
      stagger,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: parentTrigger || selector,
        start: 'top 85%',
        once: true,
      },
    }
  );
};
