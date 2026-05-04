# N8n Integration Guide for Batch Processing
To close the loop so the dashboard progress bar moves, your n8n workflow must update the Supabase `batch_items` table when it finishes processing a URL.

Below is an abstract example of the HTTP Node you should place at the END of your n8n workflow to mark the item as 'completed'.

### Supabase Callback Node

1. Add an **HTTP Request** node in n8n.
2. Set Method to **PATCH**
3. Set URL to: `https://cbysbvanpohcdgbrembr.supabase.co/rest/v1/batch_items?batch_id=eq.{{$json["batchJobId"]}}&url=eq.{{$json["source_url"]}}`
4. Send Headers:
   - `Content-Type`: `application/json`
   - `apikey`: `<YOUR_SUPABASE_SERVICE_ROLE_KEY>`
   - `Authorization`: `Bearer <YOUR_SUPABASE_SERVICE_ROLE_KEY>`
5. Send Body (JSON):
   ```json
   {
      "status": "completed",
      "result_url": "{{$json["uploaded_html_url_from_s3"]}}",
      "score": 90
   }
   ```

By executing this Node, real-time polling in the Dashboard UI will instantly recognize the completion of the row and augment the UI's progress bar.
