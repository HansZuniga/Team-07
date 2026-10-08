(() => {
  'use strict';

  const EXAMPLE = 'printf("This is an example");\nint a = 10;';
  const source = document.getElementById('sourceCode');
  const analyzeBtn = document.getElementById('analyzeBtn');
  const exampleBtn = document.getElementById('exampleBtn');
  const clearBtn = document.getElementById('clearBtn');
  const fileBtn = document.getElementById('fileBtn');
  const fileInput = document.getElementById('fileInput');
  const tokenBody = document.getElementById('tokenBody');
  const errorBody = document.getElementById('errorBody');
  const errorsPanel = document.getElementById('errorsPanel');
  const tokenTotal = document.getElementById('tokenTotal');
  const errorTotal = document.getElementById('errorTotal');
  const analysisStatus = document.getElementById('analysisStatus');
  const message = document.getElementById('message');
  const charCount = document.getElementById('charCount');

  const setMessage = (text = '', isError = false) => {
    message.textContent = text;
    message.classList.toggle('error', isError);
  };

  const updateCount = () => {
    charCount.textContent = `${source.value.length.toLocaleString()} / 50,000`;
  };

  const addCell = (row, text, className = '') => {
    const cell = document.createElement('td');
    cell.textContent = String(text);
    if (className) cell.className = className;
    row.appendChild(cell);
  };

  const renderTokens = (tokens) => {
    tokenBody.replaceChildren();
    if (!tokens.length) {
      const row = document.createElement('tr');
      row.className = 'empty-row';
      const cell = document.createElement('td');
      cell.colSpan = 4;
      cell.textContent = 'No valid tokens were recognized.';
      row.appendChild(cell);
      tokenBody.appendChild(row);
      return;
    }

    tokens.forEach((token) => {
      const row = document.createElement('tr');
      const typeCell = document.createElement('td');
      const badge = document.createElement('span');
      badge.className = 'type-badge';
      badge.textContent = token.type;
      typeCell.appendChild(badge);
      row.appendChild(typeCell);
      addCell(row, token.lexeme);
      addCell(row, token.line);
      addCell(row, token.column);
      tokenBody.appendChild(row);
    });
  };

  const renderErrors = (errors) => {
    errorBody.replaceChildren();
    errorsPanel.hidden = errors.length === 0;
    errors.forEach((error) => {
      const row = document.createElement('tr');
      addCell(row, error.lexeme, 'error-lexeme');
      addCell(row, error.line);
      addCell(row, error.column);
      errorBody.appendChild(row);
    });
  };

  const analyze = async () => {
    const text = source.value;
    if (!text.trim()) {
      tokenTotal.textContent = '0';
      errorTotal.textContent = '0';
      analysisStatus.textContent = 'Waiting for input';
      renderTokens([]);
      renderErrors([]);
      setMessage('Enter source code before running the lexical analysis.', true);
      source.focus();
      return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = 'Analyzing…';
    analysisStatus.textContent = 'Processing';
    setMessage('Running the original Team 07 Python lexer…');

    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source: text })
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok || !data.ok) throw new Error(data.message || 'Analysis failed.');

      renderTokens(data.tokens || []);
      renderErrors(data.errors || []);
      tokenTotal.textContent = data.total_tokens;
      errorTotal.textContent = data.total_errors;
      analysisStatus.textContent = data.total_errors ? 'Completed with errors' : 'Completed';
      setMessage(data.total_errors ? `${data.total_errors} lexical error(s) detected. Scanning continued.` : 'No lexical errors detected.');
      document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (error) {
      analysisStatus.textContent = 'Error';
      setMessage(error.message || 'The analyzer could not process the request.', true);
    } finally {
      analyzeBtn.disabled = false;
      analyzeBtn.textContent = 'Analyze Code';
    }
  };

  source.addEventListener('input', updateCount);
  analyzeBtn.addEventListener('click', analyze);
  source.addEventListener('keydown', (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') analyze();
  });

  exampleBtn.addEventListener('click', () => {
    source.value = EXAMPLE;
    updateCount();
    setMessage('Professor example loaded.');
    source.focus();
  });

  clearBtn.addEventListener('click', () => {
    source.value = '';
    updateCount();
    tokenTotal.textContent = '—';
    errorTotal.textContent = '—';
    analysisStatus.textContent = 'Ready';
    renderTokens([]);
    renderErrors([]);
    setMessage('');
    source.focus();
  });

  fileBtn.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', async () => {
    const file = fileInput.files && fileInput.files[0];
    if (!file) return;
    if (file.size > 50_000) {
      setMessage('The selected file is larger than the 50,000-character analysis limit.', true);
      fileInput.value = '';
      return;
    }
    try {
      source.value = await file.text();
      updateCount();
      setMessage(`Loaded ${file.name}.`);
      source.focus();
    } catch (_) {
      setMessage('The selected file could not be read as text.', true);
    } finally {
      fileInput.value = '';
    }
  });

  updateCount();
})();
