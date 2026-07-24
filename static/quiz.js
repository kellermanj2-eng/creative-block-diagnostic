/* quiz.js – handles answer tracking, form submission, and result rendering */

(function () {
  'use strict';

  const form        = document.getElementById('quiz-form');
  const submitBtn   = document.getElementById('submit-btn');
  const submitHint  = document.getElementById('submit-hint');
  const quizSection = document.getElementById('quiz-section');
  const resultSection = document.getElementById('result-section');

  const resultName   = document.getElementById('result-name');
  const resultDesc   = document.getElementById('result-description');
  const resultExercise = document.getElementById('result-exercise');
  const resultPersonalization = document.getElementById('result-personalization');
  const resultConfidence = document.getElementById('result-confidence');
  const resultContributingWrap = document.getElementById('result-contributing-wrap');
  const resultContributingText = document.getElementById('result-contributing-text');
  const resultSecondaryWrap = document.getElementById('result-secondary-wrap');
  const resultSecondaryName = document.getElementById('result-secondary-name');
  const retakeBtn    = document.getElementById('retake-btn');

  const errorBanner  = document.getElementById('error-banner');
  const errorMessage = document.getElementById('error-message');
  const errorDismiss = document.getElementById('error-dismiss');

  // Track which questions have been answered.
  const answered = new Set();
  const totalQuestions = document.querySelectorAll('.question-block').length;

  // ── Answer tracking ────────────────────────────────────────────────────────
  form.addEventListener('change', function (e) {
    if (e.target.type !== 'radio') return;

    const block = e.target.closest('.question-block');
    if (block) {
      block.classList.add('answered');
      answered.add(block.dataset.qid);
    }

    const allAnswered = answered.size === totalQuestions;
    submitBtn.disabled = !allAnswered;
    submitHint.hidden = allAnswered;
  });

  // ── Form submission ────────────────────────────────────────────────────────
  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    hideError();

    const answers = {};
    document.querySelectorAll('.question-block').forEach(function (block) {
      const qid = block.dataset.qid;
      const checked = block.querySelector('input[type="radio"]:checked');
      if (checked) answers[qid] = parseInt(checked.value, 10);
    });

    const context = (document.getElementById('context-input').value || '').trim();

    submitBtn.disabled = true;
    submitBtn.textContent = 'Diagnosing…';

    try {
      const res = await fetch('/diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers, context }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error || 'Server error (' + res.status + ')');
      }

      const data = await res.json();
      showResult(data);
    } catch (err) {
      showError(err.message || 'Something went wrong. Please try again.');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Diagnose my block';
    }
  });

  // ── Render result ──────────────────────────────────────────────────────────
  function showResult(data) {
    resultName.textContent    = data.primary_name;
    resultDesc.textContent    = data.primary_description;
    resultExercise.textContent = data.exercise;
    resultPersonalization.textContent = data.personalization || '';

    // Confidence badge
    var confLabel = data.confidence || '';
    var confClass = confLabel.startsWith('high') ? 'high'
                  : confLabel.startsWith('moderate') ? 'moderate'
                  : 'mixed';
    resultConfidence.textContent = confLabel;
    resultConfidence.className = 'confidence-badge ' + confClass;

    // Contributing answers
    var contributors = data.contributing_answers || [];
    if (contributors.length > 0) {
      var qNums = contributors.map(function (c) {
        // Extract the question number from the qid (e.g. "q3" → "3")
        var num = c.qid.replace(/\D/g, '');
        return 'Q' + num;
      });
      var qList = qNums.length === 1
        ? qNums[0]
        : qNums.slice(0, -1).join(', ') + ' and ' + qNums[qNums.length - 1];
      resultContributingText.textContent =
        'Your answers to ' + qList + ' were the strongest signal for this diagnosis.';
      resultContributingWrap.hidden = false;
    } else {
      resultContributingWrap.hidden = true;
    }

    if (data.secondary && data.secondary_name) {
      resultSecondaryName.textContent = data.secondary_name;
      resultSecondaryWrap.hidden = false;
    } else {
      resultSecondaryWrap.hidden = true;
    }

    quizSection.hidden  = true;
    resultSection.hidden = false;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // ── Retake ─────────────────────────────────────────────────────────────────
  retakeBtn.addEventListener('click', function () {
    form.reset();
    answered.clear();
    document.querySelectorAll('.question-block').forEach(function (b) {
      b.classList.remove('answered');
    });
    submitBtn.disabled = true;
    submitBtn.textContent = 'Diagnose my block';
    submitHint.hidden = false;
    resultSection.hidden = true;
    quizSection.hidden   = false;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // ── Error helpers ──────────────────────────────────────────────────────────
  function showError(msg) {
    errorMessage.textContent = msg;
    errorBanner.hidden = false;
  }

  function hideError() {
    errorBanner.hidden = true;
  }

  errorDismiss.addEventListener('click', hideError);

}());
