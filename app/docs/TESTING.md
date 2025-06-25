# Testing Guide for YouTube AI App v2.5

## 1. Running Tests
- Main app tests (if present):
  ```bash
  pytest app/tests/
  ```
- Mini app tests (if present):
  ```bash
  pytest mini_app/app/tests/
  ```

## 2. Writing New Tests
- Place new tests in `app/tests/` for the main app or `mini_app/app/tests/` for the mini app.
- Use `pytest` conventions for test discovery and assertions.
- Example test file:
  ```python
  def test_example():
      assert 1 + 1 == 2
  ```

## 3. Continuous Integration
- All tests are run automatically via GitHub Actions on push and PR.
- Keep tests up to date with new features and bug fixes.

---

For more details, see the main `README.md` or contact the project owner. 