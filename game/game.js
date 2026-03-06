/**
 * Pictura — Daily Nonogram Game
 *
 * Core game engine: canvas rendering, input handling, puzzle logic,
 * streak tracking, completion flow.
 */

(function () {
  'use strict';

  // ==================== CONFIG ====================
  const GRID_SIZE = 10;
  const CLUE_AREA_RATIO = 0.28; // fraction of canvas for clue headers
  const CELL_BORDER = 1;
  const THICK_BORDER = 2;
  const THICK_EVERY = 5;
  const ERROR_FLASH_MS = 400;
  const POINTER_SAMPLE_HZ = 5; // Hz for pointer sampling

  // ==================== STATE ====================
  const state = {
    puzzle: null,         // current puzzle data
    grid: null,           // player grid: 'empty' | 'filled' | 'marked_x'
    tool: 'fill',         // current tool
    completed: false,
    startTime: 0,
    actionCount: 0,
    errorCount: 0,
    eraseCount: 0,
    hintCount: 0,
    isDragging: false,
    dragTool: null,
    lastActionTime: 0,
    hoverCell: null,
    hoverStartTime: 0,
    errorCells: new Map(), // cell key -> error number
    errorTimestamps: new Map(), // error number -> timestamp
    nextErrorNumber: 1,
    streak: { current: 0, longest: 0, lastPlayDate: null },
    stats: { played: 0, totalTime: 0 },
  };

  // ==================== CANVAS ====================
  const canvas = document.getElementById('grid-canvas');
  const ctx = canvas.getContext('2d');
  let cellSize = 0;
  let clueWidth = 0;
  let clueHeight = 0;
  let gridOriginX = 0;
  let gridOriginY = 0;
  let dpr = 1;

  // ==================== PUZZLE LOADING ====================
  async function loadPuzzle() {
    // Try loading today's puzzle, fallback to a demo puzzle
    const today = new Date().toISOString().slice(0, 10);
    document.getElementById('date-display').textContent = formatDate(today);

    try {
      const resp = await fetch(`puzzles/${today}.json`);
      if (resp.ok) {
        state.puzzle = await resp.json();
        initGame();
        return;
      }
    } catch (e) { /* fallback */ }

    // Try loading any available puzzle
    try {
      const resp = await fetch('puzzles/index.json');
      if (resp.ok) {
        const index = await resp.json();
        if (index.length > 0) {
          // Pick puzzle based on day number
          const dayNum = Math.floor(Date.now() / 86400000);
          const puzzleFile = index[dayNum % index.length];
          const puzzleResp = await fetch(`puzzles/${puzzleFile}`);
          if (puzzleResp.ok) {
            state.puzzle = await puzzleResp.json();
            initGame();
            return;
          }
        }
      }
    } catch (e) { /* fallback */ }

    // Hardcoded demo puzzle (heart)
    state.puzzle = getDemoPuzzle();
    initGame();
  }

  function getDemoPuzzle() {
    return {
      id: 'demo',
      title: 'Heart',
      category: 'symbol',
      difficulty: 'easy',
      grid_size: [10, 10],
      fill_ratio: 0.52,
      sweep_count: 3,
      solution: [
        [0,0,1,1,0,0,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,0,0,0],
        [0,0,0,0,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
      ],
      row_clues: [[2,2],[8],[10],[10],[10],[8],[6],[4],[2],[0]],
      col_clues: [[2],[3],[7],[8],[9],[9],[8],[7],[3],[2]],
      image_colors: { filled: '#E74C3C', background: '#FFFFFF' },
    };
  }

  // ==================== INIT ====================
  function initGame() {
    const p = state.puzzle;
    const rows = p.grid_size[0];
    const cols = p.grid_size[1];

    // Initialize player grid
    state.grid = [];
    for (let r = 0; r < rows; r++) {
      state.grid[r] = [];
      for (let c = 0; c < cols; c++) {
        state.grid[r][c] = 'empty';
      }
    }

    // Check for saved progress
    const saved = loadProgress();
    if (saved && saved.puzzleId === p.id) {
      state.grid = saved.grid;
      state.actionCount = saved.actionCount || 0;
      state.errorCount = saved.errorCount || 0;
      state.startTime = performance.now() - (saved.elapsedMs || 0);
    } else {
      state.startTime = performance.now();
      state.actionCount = 0;
      state.errorCount = 0;
      state.eraseCount = 0;
    }

    state.completed = false;

    // Load streak
    loadStreak();
    updateStreakDisplay();

    // Load stats
    loadStats();

    // Size canvas
    sizeCanvas();

    // Emit telemetry
    if (typeof Telemetry !== 'undefined') {
      Telemetry.emit('SESSION_START', {
        referrer: document.referrer,
        user_agent: navigator.userAgent,
        timezone_offset_min: new Date().getTimezoneOffset(),
        is_returning_user: !!localStorage.getItem('pictura_user_id'),
        current_streak: state.streak.current,
        total_puzzles_completed: state.stats.played,
      });

      Telemetry.emit('PUZZLE_START', {
        puzzle_grid_rows: rows,
        puzzle_grid_cols: cols,
        total_filled_cells: p.solution.flat().reduce((a, b) => a + b, 0),
        clue_complexity: [...p.row_clues, ...p.col_clues].reduce((s, c) => s + c.length, 0),
      });

      // Streak update
      Telemetry.emit('STREAK_UPDATE', {
        current_streak: state.streak.current,
        longest_streak: state.streak.longest,
        streak_broken: isStreakBroken(),
        days_since_last_play: daysSinceLastPlay(),
      });
    }

    // Render
    render();
  }

  // ==================== CANVAS SIZING ====================
  function sizeCanvas() {
    const area = document.getElementById('game-area');
    const availW = area.clientWidth - 24;
    const availH = area.clientHeight - 24;

    dpr = window.devicePixelRatio || 1;

    // Calculate sizes
    const totalCells = GRID_SIZE;
    const clueRatio = CLUE_AREA_RATIO;

    // Each dimension: clue area + grid
    // clue area = clueRatio * gridSide
    // gridSide = totalCells * cellSize + borders
    // totalSide = clueArea + gridSide

    // Fit to available space
    const maxSide = Math.min(availW, availH);
    const totalSide = maxSide;

    clueWidth = Math.floor(totalSide * clueRatio);
    clueHeight = clueWidth;
    const gridSide = totalSide - clueWidth;

    cellSize = Math.floor(gridSide / totalCells);
    const actualGridSide = cellSize * totalCells;

    const canvasW = clueWidth + actualGridSide;
    const canvasH = clueHeight + actualGridSide;

    canvas.style.width = canvasW + 'px';
    canvas.style.height = canvasH + 'px';
    canvas.width = canvasW * dpr;
    canvas.height = canvasH * dpr;
    ctx.scale(dpr, dpr);

    gridOriginX = clueWidth;
    gridOriginY = clueHeight;
  }

  // ==================== RENDERING ====================
  function render() {
    const w = canvas.width / dpr;
    const h = canvas.height / dpr;
    ctx.clearRect(0, 0, w, h);

    drawClues();
    drawGrid();
  }

  function drawClues() {
    const p = state.puzzle;
    const rows = p.grid_size[0];
    const cols = p.grid_size[1];

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    const clueFontSize = Math.max(9, Math.min(14, cellSize * 0.38));
    ctx.font = `500 ${clueFontSize}px Inter, sans-serif`;

    // Row clues (left side)
    ctx.fillStyle = '#F9FAFB';
    ctx.fillRect(0, gridOriginY, clueWidth, cellSize * rows);

    ctx.fillStyle = '#374151';
    for (let r = 0; r < rows; r++) {
      const clue = p.row_clues[r];
      const y = gridOriginY + r * cellSize + cellSize / 2;

      // Check if row is complete
      if (isRowComplete(r)) {
        ctx.fillStyle = '#D1D5DB';
      } else {
        ctx.fillStyle = '#374151';
      }

      const clueStr = clue.join(' ');
      const x = clueWidth - 8;
      ctx.textAlign = 'right';
      ctx.fillText(clueStr, x, y);
    }

    // Column clues (top)
    ctx.fillStyle = '#F9FAFB';
    ctx.fillRect(gridOriginX, 0, cellSize * cols, clueHeight);

    for (let c = 0; c < cols; c++) {
      const clue = p.col_clues[c];
      const x = gridOriginX + c * cellSize + cellSize / 2;

      if (isColComplete(c)) {
        ctx.fillStyle = '#D1D5DB';
      } else {
        ctx.fillStyle = '#374151';
      }

      ctx.textAlign = 'center';
      // Stack clue numbers vertically
      const lineH = clueFontSize + 2;
      const totalH = clue.length * lineH;
      const startY = clueHeight - totalH - 4;
      for (let i = 0; i < clue.length; i++) {
        ctx.fillText(String(clue[i]), x, startY + i * lineH + lineH / 2);
      }
    }

    // Corner
    ctx.fillStyle = '#F3F4F6';
    ctx.fillRect(0, 0, clueWidth, clueHeight);
  }

  function drawGrid() {
    const p = state.puzzle;
    const rows = p.grid_size[0];
    const cols = p.grid_size[1];

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const x = gridOriginX + c * cellSize;
        const y = gridOriginY + r * cellSize;
        const cellState = state.grid[r][c];

        // Cell background
        if (cellState === 'filled') {
          ctx.fillStyle = state.completed ? p.image_colors.filled : '#1A1A1A';
        } else if (cellState === 'marked_x') {
          ctx.fillStyle = '#F3F4F6';
        } else {
          // Hover highlight
          if (state.hoverCell && state.hoverCell.r === r && state.hoverCell.c === c && !state.completed) {
            ctx.fillStyle = '#F0F4FF';
          } else {
            ctx.fillStyle = '#FFFFFF';
          }
        }
        ctx.fillRect(x, y, cellSize, cellSize);

        // X mark
        if (cellState === 'marked_x') {
          ctx.strokeStyle = '#9CA3AF';
          ctx.lineWidth = 1.5;
          const pad = cellSize * 0.25;
          ctx.beginPath();
          ctx.moveTo(x + pad, y + pad);
          ctx.lineTo(x + cellSize - pad, y + cellSize - pad);
          ctx.moveTo(x + cellSize - pad, y + pad);
          ctx.lineTo(x + pad, y + cellSize - pad);
          ctx.stroke();
        }
      }
    }

    // Grid lines
    ctx.strokeStyle = '#D1D5DB';
    ctx.lineWidth = CELL_BORDER;

    for (let r = 0; r <= rows; r++) {
      const y = gridOriginY + r * cellSize;
      const thick = r % THICK_EVERY === 0;
      ctx.strokeStyle = thick ? '#9CA3AF' : '#D1D5DB';
      ctx.lineWidth = thick ? THICK_BORDER : CELL_BORDER;
      ctx.beginPath();
      ctx.moveTo(gridOriginX, y);
      ctx.lineTo(gridOriginX + cols * cellSize, y);
      ctx.stroke();
    }

    for (let c = 0; c <= cols; c++) {
      const x = gridOriginX + c * cellSize;
      const thick = c % THICK_EVERY === 0;
      ctx.strokeStyle = thick ? '#9CA3AF' : '#D1D5DB';
      ctx.lineWidth = thick ? THICK_BORDER : CELL_BORDER;
      ctx.beginPath();
      ctx.moveTo(x, gridOriginY);
      ctx.lineTo(x, gridOriginY + rows * cellSize);
      ctx.stroke();
    }

    // Outer border
    ctx.strokeStyle = '#6B7280';
    ctx.lineWidth = 2;
    ctx.strokeRect(gridOriginX, gridOriginY, cols * cellSize, rows * cellSize);
  }

  // ==================== CLUE COMPLETION CHECK ====================
  function isRowComplete(r) {
    const p = state.puzzle;
    const cols = p.grid_size[1];
    // Check if player's filled cells match the solution for this row
    for (let c = 0; c < cols; c++) {
      if (p.solution[r][c] === 1 && state.grid[r][c] !== 'filled') return false;
    }
    // Also check no incorrect fills
    for (let c = 0; c < cols; c++) {
      if (p.solution[r][c] === 0 && state.grid[r][c] === 'filled') return false;
    }
    return true;
  }

  function isColComplete(c) {
    const p = state.puzzle;
    const rows = p.grid_size[0];
    for (let r = 0; r < rows; r++) {
      if (p.solution[r][c] === 1 && state.grid[r][c] !== 'filled') return false;
    }
    for (let r = 0; r < rows; r++) {
      if (p.solution[r][c] === 0 && state.grid[r][c] === 'filled') return false;
    }
    return true;
  }

  // ==================== INPUT HANDLING ====================
  function getCellFromEvent(e) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = (canvas.width / dpr) / rect.width;
    const scaleY = (canvas.height / dpr) / rect.height;

    let clientX, clientY;
    if (e.touches) {
      clientX = e.touches[0].clientX;
      clientY = e.touches[0].clientY;
    } else {
      clientX = e.clientX;
      clientY = e.clientY;
    }

    const x = (clientX - rect.left) * scaleX;
    const y = (clientY - rect.top) * scaleY;

    const col = Math.floor((x - gridOriginX) / cellSize);
    const row = Math.floor((y - gridOriginY) / cellSize);

    if (row >= 0 && row < GRID_SIZE && col >= 0 && col < GRID_SIZE) {
      return { r: row, c: col, x, y };
    }
    return null;
  }

  function handleCellAction(r, c, isDrag) {
    if (state.completed) return;

    const p = state.puzzle;
    const prevState = state.grid[r][c];
    let newState;

    const tool = state.isDragging ? state.dragTool : state.tool;

    if (tool === 'fill') {
      if (prevState === 'filled') return; // Already filled
      newState = 'filled';
    } else if (tool === 'mark_x') {
      if (prevState === 'marked_x') return;
      newState = 'marked_x';
    } else if (tool === 'erase') {
      if (prevState === 'empty') return;
      newState = 'empty';
    }

    if (newState === prevState) return;

    state.grid[r][c] = newState;
    state.actionCount++;

    const now = performance.now();
    const timeSincePuzzleStart = Math.round(now - state.startTime);
    const timeSinceLastAction = state.lastActionTime ? Math.round(now - state.lastActionTime) : 0;
    state.lastActionTime = now;

    // Determine correctness
    let isCorrect = null;
    if (newState === 'filled') {
      isCorrect = p.solution[r][c] === 1;
    } else if (newState === 'marked_x') {
      isCorrect = p.solution[r][c] === 0;
    }

    // Calculate progress
    const rowFilled = p.solution[r].reduce((s, v) => s + v, 0);
    const rowCorrect = p.solution[r].reduce((s, v, i) => s + (v === 1 && state.grid[r][i] === 'filled' ? 1 : 0), 0);
    const colFilled = p.solution.reduce((s, row) => s + row[c], 0);
    const colCorrect = p.solution.reduce((s, row, i) => s + (row[c] === 1 && state.grid[i][c] === 'filled' ? 1 : 0), 0);

    // Hover duration
    const hoverDuration = (state.hoverCell && state.hoverCell.r === r && state.hoverCell.c === c)
      ? Math.round(now - state.hoverStartTime)
      : 0;

    // Telemetry: CELL_ACTION
    if (typeof Telemetry !== 'undefined') {
      Telemetry.emit('CELL_ACTION', {
        action: tool,
        row: r,
        col: c,
        previous_state: prevState,
        new_state: newState,
        is_correct: isCorrect,
        time_since_puzzle_start_ms: timeSincePuzzleStart,
        time_since_last_action_ms: timeSinceLastAction,
        hover_duration_before_action_ms: hoverDuration,
        cells_filled_so_far: countCells('filled'),
        cells_marked_so_far: countCells('marked_x'),
        errors_so_far: state.errorCount,
        row_progress: rowFilled > 0 ? rowCorrect / rowFilled : 0,
        col_progress: colFilled > 0 ? colCorrect / colFilled : 0,
        is_drag_action: isDrag,
      });
    }

    // Handle errors
    if (isCorrect === false) {
      state.errorCount++;
      const errorNum = state.nextErrorNumber++;
      const cellKey = `${r},${c}`;
      state.errorCells.set(cellKey, errorNum);
      state.errorTimestamps.set(errorNum, now);

      // Flash error
      flashError(r, c);

      // Revert the incorrect action
      state.grid[r][c] = prevState;

      // Telemetry: ERROR_MADE
      if (typeof Telemetry !== 'undefined') {
        const totalFilled = p.solution.flat().reduce((a, b) => a + b, 0);
        const currentFilled = countCells('filled');
        Telemetry.emit('ERROR_MADE', {
          row: r,
          col: c,
          error_number: errorNum,
          time_since_puzzle_start_ms: timeSincePuzzleStart,
          time_since_last_error_ms: state.errorCount > 1
            ? Math.round(now - (state.errorTimestamps.get(errorNum - 1) || now))
            : null,
          action_that_caused_error: tool,
          puzzle_completion_pct: totalFilled > 0 ? currentFilled / totalFilled : 0,
          was_in_completed_row: isRowComplete(r),
          was_in_completed_col: isColComplete(c),
        });
      }
    } else if (tool === 'erase') {
      state.eraseCount++;
    }

    // Save progress
    saveProgress();

    // Check completion
    if (checkCompletion()) {
      handleCompletion();
    }

    render();
  }

  function flashError(r, c) {
    const x = gridOriginX + c * cellSize;
    const y = gridOriginY + r * cellSize;

    // Draw error flash
    ctx.fillStyle = '#FCA5A5';
    ctx.fillRect(x + 1, y + 1, cellSize - 2, cellSize - 2);

    setTimeout(() => render(), ERROR_FLASH_MS);
  }

  function countCells(type) {
    let count = 0;
    for (let r = 0; r < GRID_SIZE; r++) {
      for (let c = 0; c < GRID_SIZE; c++) {
        if (state.grid[r][c] === type) count++;
      }
    }
    return count;
  }

  // ==================== COMPLETION ====================
  function checkCompletion() {
    const p = state.puzzle;
    for (let r = 0; r < GRID_SIZE; r++) {
      for (let c = 0; c < GRID_SIZE; c++) {
        if (p.solution[r][c] === 1 && state.grid[r][c] !== 'filled') return false;
        if (p.solution[r][c] === 0 && state.grid[r][c] === 'filled') return false;
      }
    }
    return true;
  }

  function handleCompletion() {
    state.completed = true;
    const solveTime = Math.round(performance.now() - state.startTime);

    // Update streak
    updateStreak();

    // Update stats
    state.stats.played++;
    state.stats.totalTime += solveTime;
    saveStats();

    // Clear saved progress
    localStorage.removeItem('pictura_progress');

    // Show completion overlay
    const overlay = document.getElementById('completion-overlay');
    document.getElementById('completion-title').textContent = state.puzzle.title || 'Puzzle Complete!';
    document.getElementById('stat-time').textContent = formatTime(solveTime);
    document.getElementById('stat-actions').textContent = state.actionCount;
    document.getElementById('stat-errors').textContent = state.errorCount;

    // Draw reveal
    drawReveal();

    overlay.classList.remove('hidden');

    // Telemetry: PUZZLE_COMPLETE
    if (typeof Telemetry !== 'undefined') {
      const firstActionDelay = state.lastActionTime ? Math.round(state.lastActionTime - state.startTime) : 0;
      Telemetry.emit('PUZZLE_COMPLETE', {
        solve_time_ms: solveTime,
        total_actions: state.actionCount,
        total_errors: state.errorCount,
        total_hints: state.hintCount,
        total_erases: state.eraseCount,
        actions_per_minute: state.actionCount / (solveTime / 60000),
        error_rate: state.actionCount > 0 ? state.errorCount / state.actionCount : 0,
        first_action_delay_ms: firstActionDelay,
        image_name: state.puzzle.title,
        shared_result: false,
      });
    }

    // Re-render with colors
    render();
  }

  function drawReveal() {
    const revealCanvas = document.getElementById('reveal-canvas');
    const rCtx = revealCanvas.getContext('2d');
    const p = state.puzzle;
    const size = 160;
    const cellSz = size / GRID_SIZE;

    revealCanvas.width = size * 2;
    revealCanvas.height = size * 2;
    rCtx.scale(2, 2);

    rCtx.fillStyle = p.image_colors.background || '#FFFFFF';
    rCtx.fillRect(0, 0, size, size);

    rCtx.fillStyle = p.image_colors.filled || '#000000';
    for (let r = 0; r < GRID_SIZE; r++) {
      for (let c = 0; c < GRID_SIZE; c++) {
        if (p.solution[r][c] === 1) {
          rCtx.fillRect(c * cellSz, r * cellSz, cellSz, cellSz);
        }
      }
    }
  }

  // ==================== SHARING ====================
  function generateShareText() {
    const p = state.puzzle;
    const solveTime = Math.round(performance.now() - state.startTime);
    const today = new Date().toISOString().slice(0, 10);

    let text = `Pictura ${today}\n`;
    text += `${formatTime(solveTime)} | ${state.errorCount} errors\n`;
    text += `🔥 ${state.streak.current} day streak\n\n`;

    // Grid as emoji
    for (let r = 0; r < GRID_SIZE; r++) {
      for (let c = 0; c < GRID_SIZE; c++) {
        text += p.solution[r][c] === 1 ? '⬛' : '⬜';
      }
      text += '\n';
    }

    return text;
  }

  // ==================== STREAK ====================
  function loadStreak() {
    const data = localStorage.getItem('pictura_streak');
    if (data) {
      try {
        Object.assign(state.streak, JSON.parse(data));
      } catch (e) { /* ignore */ }
    }
  }

  function saveStreak() {
    localStorage.setItem('pictura_streak', JSON.stringify(state.streak));
  }

  function updateStreak() {
    const today = new Date().toISOString().slice(0, 10);

    if (state.streak.lastPlayDate === today) return; // Already played today

    const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);

    if (state.streak.lastPlayDate === yesterday) {
      state.streak.current++;
    } else {
      state.streak.current = 1;
    }

    state.streak.longest = Math.max(state.streak.longest, state.streak.current);
    state.streak.lastPlayDate = today;
    saveStreak();
    updateStreakDisplay();
  }

  function isStreakBroken() {
    if (!state.streak.lastPlayDate) return false;
    const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
    const today = new Date().toISOString().slice(0, 10);
    return state.streak.lastPlayDate !== yesterday && state.streak.lastPlayDate !== today;
  }

  function daysSinceLastPlay() {
    if (!state.streak.lastPlayDate) return -1;
    const last = new Date(state.streak.lastPlayDate);
    const now = new Date();
    return Math.floor((now - last) / 86400000);
  }

  function updateStreakDisplay() {
    document.getElementById('streak-count').textContent = state.streak.current;
  }

  // ==================== PROGRESS PERSISTENCE ====================
  function saveProgress() {
    const data = {
      puzzleId: state.puzzle.id,
      grid: state.grid,
      actionCount: state.actionCount,
      errorCount: state.errorCount,
      elapsedMs: Math.round(performance.now() - state.startTime),
    };
    localStorage.setItem('pictura_progress', JSON.stringify(data));
  }

  function loadProgress() {
    const data = localStorage.getItem('pictura_progress');
    if (data) {
      try {
        return JSON.parse(data);
      } catch (e) { /* ignore */ }
    }
    return null;
  }

  // ==================== STATS ====================
  function loadStats() {
    const data = localStorage.getItem('pictura_stats');
    if (data) {
      try {
        Object.assign(state.stats, JSON.parse(data));
      } catch (e) { /* ignore */ }
    }
  }

  function saveStats() {
    localStorage.setItem('pictura_stats', JSON.stringify(state.stats));
  }

  function showStats() {
    document.getElementById('stats-played').textContent = state.stats.played;
    document.getElementById('stats-streak').textContent = state.streak.current;
    document.getElementById('stats-max-streak').textContent = state.streak.longest;
    document.getElementById('stats-avg-time').textContent =
      state.stats.played > 0
        ? formatTime(state.stats.totalTime / state.stats.played)
        : '0:00';
    document.getElementById('stats-overlay').classList.remove('hidden');
  }

  // ==================== HELPERS ====================
  function formatTime(ms) {
    const totalSecs = Math.floor(ms / 1000);
    const mins = Math.floor(totalSecs / 60);
    const secs = totalSecs % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }

  function formatDate(isoDate) {
    const d = new Date(isoDate + 'T00:00:00');
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }

  // ==================== EVENT LISTENERS ====================

  // Pointer events for cross-device support
  canvas.addEventListener('pointerdown', (e) => {
    if (state.completed) return;
    e.preventDefault();
    canvas.setPointerCapture(e.pointerId);

    const cell = getCellFromEvent(e);
    if (cell) {
      state.isDragging = true;
      state.dragTool = state.tool;
      handleCellAction(cell.r, cell.c, false);
    }
  });

  canvas.addEventListener('pointermove', (e) => {
    const cell = getCellFromEvent(e);

    // Update hover state
    if (cell) {
      if (!state.hoverCell || state.hoverCell.r !== cell.r || state.hoverCell.c !== cell.c) {
        state.hoverCell = cell;
        state.hoverStartTime = performance.now();
        if (!state.isDragging) render();
      }
    } else {
      if (state.hoverCell) {
        state.hoverCell = null;
        if (!state.isDragging) render();
      }
    }

    // Drag filling
    if (state.isDragging && cell) {
      handleCellAction(cell.r, cell.c, true);
    }
  });

  canvas.addEventListener('pointerup', () => {
    state.isDragging = false;
    state.dragTool = null;
  });

  canvas.addEventListener('pointerleave', () => {
    state.hoverCell = null;
    render();
  });

  // Prevent context menu on long press
  canvas.addEventListener('contextmenu', (e) => e.preventDefault());

  // Tool buttons
  document.querySelectorAll('.tool-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.tool = btn.dataset.tool;
    });
  });

  // Overlay buttons
  document.getElementById('btn-help').addEventListener('click', () => {
    document.getElementById('help-overlay').classList.remove('hidden');
  });
  document.getElementById('btn-close-help').addEventListener('click', () => {
    document.getElementById('help-overlay').classList.add('hidden');
  });
  document.getElementById('btn-stats').addEventListener('click', showStats);
  document.getElementById('btn-close-stats').addEventListener('click', () => {
    document.getElementById('stats-overlay').classList.add('hidden');
  });
  document.getElementById('btn-close-overlay').addEventListener('click', () => {
    document.getElementById('completion-overlay').classList.add('hidden');
  });
  document.getElementById('btn-share').addEventListener('click', () => {
    const text = generateShareText();
    if (navigator.share) {
      navigator.share({ text }).catch(() => {});
    } else if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(() => {
        const btn = document.getElementById('btn-share');
        btn.textContent = 'Copied!';
        setTimeout(() => { btn.textContent = 'Share'; }, 2000);
      });
    }
  });

  // Close overlays on backdrop click
  document.querySelectorAll('.overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        overlay.classList.add('hidden');
      }
    });
  });

  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    if (e.key === '1' || e.key === 'f') {
      document.getElementById('tool-fill').click();
    } else if (e.key === '2' || e.key === 'x') {
      document.getElementById('tool-mark').click();
    } else if (e.key === '3' || e.key === 'e') {
      document.getElementById('tool-erase').click();
    }
  });

  // Resize handling
  window.addEventListener('resize', () => {
    sizeCanvas();
    render();
  });

  // Abandonment tracking
  window.addEventListener('beforeunload', () => {
    if (!state.completed && state.actionCount > 0 && typeof Telemetry !== 'undefined') {
      const totalFilled = state.puzzle.solution.flat().reduce((a, b) => a + b, 0);
      const currentFilled = countCells('filled');
      Telemetry.emit('PUZZLE_ABANDON', {
        time_spent_ms: Math.round(performance.now() - state.startTime),
        puzzle_completion_pct: totalFilled > 0 ? currentFilled / totalFilled : 0,
        total_actions: state.actionCount,
        total_errors: state.errorCount,
        last_action_type: state.tool,
        time_since_last_action_ms: state.lastActionTime
          ? Math.round(performance.now() - state.lastActionTime)
          : 0,
        abandon_method: 'tab_close',
      });
      Telemetry.flush();
    }
  });

  // Pointer sampling for telemetry
  let pointerSampleInterval = null;
  let lastPointerEvent = null;
  let lastPointerPos = null;

  canvas.addEventListener('pointermove', (e) => {
    lastPointerEvent = e;
  });

  function startPointerSampling() {
    pointerSampleInterval = setInterval(() => {
      if (!lastPointerEvent || state.completed) return;
      if (typeof Telemetry === 'undefined') return;

      const e = lastPointerEvent;
      const cell = getCellFromEvent(e);

      const rect = canvas.getBoundingClientRect();
      const clientX = e.clientX;
      const clientY = e.clientY;

      // Calculate velocity
      let velocity = 0;
      if (lastPointerPos) {
        const dx = clientX - lastPointerPos.x;
        const dy = clientY - lastPointerPos.y;
        const dt = 1000 / POINTER_SAMPLE_HZ; // ms between samples
        velocity = Math.sqrt(dx * dx + dy * dy) / (dt / 1000); // px/s
      }
      lastPointerPos = { x: clientX, y: clientY };

      // Check if over clue area
      const scaleX = (canvas.width / dpr) / rect.width;
      const x = (clientX - rect.left) * scaleX;
      const y = (clientY - rect.top) * scaleX;
      const isOverClue = x < gridOriginX || y < gridOriginY;
      let clueRowOrCol = null;
      if (isOverClue) {
        if (x < gridOriginX && y >= gridOriginY) {
          clueRowOrCol = Math.floor((y - gridOriginY) / cellSize);
        } else if (y < gridOriginY && x >= gridOriginX) {
          clueRowOrCol = Math.floor((x - gridOriginX) / cellSize);
        }
      }

      Telemetry.emit('POINTER_SAMPLE', {
        client_x: Math.round(clientX),
        client_y: Math.round(clientY),
        grid_row: cell ? cell.r : null,
        grid_col: cell ? cell.c : null,
        velocity_px_per_s: Math.round(velocity),
        is_over_clue_area: isOverClue,
        clue_row_or_col: clueRowOrCol,
      });
    }, 1000 / POINTER_SAMPLE_HZ);
  }

  // ==================== INIT ====================
  // Generate user ID if not exists
  if (!localStorage.getItem('pictura_user_id')) {
    localStorage.setItem('pictura_user_id', crypto.randomUUID());
  }

  startPointerSampling();
  loadPuzzle();

})();
