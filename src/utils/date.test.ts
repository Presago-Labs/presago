import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { formatLeaderboardTimestamp } from './date.ts';

describe('Leaderboard Timestamp Utilities', () => {
  it('returns empty string for empty input', () => {
    assert.equal(formatLeaderboardTimestamp(''), '');
  });

  it('returns empty string for undefined', () => {
    assert.equal(
      formatLeaderboardTimestamp(undefined as any),
      ''
    );
  });

  it('formats valid timestamps', () => {
    assert.ok(
      formatLeaderboardTimestamp('2026-08-06T12:00:00Z')
    );
  });

  it('formats numeric epoch timestamp zero', () => {
    const result = formatLeaderboardTimestamp(0);
    assert.notEqual(result, '');
    assert.ok(result);
  });
});