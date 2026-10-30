(() => {
  document.documentElement.classList.add('js-enabled');
  const $ = (s, p = document) => p.querySelector(s);
  const year = $('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const reveals = document.querySelectorAll('[data-reveal]');
  if (!reduced && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(({target,isIntersecting}) => {
        if (isIntersecting) { target.classList.add('in-view'); observer.unobserve(target); }
      });
    }, { threshold: .07, rootMargin: '0px 0px -30px 0px' });
    reveals.forEach((el, i) => { el.style.setProperty('--reveal-delay', `${Math.min(i % 4, 3) * 75}ms`); observer.observe(el); });
  } else reveals.forEach(el => el.classList.add('in-view'));

  const toggle = $('.menu-toggle');
  const menu = $('#primary-navigation');
  const close = () => { if (!toggle || !menu) return; toggle.setAttribute('aria-expanded','false'); toggle.setAttribute('aria-label','Open menu'); menu.classList.remove('is-open'); };
  if (toggle && menu) {
    toggle.addEventListener('click', () => {
      const opened = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(opened));
      toggle.setAttribute('aria-label', opened ? 'Close menu' : 'Open menu');
      menu.classList.toggle('is-open', opened);
    });
    menu.addEventListener('click', e => { if (e.target.closest('a')) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
    window.addEventListener('resize', () => { if (innerWidth > 880) close(); }, { passive: true });
  }

  const toast = $('.copy-toast');
  const showToast = text => { if (!toast) return; toast.textContent=text; toast.classList.add('show'); clearTimeout(showToast.timeout); showToast.timeout=setTimeout(()=>toast.classList.remove('show'),2600); };
  document.querySelectorAll('[data-copy-page], [data-copy-text]').forEach(button => button.addEventListener('click', async () => {
    const value = button.hasAttribute('data-copy-page') ? location.href : button.getAttribute('data-copy-text');
    if (!value) return;
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(value);
      showToast('Copied to clipboard');
      const status = button.parentElement?.querySelector('[data-copy-feedback]') || document.querySelector('[data-copy-feedback]');
      if (status) status.textContent = 'Copied to clipboard.';
    } catch (_) {
      showToast('Copy unavailable. Select the text manually.');
      const status = button.parentElement?.querySelector('[data-copy-feedback]');
      if (status) status.textContent = `Copy this: ${value}`;
    }
  }));

  const progress = $('.scroll-progress');
  if (progress && !reduced) {
    let scheduled = false;
    const update = () => {
      const height = document.documentElement.scrollHeight - innerHeight;
      progress.style.transform = `scaleX(${height > 0 ? Math.max(0, Math.min(1, scrollY / height)) : 0})`;
      scheduled = false;
    };
    addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }
})();

// A static localhost preview cannot receive contact submissions. Do not claim that it can.
(() => {
  const form = document.querySelector('[data-enquiry-form]');
  if (!form) return;
  const status = form.querySelector('[data-form-feedback]');
  const host = location.hostname.toLowerCase();
  const canUseNetlifyForms = host.endsWith('.netlify.app') || host.endsWith('.netlify.com');
  // Set data-netlify-form-host="true" on the deployed form for a verified custom Netlify domain.
  const configuredCustomHost = form.dataset.netlifyFormHost === 'true';
  form.addEventListener('submit', (event) => {
    if (canUseNetlifyForms || configuredCustomHost) return; // Native form POST processed by Netlify.
    event.preventDefault();
    if (status) status.textContent = 'Enquiry sending becomes available on the Netlify-hosted website. This local/other-host preview cannot collect messages.';
  });
})();
