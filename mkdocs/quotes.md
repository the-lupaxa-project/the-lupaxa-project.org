---
hide:
  - navigation
  - toc
---

{% set wall = quotes_data() %}

<div
  id="quotes-wall"
  data-shuffle="{{ 'true' if wall.page.get('shuffle', false) else 'false' }}"
>
  <nav class="quotes-filters" aria-label="Filter quotes by tag">
    <button type="button" class="quotes-filter is-active" data-filter="all">All</button>
    {% for tag in wall_tags() %}
    <span class="quotes-filter-sep" aria-hidden="true">·</span>
    <button type="button" class="quotes-filter" data-filter="{{ tag | e }}">{{ tag | e }}</button>
    {% endfor %}
  </nav>

  <div class="quotes-masonry">
    {% for quote in wall_quotes() %}
    <article
      class="quote-card"
      data-tags="{{ quote.get('tags', []) | join('|') | e }}"
      style="background: {{ quote.card_color | e }}; color: {{ quote.text_color | e }};"
    >
      <div class="quote-text">
        {% set lines = quote.text.split('\n') | map('trim') | reject('equalto', '') | list %}
        {% for line in lines %}
        <p class="quote-line">{% if loop.first %}“{% endif %}{{ line | e }}{% if loop.last %}”{% endif %}</p>
        {% endfor %}
      </div>
      <footer class="quote-attribution">
        <div class="quote-author">{{ quote.author | e }}</div>
        {% if quote.get('year') %}
        <div class="quote-year">{{ quote.get('year') | e }}</div>
        {% endif %}
      </footer>
    </article>
    {% endfor %}
  </div>
</div>
