/* ==============================================
   WHEN I WAS IN SCHOOL — V3
   Teacher-focused advocacy tool
   ============================================== */

(function () {
  'use strict';

  // Data stores
  let TEACHER = null;
  let LEGISLATOR = null;
  let NATIONAL = null;
  let STATES = null;
  let COST = null;
  let DISTRICTS = null;
  let DISTRICT_SALARY = null;

  // DOM refs
  const $landing = document.getElementById('landing');
  const $results = document.getElementById('results');
  const $gradYear = document.getElementById('grad-year');
  const $district = document.getElementById('district-select');
  const $email = document.getElementById('email-input');
  const $showMe = document.getElementById('show-me-btn');
  const $shareBtn = document.getElementById('share-btn');
  const $quickYear = document.getElementById('quick-year');
  const $copyMsg = document.getElementById('copy-message-btn');
  const $banner = document.getElementById('session-banner');
  const $stickyBar = document.getElementById('sticky-share-bar');
  const $stickyShareBtn = document.getElementById('sticky-share-btn');
  const $stickyClose = document.getElementById('sticky-share-close');

  let stickyDismissed = false;
  let shareCardBlob = null; // cached share card image

  // State names for display
  const STATE_NAMES = {
    KY: 'Kentucky', OH: 'Ohio', IN: 'Indiana', IL: 'Illinois',
    MO: 'Missouri', TN: 'Tennessee', VA: 'Virginia', WV: 'West Virginia',
  };
  const BORDER_STATES = ['OH', 'IN', 'IL', 'MO', 'TN', 'VA', 'WV'];

  // ---- Bootstrap ----
  async function init() {
    populateYearDropdown();
    await loadAllData();
    populateDistrictDropdown();
    bindEvents();
    showSessionBanner();
    handleHash();
  }

  function populateYearDropdown() {
    const currentYear = new Date().getFullYear();
    const max = Math.min(currentYear, 2025);
    for (let y = max; y >= 1970; y--) {
      const opt = document.createElement('option');
      opt.value = y;
      opt.textContent = y;
      $gradYear.appendChild(opt);

      const opt2 = document.createElement('option');
      opt2.value = y;
      opt2.textContent = y;
      $quickYear.appendChild(opt2);
    }
  }

  function populateDistrictDropdown() {
    if (!DISTRICTS) return;
    DISTRICTS.forEach(d => {
      const opt = document.createElement('option');
      opt.value = d.leaid;
      opt.textContent = d.name;
      $district.appendChild(opt);
    });
  }

  async function loadAllData() {
    const [teacher, legislator, national, states, cost, districts, districtSalary] = await Promise.all([
      fetch('data/output/teacher-salary.json').then(r => r.json()).catch(() => null),
      fetch('data/output/legislator.json').then(r => r.json()).catch(() => null),
      fetch('data/output/national-teacher-salary.json').then(r => r.json()).catch(() => null),
      fetch('data/output/state-teacher-salary.json').then(r => r.json()).catch(() => null),
      fetch('data/output/cost-of-living.json').then(r => r.json()).catch(() => null),
      fetch('data/output/districts.json').then(r => r.json()).catch(() => null),
      fetch('data/output/district_salary.json').then(r => r.json()).catch(() => null),
    ]);

    TEACHER = teacher;
    LEGISLATOR = legislator;
    NATIONAL = national;
    STATES = states;
    COST = cost;
    DISTRICTS = districts;
    DISTRICT_SALARY = districtSalary;
  }

  function bindEvents() {
    $gradYear.addEventListener('change', () => {
      $showMe.disabled = !$gradYear.value;
    });

    $showMe.addEventListener('click', () => {
      const year = parseInt($gradYear.value, 10);
      if (year) {
        collectContact(year);
        showResults(year);
      }
    });

    $shareBtn.addEventListener('click', shareResults);
    $stickyShareBtn.addEventListener('click', shareResults);

    $stickyClose.addEventListener('click', () => {
      stickyDismissed = true;
      $stickyBar.classList.remove('visible');
      $stickyBar.classList.add('hidden');
    });

    $quickYear.addEventListener('change', () => {
      const year = parseInt($quickYear.value, 10);
      if (year) showResults(year);
    });

    if ($copyMsg) {
      $copyMsg.addEventListener('click', copyMessage);
    }
  }

  function handleHash() {
    const hash = window.location.hash;
    const yearMatch = hash.match(/year=(\d{4})/);
    const districtMatch = hash.match(/district=(\d+)/);
    if (yearMatch) {
      const year = parseInt(yearMatch[1], 10);
      if (year >= 1970 && year <= 2025) {
        $gradYear.value = year;
        if (districtMatch && $district) {
          $district.value = districtMatch[1];
        }
        showResults(year);
      }
    }
  }

  // ---- Session Banner ----
  function showSessionBanner() {
    const now = new Date();
    const month = now.getMonth();
    const inSession = month >= 0 && month <= 3;
    if (inSession) {
      $banner.textContent = 'The Kentucky General Assembly is in session RIGHT NOW. Your voice matters today.';
    } else {
      $banner.textContent = 'The next legislative session begins in January. Get informed now.';
    }
    $banner.classList.remove('hidden');
  }

  // ---- Email Collection ----
  function collectContact(year) {
    const email = $email.value.trim();
    if (!email) return;

    const endpoint = ''; // TODO: Replace with deployed Google Apps Script URL
    if (!endpoint) return;

    const body = JSON.stringify({
      email: email,
      year: year,
      district: $district.value || '',
      timestamp: new Date().toISOString(),
    });

    fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body,
      mode: 'no-cors',
    }).catch(() => {});
  }

  // ---- Show Results ----
  function showResults(gradYear) {
    const districtId = $district ? $district.value : '';
    let hashStr = `year=${gradYear}`;
    if (districtId) hashStr += `&district=${districtId}`;
    window.location.hash = hashStr;

    $landing.classList.add('hidden');
    $results.classList.remove('hidden');

    const gy = String(gradYear);
    const tch = TEACHER?.by_grad_year?.[gy] || {};
    const tchNow = TEACHER?.current_year || {};
    const leg = LEGISLATOR?.by_grad_year?.[gy] || {};
    const legNow = LEGISLATOR?.current_year || {};

    renderHeroStat(gradYear, tch, tchNow);
    renderDetailCards(gradYear, tch, tchNow);
    renderBudget(gradYear, tch, tchNow, leg, legNow);
    renderNation(gradYear, tch, tchNow);
    renderNeighbors(gradYear);
    renderCostOfLiving(gradYear, tch, tchNow);
    renderMessage(gradYear, tch, tchNow);
    setupStickyBar(gradYear, tch, tchNow);

    // Set quick year picker to current selection
    $quickYear.value = gradYear;

    // Reset and setup scroll reveals
    setupScrollReveals();

    // Generate share card after count-up animation finishes
    shareCardBlob = null;
    const animDelay = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 100 : 1600;
    setTimeout(() => generateShareCard(), animDelay);

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // ---- Section Renderers ----

  function renderHeroStat(gradYear, then, now) {
    const $intro = document.getElementById('hero-stat-intro');
    const $number = document.getElementById('hero-stat-number');
    const $narrative = document.getElementById('hero-stat-narrative');
    const $detail = document.getElementById('hero-stat-detail');

    $intro.textContent = `YOU GRADUATED IN ${gradYear}.`;

    if (!then.data_available) {
      $number.className = 'hero-stat-number no-data';
      $number.textContent = '\u2014';
      $narrative.textContent = "We don\u2019t have salary data from back then \u2014 but here\u2019s what we do know about what\u2019s happened since.";
      $detail.textContent = '';
      return;
    }

    const pctChange = computePctChange(then.adjusted, now.adjusted);
    const isNeg = pctChange < 0;

    $number.className = 'hero-stat-number ' + (isNeg ? 'negative' : 'positive');
    $number.textContent = '0%';

    if (isNeg) {
      $narrative.textContent = `That\u2019s how much Kentucky teacher pay has fallen since you walked the halls.`;
    } else {
      $narrative.textContent = `That\u2019s how much Kentucky teacher pay has grown since you walked the halls.`;
    }

    $detail.textContent = `In ${then.school_year}, a Kentucky teacher earned ${dollar(then.adjusted)} (in today\u2019s dollars). Today: ${dollar(now.adjusted)}.`;

    animateCount($number, pctChange);
  }

  function renderDetailCards(gradYear, then, now) {
    const $cardsCol = document.getElementById('detail-cards-col');
    const $hoursNote = document.getElementById('detail-hours-note');
    const $source = document.getElementById('detail-source');

    if (!then.data_available) {
      $cardsCol.innerHTML = noDataBlock(gradYear, 'teacher salary', 1990);
      $hoursNote.textContent = '';
      $source.textContent = '';
      return;
    }

    const hours = TEACHER?.metadata?.hours_basis || 1402;

    const thenHourly = then.hourly_rate != null ? then.hourly_rate : (then.adjusted / hours).toFixed(2);
    const nowHourly = now.hourly_rate != null ? now.hourly_rate : (now.adjusted / hours).toFixed(2);

    $cardsCol.innerHTML = `
      <div class="comp-card comp-card--then">
        <div class="comp-label comp-label--then">THEN</div>
        <div class="comp-year">${then.school_year || ''}</div>
        <div class="comp-value">${dollar(then.adjusted)}</div>
        ${then.nominal ? `<div class="comp-detail">${dollar(then.nominal)} in original dollars</div>` : ''}
        <div class="comp-hourly">
          <div class="comp-hourly-value">${dollar(thenHourly)}/hr</div>
          <div class="comp-hourly-label">effective hourly rate</div>
        </div>
      </div>
      <div class="comp-card comp-card--now">
        <div class="comp-label comp-label--now">NOW</div>
        <div class="comp-year">${now.school_year || ''}</div>
        <div class="comp-value">${dollar(now.adjusted)}</div>
        ${now.nominal ? `<div class="comp-detail">${dollar(now.nominal)} in current dollars</div>` : ''}
        <div class="comp-hourly">
          <div class="comp-hourly-value">${dollar(nowHourly)}/hr</div>
          <div class="comp-hourly-label">effective hourly rate</div>
        </div>
      </div>
    `;

    $hoursNote.textContent = `Based on ${hours} contractual hours/year (187 days \u00d7 7.5 hrs). Most teachers work significantly more \u2014 planning, grading, coaching, and more.`;
    $source.textContent = then.source ? `Source: ${then.source}` : '';
  }

  // ---- vs. The Nation ----
  function renderNation(gradYear, kyThen, kyNow) {
    const $comp = document.getElementById('nation-comparison');
    const $narr = document.getElementById('nation-narrative');
    const gy = String(gradYear);

    if (!NATIONAL) {
      $comp.innerHTML = '';
      $narr.textContent = '';
      return;
    }

    const natThen = NATIONAL.by_grad_year?.[gy] || {};
    const natNow = NATIONAL.current_year || {};
    const kyPct = computePctChange(kyThen.adjusted, kyNow.adjusted);
    const natPct = computePctChange(natThen.adjusted, natNow.adjusted);
    const kyRank = STATES?.metadata?.ranks?.KY;

    const kySign = kyPct !== null ? (kyPct >= 0 ? '+' : '') : '';
    const natSign = natPct !== null ? (natPct >= 0 ? '+' : '') : '';
    const kyCls = kyPct !== null ? (kyPct >= 0 ? 'positive' : 'negative') : '';
    const natCls = natPct !== null ? (natPct >= 0 ? 'positive' : 'negative') : '';

    $comp.innerHTML = `
      <div class="nation-card">
        <div class="nation-card-label">KENTUCKY</div>
        <div class="nation-card-pct ${kyCls}">${kyPct !== null ? kySign + kyPct + '%' : 'N/A'}</div>
        <div class="nation-card-salary">${dollar(kyNow.adjusted)}</div>
        ${kyRank ? `<div class="nation-card-rank">Rank: ${ordinal(kyRank)}</div>` : ''}
      </div>
      <div class="nation-card">
        <div class="nation-card-label">NATIONAL AVG</div>
        <div class="nation-card-pct ${natCls}">${natPct !== null ? natSign + natPct + '%' : 'N/A'}</div>
        <div class="nation-card-salary">${dollar(natNow.adjusted)}</div>
        <div class="nation-card-detail">&nbsp;</div>
      </div>
    `;

    if (kyPct !== null && natPct !== null) {
      const kyVerb = kyPct < 0 ? `a ${Math.abs(kyPct)}% pay cut` : `a ${kyPct}% raise`;
      const natVerb = natPct < 0 ? `a ${Math.abs(natPct)}% cut` : `a ${natPct}% raise`;
      $narr.textContent = `Since you graduated, the average American teacher saw ${natVerb}. Kentucky teachers got ${kyVerb}.${kyRank ? ` Kentucky now ranks ${ordinal(kyRank)} out of 50 states.` : ''}`;
    } else {
      $narr.textContent = '';
    }
  }

  // ---- vs. Your Neighbors ----
  function renderNeighbors(gradYear) {
    const $pills = document.getElementById('neighbor-pills');
    const $content = document.getElementById('neighbor-content');

    if (!STATES) {
      $pills.innerHTML = '';
      $content.innerHTML = '';
      return;
    }

    // Build pills
    let pillsHtml = '';
    BORDER_STATES.forEach(st => {
      pillsHtml += `<button class="neighbor-pill" data-state="${st}">${st}</button>`;
    });
    $pills.innerHTML = pillsHtml;

    // Default: show ranked list of all states
    renderNeighborRankList(gradYear);

    // Bind pill clicks
    $pills.querySelectorAll('.neighbor-pill').forEach(btn => {
      btn.addEventListener('click', () => {
        const st = btn.dataset.state;
        const isActive = btn.classList.contains('active');

        // Deselect all
        $pills.querySelectorAll('.neighbor-pill').forEach(b => b.classList.remove('active'));

        if (isActive) {
          renderNeighborRankList(gradYear);
        } else {
          btn.classList.add('active');
          renderNeighborDetail(gradYear, st);
        }
      });
    });
  }

  function renderNeighborRankList(gradYear) {
    const $content = document.getElementById('neighbor-content');
    const gy = String(gradYear);

    // Build array of all states with current data
    const allStates = ['KY', ...BORDER_STATES];
    const items = allStates.map(st => {
      const cur = STATES[st]?.current_year || {};
      const then = STATES[st]?.by_grad_year?.[gy] || {};
      const pct = computePctChange(then.adjusted, cur.adjusted);
      return {
        state: st,
        salary: cur.adjusted,
        rank: cur.rank,
        pct: pct,
      };
    }).sort((a, b) => (b.salary || 0) - (a.salary || 0));

    let html = '<div class="neighbor-rank-list">';
    items.forEach((item) => {
      const isKy = item.state === 'KY';
      html += `
        <div class="neighbor-rank-item${isKy ? ' is-ky' : ''}">
          <span class="neighbor-rank-pos">${item.rank ? ordinal(item.rank) : ''}</span>
          <span class="neighbor-rank-state">${STATE_NAMES[item.state] || item.state}</span>
          <span class="neighbor-rank-salary">${dollar(item.salary)}</span>
        </div>
      `;
    });
    html += '</div>';
    $content.innerHTML = html;
  }

  function renderNeighborDetail(gradYear, selectedState) {
    const $content = document.getElementById('neighbor-content');
    const gy = String(gradYear);

    const kyCur = STATES.KY?.current_year || {};
    const kyThen = STATES.KY?.by_grad_year?.[gy] || {};
    const kyPct = computePctChange(kyThen.adjusted, kyCur.adjusted);

    const stCur = STATES[selectedState]?.current_year || {};
    const stThen = STATES[selectedState]?.by_grad_year?.[gy] || {};
    const stPct = computePctChange(stThen.adjusted, stCur.adjusted);

    const kySign = kyPct !== null ? (kyPct >= 0 ? '+' : '') : '';
    const stSign = stPct !== null ? (stPct >= 0 ? '+' : '') : '';
    const kyCls = kyPct !== null ? (kyPct >= 0 ? 'positive' : 'negative') : '';
    const stCls = stPct !== null ? (stPct >= 0 ? 'positive' : 'negative') : '';

    $content.innerHTML = `
      <div class="neighbor-detail">
        <div class="neighbor-detail-card ky-card">
          <div class="neighbor-detail-state">KENTUCKY</div>
          <div class="neighbor-detail-then-now">
            <span class="neighbor-detail-then">${dollar(kyThen.adjusted)}</span>
            <span class="neighbor-detail-arrow">\u2192</span>
            <span class="neighbor-detail-now">${dollar(kyCur.adjusted)}</span>
          </div>
          <div class="neighbor-detail-pct ${kyCls}">${kyPct !== null ? kySign + kyPct + '%' : 'N/A'}</div>
          <div class="neighbor-detail-sub">${kyThen.school_year || gradYear} vs. today</div>
        </div>
        <div class="neighbor-detail-card">
          <div class="neighbor-detail-state">${STATE_NAMES[selectedState] || selectedState}</div>
          <div class="neighbor-detail-then-now">
            <span class="neighbor-detail-then">${dollar(stThen.adjusted)}</span>
            <span class="neighbor-detail-arrow">\u2192</span>
            <span class="neighbor-detail-now">${dollar(stCur.adjusted)}</span>
          </div>
          <div class="neighbor-detail-pct ${stCls}">${stPct !== null ? stSign + stPct + '%' : 'N/A'}</div>
          <div class="neighbor-detail-sub">${stThen.school_year || gradYear} vs. today</div>
        </div>
      </div>
    `;
  }

  // ---- What a Teacher's Salary Actually Buys ----
  function renderCostOfLiving(gradYear, tch, tchNow) {
    const $salaryPct = document.getElementById('cost-salary-pct');
    const $rows = document.getElementById('cost-rows');
    const $total = document.getElementById('cost-total');
    const gy = String(gradYear);

    // Salary pct change at top of section
    const salPct = computePctChange(tch.adjusted, tchNow.adjusted);
    if (salPct !== null) {
      const salSign = salPct >= 0 ? '+' : '';
      const salCls = salPct >= 0 ? 'positive' : 'negative';
      $salaryPct.innerHTML = `
        <div class="cost-salary-pct-value ${salCls}">${salSign}${salPct}%</div>
        <div class="cost-salary-pct-label">statewide average salary change since you graduated</div>
      `;
    } else {
      $salaryPct.innerHTML = '';
    }

    if (!COST) {
      $rows.innerHTML = '';
      $total.textContent = '';
      return;
    }

    const then = COST.by_grad_year?.[gy] || {};
    const now = COST.current_year || {};
    const cats = COST.metadata?.categories || {};

    if (!then.data_available) {
      $rows.innerHTML = '<div class="no-data" style="background:rgba(255,255,255,0.06)"><div class="no-data-msg" style="color:var(--gray-muted)">Cost of living data isn\u2019t available for this graduation year.</div></div>';
      $total.textContent = '';
      return;
    }

    const items = [
      { key: 'rent', emoji: '\uD83C\uDFE0', label: 'Rent', monthlyNow: 1071 },
      { key: 'gas', emoji: '\u26FD', label: 'Gas', monthlyNow: 200 },
      { key: 'utilities', emoji: '\uD83D\uDD0C', label: 'Utilities', monthlyNow: 465 },
      { key: 'food', emoji: '\uD83D\uDED2', label: 'Groceries', monthlyNow: 600 },
    ];

    let html = '';
    items.forEach(item => {
      const thenAnnual = then[item.key + '_annual_adjusted'];
      const nowAnnual = cats[item.key]?.current_annual;
      if (thenAnnual == null || nowAnnual == null) return;

      const thenMonthly = Math.round(thenAnnual / 12);
      const nowMonthly = Math.round(nowAnnual / 12);
      const itemPct = computePctChange(thenAnnual, nowAnnual);
      const itemSign = itemPct !== null ? (itemPct >= 0 ? '+' : '') : '';
      const itemCls = itemPct !== null ? (itemPct >= 0 ? 'negative' : 'positive') : '';

      const thenPct = then[item.key + '_pct'];
      const nowPct = now[item.key + '_pct'];
      const thenWidth = thenPct != null ? Math.min(Math.round(thenPct * 100), 100) : 0;
      const nowWidth = nowPct != null ? Math.min(Math.round(nowPct * 100), 100) : 0;

      html += `
        <div class="cost-row">
          <span class="cost-emoji">${item.emoji}</span>
          <div class="cost-row-content">
            <div class="cost-row-label">${item.label}</div>
            <div class="cost-item-amounts">$${thenMonthly}/mo \u2192 $${nowMonthly}/mo</div>
            <div class="cost-item-pct ${itemCls}">${itemPct !== null ? itemSign + itemPct + '%' : ''}</div>
            <div class="cost-bars">
              <div class="cost-bar-group">
                <div class="cost-bar-label">THEN (% of salary)</div>
                <div class="cost-bar-track">
                  <div class="cost-bar-fill then-bar" style="width:${thenWidth}%">${thenPct != null ? Math.round(thenPct * 100) + '%' : ''}</div>
                </div>
              </div>
              <div class="cost-bar-group">
                <div class="cost-bar-label">NOW (% of salary)</div>
                <div class="cost-bar-track">
                  <div class="cost-bar-fill now-bar" style="width:${nowWidth}%">${nowPct != null ? Math.round(nowPct * 100) + '%' : ''}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    });

    $rows.innerHTML = html;

    const thenTotal = then.total_pct;
    const nowTotal = now.total_pct;
    if (thenTotal != null && nowTotal != null) {
      $total.textContent = `In ${then.grad_year ? then.grad_year - 1 + '\u2013' + then.grad_year : gradYear}, these basics cost ${Math.round(thenTotal * 100)}% of a teacher\u2019s salary. Today: ${Math.round(nowTotal * 100)}%.`;
    } else {
      $total.textContent = '';
    }
  }

  // ---- Who Sets The Budget? ----
  function renderBudget(gradYear, tch, tchNow, leg, legNow) {
    const $intro = document.getElementById('budget-intro');
    const $comp = document.getElementById('budget-comparison');
    const $narr = document.getElementById('budget-narrative');

    const tchPct = computePctChange(tch.adjusted, tchNow.adjusted);
    const legPct = computePctChange(leg.total_adjusted, legNow.total_adjusted);

    $intro.textContent = 'Kentucky legislators decide how much teachers get paid. So how has their own pay compared?';

    if (tchPct === null || legPct === null) {
      const tchHours = TEACHER?.metadata?.hours_basis || 1402;
      const legHours = LEGISLATOR?.metadata?.hours_basis || 480;
      const tchHourly = tchNow.hourly_rate || (tchNow.adjusted ? (tchNow.adjusted / tchHours).toFixed(2) : null);
      const legHourly = legNow.hourly_rate || (legNow.total_adjusted ? (legNow.total_adjusted / legHours).toFixed(2) : null);

      $comp.innerHTML = `
        <div class="budget-card">
          <div class="budget-card-role">TEACHER</div>
          <div class="budget-card-pct">${tchHourly ? dollar(tchHourly) + '<span class="budget-card-per">/hr</span>' : 'N/A'}</div>
          <div class="budget-card-detail">187 days/year</div>
        </div>
        <div class="budget-card">
          <div class="budget-card-role">LEGISLATOR</div>
          <div class="budget-card-pct">${legHourly ? dollar(legHourly) + '<span class="budget-card-per">/hr</span>' : 'N/A'}</div>
          <div class="budget-card-detail">60 session days/year</div>
        </div>
      `;
      $narr.textContent = '';
      return;
    }

    $comp.innerHTML = `
      <div class="budget-card">
        <div class="budget-card-role">RAISES PASSED FOR TEACHERS</div>
        <div class="budget-card-pct negative">0</div>
        <div class="budget-card-detail">no legislated pay raises</div>
      </div>
      <div class="budget-card">
        <div class="budget-card-role">RAISES PASSED FOR THEMSELVES</div>
        <div class="budget-card-pct positive">+8%<span class="budget-card-per"> &amp; </span>+9%</div>
        <div class="budget-card-detail">two raises they voted themselves</div>
      </div>
    `;

    let narrative = `Legislators voted themselves an 8% raise in 2023 and another 9% in 2025. Meanwhile, teacher pay has fallen ${Math.abs(tchPct)}% since you graduated after adjusting for inflation.`;
    narrative += ' They set the budget. They set their own pay.';

    $narr.textContent = narrative;
  }

  function renderMessage(gradYear, tch, tchNow) {
    const $box = document.getElementById('message-box');
    const tchPct = computePctChange(tch.adjusted, tchNow.adjusted);

    let msg = `Since I graduated in ${gradYear}`;
    if (tchPct !== null) msg += `, teacher pay in Kentucky has changed by ${tchPct > 0 ? '+' : ''}${tchPct}% in real dollars`;
    msg += `. I\u2019m asking you to prioritize funding for the people who work in our schools every day. Kentucky students deserve better.`;

    $box.textContent = msg;
  }

  // ---- Sticky Share Bar ----
  function setupStickyBar(gradYear, tch, tchNow) {
    if (stickyDismissed) return;

    const pctChange = computePctChange(tch.adjusted, tchNow.adjusted);
    if (pctChange === null) return;

    const sign = pctChange >= 0 ? '+' : '';
    document.getElementById('sticky-share-stat').textContent = `${sign}${pctChange}% teacher pay`;

    const heroSection = document.getElementById('section-hero-stat');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!stickyDismissed) {
          if (!entry.isIntersecting) {
            $stickyBar.classList.remove('hidden');
            $stickyBar.classList.add('visible');
          } else {
            $stickyBar.classList.remove('visible');
            $stickyBar.classList.add('hidden');
          }
        }
      });
    }, { threshold: 0 });

    observer.observe(heroSection);
  }

  // ---- Scroll Reveals ----
  let revealObserver = null;

  function setupScrollReveals() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    // Reset all reveal elements
    document.querySelectorAll('.reveal').forEach(el => {
      el.classList.remove('revealed');
    });

    // Disconnect previous observer if exists
    if (revealObserver) revealObserver.disconnect();

    revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });

    document.querySelectorAll('.reveal').forEach(el => {
      revealObserver.observe(el);
    });
  }

  // ---- Count-Up Animation ----
  function animateCount(el, target) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      const sign = target >= 0 ? '+' : '';
      el.textContent = `${sign}${target}%`;
      return;
    }

    const duration = 1500;
    const start = performance.now();
    const sign = target >= 0 ? '+' : '';

    function tick(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(target * eased);
      el.textContent = `${current >= 0 && target >= 0 ? '+' : ''}${current}%`;

      if (progress < 1) {
        requestAnimationFrame(tick);
      } else {
        el.textContent = `${sign}${target}%`;
      }
    }

    requestAnimationFrame(tick);
  }

  // ---- Share Card Generation ----
  function generateShareCard() {
    if (typeof html2canvas === 'undefined') return;

    const heroSection = document.getElementById('section-hero-stat');
    if (!heroSection) return;

    html2canvas(heroSection, {
      width: 1200,
      height: 630,
      scale: 2,
      backgroundColor: '#FFFFFF',
      useCORS: true,
      windowWidth: 1200,
      windowHeight: 630,
      onclone: function (clonedDoc) {
        const el = clonedDoc.getElementById('section-hero-stat');
        if (el) {
          el.style.width = '1200px';
          el.style.minHeight = '630px';
          el.style.display = 'flex';
          el.style.alignItems = 'center';
          el.style.justifyContent = 'center';
          el.style.padding = '80px 120px';
        }
      },
    }).then(canvas => {
      canvas.toBlob(blob => {
        if (blob) shareCardBlob = blob;
      }, 'image/png');
    }).catch(() => {});
  }

  function getShareText() {
    const gy = window.location.hash.match(/year=(\d{4})/);
    if (gy) {
      const year = gy[1];
      const tch = TEACHER?.by_grad_year?.[year];
      if (tch && tch.data_available) {
        const tchPct = computePctChange(tch.adjusted, TEACHER.current_year.adjusted);
        if (tchPct !== null) {
          const verb = tchPct < 0 ? 'dropped' : 'grew';
          return `Since I graduated in ${year}, Kentucky teacher pay ${verb} ${Math.abs(tchPct)}%. See your year #WhenIWasInSchool`;
        }
      }
    }
    return 'See how much Kentucky teacher pay has changed since you graduated. #WhenIWasInSchool';
  }

  // ---- Share ----
  function shareResults() {
    const url = window.location.href;
    const text = getShareText();

    if (navigator.share) {
      const shareData = { title: 'When I Was in School', text, url };

      // Include share card image if available and supported
      if (shareCardBlob && navigator.canShare) {
        const file = new File([shareCardBlob], 'when-i-was-in-school.png', { type: 'image/png' });
        const withFile = { ...shareData, files: [file] };
        if (navigator.canShare(withFile)) {
          navigator.share(withFile).catch(() => {});
          return;
        }
      }

      navigator.share(shareData).catch(() => {});
    } else {
      navigator.clipboard.writeText(`${text} ${url}`).then(() => {
        $shareBtn.textContent = 'LINK COPIED!';
        setTimeout(() => { $shareBtn.textContent = 'SHARE YOUR RESULTS'; }, 2000);
      }).catch(() => {
        prompt('Copy this link to share:', `${text} ${url}`);
      });
    }
  }

  function copyMessage() {
    const $box = document.getElementById('message-box');
    navigator.clipboard.writeText($box.textContent).then(() => {
      $copyMsg.textContent = 'COPIED!';
      setTimeout(() => { $copyMsg.textContent = 'COPY MESSAGE'; }, 2000);
    }).catch(() => {
      const range = document.createRange();
      range.selectNode($box);
      window.getSelection().removeAllRanges();
      window.getSelection().addRange(range);
    });
  }

  // ---- Helpers ----

  function computePctChange(thenVal, nowVal) {
    if (thenVal == null || nowVal == null || thenVal === 0) return null;
    return Math.round(((nowVal - thenVal) / thenVal) * 100);
  }

  function ordinal(n) {
    const s = ['th', 'st', 'nd', 'rd'];
    const v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
  }

  function noDataBlock(gradYear, category, earliestYear) {
    if (gradYear < 1980) {
      return `<div class="no-data">
        <div class="no-data-title">Well, you\u2019ve got us there.</div>
        <div class="no-data-msg">Kentucky didn\u2019t start tracking ${category} data until around ${earliestYear}. Here\u2019s the earliest snapshot we have.</div>
      </div>`;
    }
    return `<div class="no-data">
      <div class="no-data-msg">${category.charAt(0).toUpperCase() + category.slice(1)} data isn\u2019t available for ${gradYear}. The earliest we have is ${earliestYear}.</div>
    </div>`;
  }

  function dollar(val) {
    if (val == null) return 'N/A';
    const n = parseFloat(val);
    if (isNaN(n)) return 'N/A';
    if (n >= 1000) return '$' + Math.round(n).toLocaleString('en-US');
    return '$' + n.toFixed(2);
  }

  // ---- Go ----
  init().catch(err => console.error('Init failed:', err));
})();
