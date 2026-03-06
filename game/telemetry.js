/**
 * Telemetry — Behavioral data collection for Pictura.
 *
 * Implements the event schema from behavioral-data-schema.md.
 * Events are buffered in memory and batched to localStorage.
 * In production, replace flush() with an API endpoint.
 */

const Telemetry = (function () {
  'use strict';

  const BUFFER_SIZE = 50;
  const FLUSH_INTERVAL_MS = 30000; // 30s
  const STORAGE_KEY = 'pictura_events';

  function safeUUID() {
    if (typeof crypto.randomUUID === 'function' && window.isSecureContext) {
      return crypto.randomUUID();
    }
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = Math.random() * 16 | 0;
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
  }

  let sessionId = safeUUID();
  let userId = localStorage.getItem('pictura_user_id') || safeUUID();
  let eventSeq = 0;
  let buffer = [];
  let puzzleId = null;
  let puzzleDifficulty = null;
  let puzzleSize = null;
  let deviceType = 'mouse'; // Updated on first pointer event

  // Detect device type from first pointer event
  document.addEventListener('pointerdown', function detectDevice(e) {
    deviceType = e.pointerType || 'mouse'; // 'mouse' | 'touch' | 'pen'
    document.removeEventListener('pointerdown', detectDevice);
  }, { once: true });

  function emit(eventType, eventData) {
    // Update puzzle context from PUZZLE_START
    if (eventType === 'PUZZLE_START') {
      puzzleSize = `${eventData.puzzle_grid_rows}x${eventData.puzzle_grid_cols}`;
    }

    const event = {
      session_id: sessionId,
      user_id: userId,
      puzzle_id: puzzleId,
      puzzle_difficulty: puzzleDifficulty,
      puzzle_size: puzzleSize,
      event_type: eventType,
      event_seq: eventSeq++,
      timestamp_ms: Math.round(performance.timeOrigin + performance.now()),
      device_type: deviceType,
      viewport_width: window.innerWidth,
      viewport_height: window.innerHeight,
      event_data: eventData,
    };

    buffer.push(event);

    // Auto-flush when buffer is full
    if (buffer.length >= BUFFER_SIZE) {
      flush();
    }
  }

  function setPuzzleContext(id, difficulty, size) {
    puzzleId = id;
    puzzleDifficulty = difficulty;
    puzzleSize = size;
  }

  function flush() {
    if (buffer.length === 0) return;

    // Append to localStorage
    const existing = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    const combined = existing.concat(buffer);

    // Keep last 5000 events to prevent storage overflow
    const trimmed = combined.length > 5000 ? combined.slice(-5000) : combined;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(trimmed));

    buffer = [];
  }

  function getEvents() {
    flush();
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  }

  function clearEvents() {
    localStorage.removeItem(STORAGE_KEY);
    buffer = [];
  }

  // Periodic flush
  setInterval(flush, FLUSH_INTERVAL_MS);

  // Flush on page hide
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
      flush();
    }
  });

  return {
    emit,
    setPuzzleContext,
    flush,
    getEvents,
    clearEvents,
  };

})();
