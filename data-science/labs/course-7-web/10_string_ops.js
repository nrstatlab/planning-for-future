/* Experiment 10 — JavaScript string operations.
 *
 * Reverse, substring, count vowels — plus the statistics a viva usually asks
 * for on top. Every function is pure: input in, value out, no DOM. That is
 * what lets tools/run_web_labs.js assert them without a browser.
 */

/** Reverse a string.
 *
 * [...s] splits by CODE POINT; s.split("") splits by UTF-16 code unit. For
 * plain ASCII they agree, but split("") tears an emoji or a surrogate pair in
 * half and the reversal produces garbage.
 */
export function reverse(s) {
  return [...s].reverse().join("");
}

export function countVowels(s) {
  return [...s.toLowerCase()].filter(c => "aeiou".includes(c)).length;
}

export function countConsonants(s) {
  return (s.match(/[b-df-hj-np-tv-z]/gi) || []).length;
}

/** Word count. s.trim().split(/\s+/) on an empty string gives [""], whose
 *  length is 1 — so a blank input would otherwise report one word. */
export function countWords(s) {
  const t = s.trim();
  return t === "" ? 0 : t.split(/\s+/).length;
}

export function isPalindrome(s) {
  const clean = s.toLowerCase().replace(/[^a-z0-9]/g, "");
  return clean.length > 0 && clean === reverse(clean);
}

export function titleCase(s) {
  return s.toLowerCase().replace(/\b[a-z]/g, c => c.toUpperCase());
}

/** Frequency of each character, ignoring case and whitespace. */
export function charFrequency(s) {
  const freq = {};
  for (const c of s.toLowerCase()) {
    if (/\s/.test(c)) continue;
    freq[c] = (freq[c] || 0) + 1;      // (freq[c] || 0) handles the first hit
  }
  return freq;
}

export function longestWord(s) {
  const words = s.trim() === "" ? [] : s.trim().split(/\s+/);
  return words.reduce((best, w) => (w.length > best.length ? w : best), "");
}

/** Everything at once — what the browser page displays. */
export function stats(s) {
  return {
    length:      s.length,
    words:       countWords(s),
    vowels:      countVowels(s),
    consonants:  countConsonants(s),
    digits:      (s.match(/\d/g) || []).length,
    upper:       s.toUpperCase(),
    lower:       s.toLowerCase(),
    title:       titleCase(s),
    reversed:    reverse(s),
    firstFour:   s.slice(0, 4),
    lastSeven:   s.slice(-7),
    isPalindrome: isPalindrome(s),
    longestWord: longestWord(s)
  };
}
