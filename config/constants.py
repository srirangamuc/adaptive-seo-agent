MAX_RETRIES = 3
MIN_RELEVANCE_SCORE = 0.7
MIN_CONSISTENCY_SCORE = 0.8
DEFAULT_PROMPT = "Generate adaptive content."

MAX_SEO_TITLE_CHARS = 60
MAX_SEO_DESC_CHARS = 155
MAX_SOCIAL_TWITTER_CHARS = 280
MAX_SOCIAL_LINKEDIN_CHARS = 600
MAX_NEWSLETTER_CHARS = 2000

BLOG_PROMPT = """You are a content strategist. Write a detailed blog draft about: {topic}.
Audience: {audience}
Constraints: {constraints}
Outline: {outline}
Tone: {tone}
Keywords: {keywords}
Entities: {entities}
Source excerpt (if provided): {source_excerpt}
Return 6-8 paragraphs with clear section headings and at least 700 words.
"""

SEO_PROMPT = """You are an SEO expert. Create:
1) A title (max 60 chars)
2) A meta description (max 155 chars)
Topic: {topic}
"""

SEO_JSON_PROMPT = """Return STRICT JSON with keys:
title (string, <= 60 chars), description (string, <= 155 chars), keywords (array of 4-8 strings).
Topic: {topic}
Use concise wording. Return ONLY valid JSON.
"""

SOCIAL_PROMPT = """You are a social media manager. Create:
- 1 tweet (max 280 chars)
- 1 LinkedIn post (max 600 chars)
Topic: {topic}
Audience: {audience}
"""

SOCIAL_JSON_PROMPT = """Return STRICT JSON with keys:
twitter (string, <= 280 chars), linkedin (string, <= 600 chars).
Topic: {topic}
Audience: {audience}
Return ONLY valid JSON.
"""

SEO_SOCIAL_JSON_PROMPT = """Return STRICT JSON with keys:
seo: {{"title": "", "description": "", "keywords": []}}
social: {{"twitter": "", "linkedin": ""}}
Constraints:
- title <= 60 chars
- description <= 155 chars
- twitter <= 280 chars
- linkedin <= 600 chars
Topic: {topic}
Audience: {audience}
Return ONLY valid JSON. No markdown, no commentary, no extra keys.
"""

NEWSLETTER_PROMPT = """You are a newsletter editor. Write a concise summary for a newsletter.
Topic: {topic}
Audience: {audience}
Use the anchor content below as source material:
{anchor}
Return 1 short paragraph with a clear takeaway.
"""

NEWSLETTER_JSON_PROMPT = """Return STRICT JSON with keys:
headline (string, <= 90 chars), summary (string, <= 1500 chars).
Topic: {topic}
Audience: {audience}
Use the anchor content below as source material:
{anchor}
Return ONLY valid JSON.
"""

PLANNING_PROMPT = """Create a content plan as strict JSON with keys:
outline (array of 4-6 bullets), tone (string), entities (array), keywords (array).
Topic: {topic}
Audience: {audience}
Constraints: {constraints}
Source excerpt (if provided): {source_excerpt}
Return ONLY valid JSON.
"""
