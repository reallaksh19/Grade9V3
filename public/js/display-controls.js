/**
 * Grade9V3 Display & Accessibility Controls
 * Manages global font adjustment and UI zoom scale across all pages and explorers.
 * Persists preferences in localStorage ('grade9v3_font_scale', 'grade9v3_ui_scale').
 * Synchronizes in real-time across tabs via storage event.
 */

(function () {
  'use strict';

  const STORAGE_KEY_FONT = 'grade9v3_font_scale';
  const STORAGE_KEY_SCALE = 'grade9v3_ui_scale';

  let fontScale = 1.0;
  let uiScale = 1.0;

  // Read saved preferences
  try {
    const savedFont = localStorage.getItem(STORAGE_KEY_FONT);
    if (savedFont) {
      const parsed = parseFloat(savedFont);
      if (!isNaN(parsed) && parsed >= 0.75 && parsed <= 1.6) fontScale = parsed;
    }
    const savedScale = localStorage.getItem(STORAGE_KEY_SCALE);
    if (savedScale) {
      const parsed = parseFloat(savedScale);
      if (!isNaN(parsed) && parsed >= 0.7 && parsed <= 1.5) uiScale = parsed;
    }
  } catch (e) {
    console.warn('Grade9V3: localStorage unavailable for display preferences', e);
  }

  function applyDisplaySettings() {
    // 1. Apply Font Scale
    document.documentElement.style.setProperty('--font-scale', fontScale.toString());
    document.documentElement.style.fontSize = (16 * fontScale) + 'px';

    // 2. Apply UI Zoom Scale
    document.documentElement.style.setProperty('--ui-scale', uiScale.toString());
    if (document.body) {
      document.body.style.zoom = uiScale.toString();
    }

    // 3. Update active UI controls if rendered
    updateWidgetUI();
  }

  function setFontScale(scale, save = true) {
    fontScale = Math.max(0.75, Math.min(1.6, parseFloat(scale)));
    if (save) {
      try { localStorage.setItem(STORAGE_KEY_FONT, fontScale.toFixed(2)); } catch (e) {}
    }
    applyDisplaySettings();
  }

  function setUiScale(scale, save = true) {
    uiScale = Math.max(0.7, Math.min(1.5, parseFloat(scale)));
    if (save) {
      try { localStorage.setItem(STORAGE_KEY_SCALE, uiScale.toFixed(2)); } catch (e) {}
    }
    applyDisplaySettings();
  }

  function resetDisplay() {
    setFontScale(1.0);
    setUiScale(1.0);
  }

  // Cross-tab synchronization
  window.addEventListener('storage', (e) => {
    if (e.key === STORAGE_KEY_FONT && e.newValue) {
      setFontScale(parseFloat(e.newValue), false);
    } else if (e.key === STORAGE_KEY_SCALE && e.newValue) {
      setUiScale(parseFloat(e.newValue), false);
    }
  });

  // Apply immediately upon script execution
  applyDisplaySettings();

  // Re-apply once body is loaded to ensure body.style.zoom is set
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWidget);
  } else {
    initWidget();
  }

  function updateWidgetUI() {
    const fontSlider = document.getElementById('g9-font-slider');
    const fontLabel = document.getElementById('g9-font-val');
    const scaleSlider = document.getElementById('g9-scale-slider');
    const scaleLabel = document.getElementById('g9-scale-val');

    if (fontSlider) fontSlider.value = fontScale;
    if (fontLabel) fontLabel.textContent = Math.round(fontScale * 100) + '%';
    if (scaleSlider) scaleSlider.value = uiScale;
    if (scaleLabel) scaleLabel.textContent = Math.round(uiScale * 100) + '%';
  }

  function initWidget() {
    applyDisplaySettings();

    // Prevent duplicate injection
    if (document.getElementById('g9-display-widget-root')) return;

    // Inject CSS for the display widget
    const style = document.createElement('style');
    style.id = 'g9-display-widget-styles';
    style.textContent = `
      #g9-display-widget-root {
        position: fixed;
        bottom: 18px;
        right: 18px;
        z-index: 99999;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      }
      .g9-display-trigger {
        background: #161b22;
        border: 1px solid #444c56;
        color: #f0f6fc;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.5);
        transition: all 0.2s ease;
        backdrop-filter: blur(8px);
      }
      .g9-display-trigger:hover {
        background: #21262d;
        border-color: #58a6ff;
        color: #58a6ff;
        transform: translateY(-1px);
      }
      .g9-display-popover {
        position: absolute;
        bottom: 38px;
        right: 0;
        width: 270px;
        background: #161b22;
        border: 1px solid #444c56;
        border-radius: 8px;
        padding: 14px 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.6);
        display: none;
        flex-direction: column;
        gap: 12px;
        z-index: 100000;
        backdrop-filter: blur(12px);
      }
      .g9-display-popover.active {
        display: flex;
      }
      .g9-popover-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(68, 76, 86, 0.5);
        padding-bottom: 6px;
      }
      .g9-popover-title {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #9aa4b2;
        display: flex;
        align-items: center;
        gap: 5px;
      }
      .g9-control-row {
        display: flex;
        flex-direction: column;
        gap: 4px;
      }
      .g9-control-label-wrap {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 11px;
        font-weight: 600;
        color: #c9d1d9;
      }
      .g9-val-badge {
        font-family: ui-monospace, monospace;
        color: #58a6ff;
        font-weight: 700;
      }
      .g9-slider {
        width: 100%;
        accent-color: #58a6ff;
        cursor: pointer;
        height: 6px;
      }
      .g9-btn-pill-row {
        display: flex;
        gap: 4px;
        margin-top: 2px;
      }
      .g9-pill {
        background: #21262d;
        border: 1px solid #30363d;
        color: #9aa4b2;
        padding: 2px 7px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.1s ease;
        flex: 1;
        text-align: center;
      }
      .g9-pill:hover {
        background: #2d333b;
        color: #58a6ff;
        border-color: #58a6ff;
      }
      .g9-reset-btn {
        background: transparent;
        border: 1px solid #30363d;
        color: #9aa4b2;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
        cursor: pointer;
        align-self: flex-end;
        transition: all 0.15s;
      }
      .g9-reset-btn:hover {
        background: rgba(248, 81, 73, 0.1);
        border-color: #f85149;
        color: #ff7b72;
      }
    `;
    document.head.appendChild(style);

    // Create widget container
    const container = document.createElement('div');
    container.id = 'g9-display-widget-root';

    container.innerHTML = `
      <button class="g9-display-trigger" id="g9-display-toggle-btn" title="Global Display & Accessibility (Font & UI Scale)">
        <span>🔤 / 🔍</span>
        <span>Display</span>
      </button>

      <div class="g9-display-popover" id="g9-display-popover">
        <div class="g9-popover-header">
          <span class="g9-popover-title">⚙️ Display &amp; Scale</span>
          <button class="g9-reset-btn" id="g9-btn-reset" title="Reset Font &amp; Scale to 100%">Reset</button>
        </div>

        <!-- Font Size Slider -->
        <div class="g9-control-row">
          <div class="g9-control-label-wrap">
            <span>🔤 Global Font Size</span>
            <span class="g9-val-badge" id="g9-font-val">100%</span>
          </div>
          <input type="range" class="g9-slider" id="g9-font-slider" min="0.80" max="1.45" step="0.05" value="1.0">
          <div class="g9-btn-pill-row">
            <button class="g9-pill" data-font="0.85">85%</button>
            <button class="g9-pill" data-font="1.00">100%</button>
            <button class="g9-pill" data-font="1.15">115%</button>
            <button class="g9-pill" data-font="1.30">130%</button>
          </div>
        </div>

        <!-- UI Zoom Scale Slider -->
        <div class="g9-control-row">
          <div class="g9-control-label-wrap">
            <span>🔍 Global UI Zoom</span>
            <span class="g9-val-badge" id="g9-scale-val">100%</span>
          </div>
          <input type="range" class="g9-slider" id="g9-scale-slider" min="0.75" max="1.35" step="0.05" value="1.0">
          <div class="g9-btn-pill-row">
            <button class="g9-pill" data-scale="0.80">80%</button>
            <button class="g9-pill" data-scale="0.90">90%</button>
            <button class="g9-pill" data-scale="1.00">100%</button>
            <button class="g9-pill" data-scale="1.20">120%</button>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(container);

    // Event handlers
    const toggleBtn = document.getElementById('g9-display-toggle-btn');
    const popover = document.getElementById('g9-display-popover');
    const fontSlider = document.getElementById('g9-font-slider');
    const scaleSlider = document.getElementById('g9-scale-slider');
    const resetBtn = document.getElementById('g9-btn-reset');

    toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      popover.classList.toggle('active');
    });

    document.addEventListener('click', (e) => {
      if (!container.contains(e.target)) {
        popover.classList.remove('active');
      }
    });

    fontSlider.addEventListener('input', (e) => {
      setFontScale(e.target.value);
    });

    scaleSlider.addEventListener('input', (e) => {
      setUiScale(e.target.value);
    });

    resetBtn.addEventListener('click', () => {
      resetDisplay();
    });

    // Preset pills
    container.querySelectorAll('.g9-pill').forEach(pill => {
      pill.addEventListener('click', (e) => {
        if (pill.dataset.font) {
          setFontScale(pill.dataset.font);
        } else if (pill.dataset.scale) {
          setUiScale(pill.dataset.scale);
        }
      });
    });

    // Initial update
    updateWidgetUI();
  }

  // Expose global API
  window.Grade9Display = {
    setFontScale,
    setUiScale,
    resetDisplay,
    getFontScale: () => fontScale,
    getUiScale: () => uiScale
  };
})();
