## Review: qwen-random.py by Anthropic/Claude Code

The following is the verbatim output of the Gemini/Antigravity review of qwen-random.py.

### Findings

1. **Fatal syntax error — script cannot run at all** (line 229)
   `StdRandom.uniformLong(100000000000L)` uses the `L` integer suffix, which is Python 2 syntax and is invalid in Python 3. Confirmed via `ast.parse`:
   ```
   SyntaxError: invalid decimal literal
   ```
   Fix: drop the suffix — `100000000000`.

2. **Duplicate `@classmethod` definitions silently shadow each other** (Python has no method overloading; the last definition with a given name wins, unlike Java/C++ where this file's style originates)
   - `gaussian` is defined twice: `gaussian(cls, mu, sigma)` (line 40) and `gaussian(cls)` (line 44). Only the no-arg version survives on the class. The call `StdRandom.gaussian(9.0, 0.2)` (line 226) will raise `TypeError: gaussian() takes 1 positional argument but 3 were given`.
   - `discrete` is defined twice: probability-array version (line 73) and frequency-array version (line 93). Only the frequency version survives. The call `StdRandom.discrete(probabilities)` (line 227) with `probabilities = [0.5, 0.3, 0.1, 0.1]` will run the frequency logic against floats and fail in `random.randint(0, sum_freq - 1)` (non-integer bound).
   - `shuffle` is defined twice: `shuffle(cls, a)` (line 119) and `shuffle(cls, a, lo, hi)` (line 123). Only the 3-positional-arg version survives. The call `StdRandom.shuffle(a)` (line 230) will raise `TypeError: shuffle() missing 2 required positional arguments: 'lo' and 'hi'`.
   - Same shadowing pattern applies to `StdOut.println`, `StdOut.print`, and `StdOut.printf` (each defined ~8/2 times). These happen to still "work" because every surviving override just does `print(x)`, but all the earlier overload definitions are dead code and misleading.

3. **`uniformDouble` called with arguments it doesn't accept** (line 224)
   `uniformDouble` is defined only as `uniformDouble(cls)` → `random.random()` (no range parameters), but called as `StdRandom.uniformDouble(10.0, 99.0)`. This will raise `TypeError` once the above issues are fixed, since the method has no `lo`/`hi` parameters and never scales the range.

4. **`shuffle(cls, a, lo, hi)` does not shuffle in place** (line 123-124)
   `random.shuffle(a[lo:hi])` shuffles a *copy* (the slice) and discards the result — the original list `a` is left unmodified. Even if this overload weren't shadowed, it would be a no-op bug. Should mutate the original slice, e.g.:
   ```python
   a[lo:hi] = random.sample(a[lo:hi], hi - lo)
   ```

## Summary
The script cannot execute as-is due to the Python 2 `L` literal (fatal). Even after fixing that, several call sites in `__main__` (lines 224, 226, 227, 230) will raise `TypeError` because Python's lack of method overloading causes the "later" duplicate `@classmethod` definitions to silently replace earlier ones with different signatures — a direct artifact of a Java-style API (this mirrors Princeton's `StdRandom`/`StdOut`) being ported to Python without adapting for method overloading.
