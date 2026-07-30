---
hide:
  - navigation
  - toc
---

{% set wall = gallery_data() %}

<div
  id="gallery-wall"
  data-shuffle="{{ 'true' if wall.page.get('shuffle', false) else 'false' }}"
>
  <nav class="gallery-filters" aria-label="Filter gallery by tag">
    <button type="button" class="gallery-filter is-active" data-filter="all">All</button>
    {% for tag in gallery_wall_tags() %}
    <span class="gallery-filter-sep" aria-hidden="true">·</span>
    <button type="button" class="gallery-filter" data-filter="{{ tag | e }}">{{ tag | e }}</button>
    {% endfor %}
  </nav>
  <nav class="gallery-filters gallery-filters-media" aria-label="Filter by media type">
    <button type="button" class="gallery-filter" data-filter="images">images</button>
    <span class="gallery-filter-sep" aria-hidden="true">·</span>
    <button type="button" class="gallery-filter" data-filter="videos">videos</button>
  </nav>

  <div class="gallery-masonry">
    {% for item in wall_gallery_entries() %}
    {% set is_video = item.get('video') %}
    {% set media_src = item.video if is_video else item.image %}
    {% set media_url = media_src if gallery_media_is_remote(media_src) else media_src | relative_url %}
    {% set poster_raw = item.get('poster', '') %}
    {% set poster_url = poster_raw if (not poster_raw or gallery_media_is_remote(poster_raw)) else poster_raw | relative_url %}
    {% set media_tag = 'videos' if is_video else 'images' %}
    {% set item_tags = [media_tag] + (item.get('tags') or []) %}
    <article
      class="gallery-card{% if is_video %} is-video{% endif %}"
      data-tags="{{ item_tags | join('|') | e }}"
      data-media="{{ 'video' if is_video else 'image' }}"
      style="
        {% set card_bg = item.get('card_color') or wall.page.get('card_color') %}
        {% set card_fg = item.get('text_color') or wall.page.get('card_text_color') or wall.page.get('text_color') %}
        {% if card_bg %}background: {{ card_bg | e }}; {% endif %}
        {% if card_fg %}color: {{ card_fg | e }};{% endif %}
      "
    >
      <button
        type="button"
        class="gallery-open"
        data-type="{{ 'video' if is_video else 'image' }}"
        data-src="{{ media_url | e }}"
        data-poster="{{ poster_url | e }}"
        data-comment="{{ item.get('comment', '') | e }}"
        data-date="{{ item.get('date', '') | e }}"
        aria-label="Open {% if is_video %}video{% else %}image{% endif %}{% if item.get('comment') %}: {{ item.comment | e }}{% endif %}"
      >
        <span class="gallery-media">
          {% if is_video %}
          <video
            class="gallery-image gallery-video"
            src="{{ media_url | e }}"
            {% if poster_url %}poster="{{ poster_url | e }}"{% endif %}
            muted
            playsinline
            preload="metadata"
            {% if item.get('width') %}width="{{ item.width | int }}"{% endif %}
            {% if item.get('height') %}height="{{ item.height | int }}"{% endif %}
            {% if item.get('width') and item.get('height') %}
            style="aspect-ratio: {{ item.width | int }} / {{ item.height | int }};"
            {% elif item.get('aspect_ratio') %}
            style="aspect-ratio: {{ item.aspect_ratio | e }};"
            {% endif %}
          ></video>
          <span class="gallery-play" aria-hidden="true">▶</span>
          {% else %}
          <img
            class="gallery-image"
            src="{{ media_url | e }}"
            alt="{{ item.get('comment', '') | e }}"
            loading="lazy"
            decoding="async"
            {% if item.get('width') %}width="{{ item.width | int }}"{% endif %}
            {% if item.get('height') %}height="{{ item.height | int }}"{% endif %}
            {% if item.get('width') and item.get('height') %}
            style="aspect-ratio: {{ item.width | int }} / {{ item.height | int }};"
            {% elif item.get('aspect_ratio') %}
            style="aspect-ratio: {{ item.aspect_ratio | e }};"
            {% endif %}
          />
          {% endif %}
        </span>
      </button>
      {% if item.get('comment') or item.get('date') %}
      <div class="gallery-meta">
        {% if item.get('comment') %}
        <p class="gallery-comment">{{ item.comment | e }}</p>
        {% endif %}
        {% if item.get('date') %}
        <div class="gallery-date">{{ item.date | e }}</div>
        {% endif %}
      </div>
      {% endif %}
    </article>
    {% endfor %}
  </div>
</div>

<div
  id="gallery-lightbox"
  class="gallery-lightbox"
  hidden
  role="dialog"
  aria-modal="true"
  aria-label="Media viewer"
>
  <button type="button" class="lightbox-backdrop" aria-label="Close"></button>
  <button type="button" class="lightbox-prev" aria-label="Previous">‹</button>
  <button type="button" class="lightbox-next" aria-label="Next">›</button>
  <div class="lightbox-dialog">
    <button type="button" class="lightbox-close" aria-label="Close">×</button>
    <img class="lightbox-image" src="" alt="" hidden />
    <video class="lightbox-video" controls playsinline hidden></video>
    <p class="lightbox-comment" hidden></p>
    <div class="lightbox-date" hidden></div>
  </div>
</div>
