/* Strip a leading run of dashes from the site search query.
 *
 * The handbook documents CLI flags verbatim, so visitors search for
 * "--async-scheduling". Lunr's query lexer reads leading "-" / "+" as
 * presence modifiers, which turns such a query into a negation and returns
 * nothing. Material reads the input value when handling the "input" event;
 * this capture-phase listener runs first and rewrites the value so the
 * flag name is searched instead.
 *
 * Only the leading dashes are removed ("--async-scheduling" ->
 * "async-scheduling"); single dashes inside the name still act as
 * separators, and underscore-separated env vars are left untouched.
 */
(() => {
  document.addEventListener("input", event => {
    const el = event.target
    if (
      !(el instanceof HTMLInputElement) ||
      !el.classList.contains("md-search__input")
    )
      return

    const value = el.value
    const stripped = value.replace(/^--+/, "")
    if (stripped !== value)
      el.value = stripped
  }, true)
})()
