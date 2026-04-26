# n8n Variable Mapping

Required fields:

- {{$json.article_title}}
- {{$json.article_subtitle}}
- {{$json.author_name}}
- {{$json.publish_date}}
- {{$json.hero_image_url}}
- {{$json.article_body}}
- {{$json.tags}}
- {{$json.source_url}}
- {{$json.campaign_id}}

Optional fields:

- {{$json.logo_url}}
- {{$json.unsubscribe_url}}
- {{$json.tracking_pixel_url}}
- {{$json.brand_name}}
- {{$json.subject_variant}}

Rules:

- Keep expressions raw; n8n processes them server-side.
- Ensure every link is absolute after n8n renders.
- UTM campaign should use {{$json.campaign_id}}.
