/* quiz.js – handles answer tracking, form submission, and result rendering */

(function () {
  'use strict';

  const form        = document.getElementById('quiz-form');
  const submitBtn   = document.getElementById('submit-btn');
  const submitHint  = document.getElementById('submit-hint');
  const quizSection = document.getElementById('quiz-section');
  const resultSection = document.getElementById('result-section');
  const followupSection = document.getElementById('followup-section');
  const followupForm = document.getElementById('followup-form');
  const followupContainer = document.getElementById('followup-questions-container');
  const followupSubmitBtn = document.getElementById('followup-submit-btn');
  const followupHint = document.getElementById('followup-hint');

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

  // Preserve round-1 answers + context across the two-round flow.
  var savedAnswers = null;
  var savedContext = '';

  // ── Answer tracking (main quiz) ────────────────────────────────────────────
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

  // ── Follow-up answer tracking ──────────────────────────────────────────────
  var followupAnswered = new Set();
  var followupTotal = 0;

  followupForm.addEventListener('change', function (e) {
    if (e.target.type !== 'radio') return;

    const block = e.target.closest('.question-block');
    if (block) {
      block.classList.add('answered');
      followupAnswered.add(block.dataset.qid);
    }

    const allAnswered = followupAnswered.size === followupTotal;
    followupSubmitBtn.disabled = !allAnswered;
    followupHint.hidden = allAnswered;
  });

  // ── Main form submission (round 1) ─────────────────────────────────────────
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

    // Save for potential round 2.
    savedAnswers = answers;
    savedContext = context;

    submitBtn.disabled = true;
    submitBtn.textContent = 'Diagnosing…';

    try {
      const res = await fetch('/diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers: answers, context: context }),
      });

      if (!res.ok) {
        const err = await res.json().catch(function () { return {}; });
        throw new Error(err.error || 'Server error (' + res.status + ')');
      }

      const data = await res.json();

      if (data.needs_followup) {
        showFollowup(data.followup_questions);
      } else {
        showResult(data);
      }
    } catch (err) {
      showError(err.message || 'Something went wrong. Please try again.');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Diagnose my block';
    }
  });

  // ── Follow-up form submission (round 2) ────────────────────────────────────
  followupForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    hideError();

    // Validate all follow-up questions are answered.
    var allAnswered = followupAnswered.size === followupTotal;
    if (!allAnswered) {
      showError('Please answer all questions to continue.');
      return;
    }

    const followupAnswers = {};
    followupContainer.querySelectorAll('.question-block').forEach(function (block) {
      const qid = block.dataset.qid;
      const checked = block.querySelector('input[type="radio"]:checked');
      if (checked) followupAnswers[qid] = parseInt(checked.value, 10);
    });

    followupSubmitBtn.disabled = true;
    followupSubmitBtn.textContent = 'Diagnosing…';

    try {
      const res = await fetch('/diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          answers: savedAnswers,
          context: savedContext,
          followup_answers: followupAnswers,
        }),
      });

      if (!res.ok) {
        const err = await res.json().catch(function () { return {}; });
        throw new Error(err.error || 'Server error (' + res.status + ')');
      }

      const data = await res.json();
      showResult(data);
    } catch (err) {
      showError(err.message || 'Something went wrong. Please try again.');
      followupSubmitBtn.disabled = false;
      followupSubmitBtn.textContent = 'Get my diagnosis';
    }
  });

  // ── Render follow-up questions ─────────────────────────────────────────────
  function showFollowup(questions) {
    followupContainer.innerHTML = '';
    followupAnswered.clear();
    followupTotal = questions.length;
    followupSubmitBtn.disabled = true;
    followupHint.hidden = false;

    questions.forEach(function (q, idx) {
      var fieldset = document.createElement('fieldset');
      fieldset.className = 'question-block';
      fieldset.id = 'block-' + q.id;
      fieldset.dataset.qid = q.id;

      var legend = document.createElement('legend');
      legend.className = 'question-text';
      var numSpan = document.createElement('span');
      numSpan.className = 'q-num';
      numSpan.textContent = (idx + 1) + '/' + questions.length;
      legend.appendChild(numSpan);
      legend.appendChild(document.createTextNode(' ' + q.text));
      fieldset.appendChild(legend);

      var ul = document.createElement('ul');
      ul.className = 'options-list';
      ul.setAttribute('role', 'radiogroup');

      q.options.forEach(function (opt, optIdx) {
        var li = document.createElement('li');
        var label = document.createElement('label');
        label.className = 'option-label';

        var radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = q.id;
        radio.value = String(optIdx);
        radio.required = true;

        var span = document.createElement('span');
        span.className = 'option-text';
        span.textContent = opt.text;

        label.appendChild(radio);
        label.appendChild(span);
        li.appendChild(label);
        ul.appendChild(li);
      });

      fieldset.appendChild(ul);
      followupContainer.appendChild(fieldset);
    });

    quizSection.hidden = true;
    followupSection.hidden = false;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

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
    followupSection.hidden = true;
    resultSection.hidden = false;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // ── Retake ─────────────────────────────────────────────────────────────────
  retakeBtn.addEventListener('click', function () {
    form.reset();
    answered.clear();
    savedAnswers = null;
    savedContext = '';
    followupAnswered.clear();
    followupTotal = 0;
    followupContainer.innerHTML = '';
    document.querySelectorAll('#quiz-form .question-block').forEach(function (b) {
      b.classList.remove('answered');
    });
    submitBtn.disabled = true;
    submitBtn.textContent = 'Diagnose my block';
    submitHint.hidden = false;
    resultSection.hidden = true;
    followupSection.hidden = true;
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
