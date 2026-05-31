---
title: Blog List
permalink: /blog-list/
---

Browse the latest project blogs, updates, and announcements.

<ul>
  {% assign sorted_posts = site.posts | sort: 'date' | reverse %}
  {% for post in sorted_posts %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <small> - {{ post.date | date: "%Y-%m-%d" }}</small>
      {% if post.categories and post.categories.size > 0 %}
        <small> | {{ post.categories | join: ", " }}</small>
      {% endif %}
    </li>
  {% endfor %}
</ul>
