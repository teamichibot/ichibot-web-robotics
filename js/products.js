/* =========================================================
   ICHIBOT ROBOTICS — products.js
   Filter tab logic for products.html
   ========================================================= */

(function () {
  'use strict';

  const tabs  = document.querySelectorAll('.filter-tab');
  const cards = document.querySelectorAll('.product-card-wrap');

  if (!tabs.length || !cards.length) return;

  function filterCards(category) {
    let visibleIndex = 0;
    cards.forEach((card) => {
      const match = category === 'semua' || card.dataset.category === category;
      if (match) {
        card.style.display = '';
        // Re-trigger animation by removing + re-adding the class
        card.classList.remove('animate-in');
        void card.offsetWidth; // force reflow
        card.style.animationDelay = (visibleIndex * 0.07) + 's';
        card.classList.add('animate-in');
        visibleIndex++;
      } else {
        card.style.display = 'none';
        card.classList.remove('animate-in');
      }
    });
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      filterCards(tab.dataset.filter);
    });
  });

  // Initialize: show all
  filterCards('semua');

})();
