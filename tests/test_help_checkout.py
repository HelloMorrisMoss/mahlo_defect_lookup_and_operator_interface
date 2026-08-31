import json
import os


def test_version_checkout_and_parent_tracking(auth_client, app):
    """Test version checkout and parent tracking."""
    # Ensure content directory exists for CASManager
    content_dir = os.path.join(app.root_path, 'help_system', 'help_content')
    os.makedirs(content_dir, exist_ok=True)

    # 1. Create a dummy article to ensure we have something to snapshot
    article_path = os.path.join(content_dir, 'checkout_test.json')
    with open(article_path, 'w', encoding='utf-8') as f:
        json.dump([{"type": "title", "content": "Checkout Test"}], f)

    try:
        # 2. Create a version (v1)
        response = auth_client.post('/help/api/versions/create',
                                    json={"comment": "Initial version"})
        assert response.status_code == 200
        v1 = response.json
        v1_id = v1['id']

        # 3. Checkout v1
        response = auth_client.post('/help/api/versions/checkout',
                                    json={"id": v1_id})
        assert response.status_code == 200
        assert response.json['success'] is True

        # 4. Create another version (v2) with v1 as parent
        response = auth_client.post('/help/api/versions/create',
                                    json={"comment": "Second version", "parent_id": v1_id})
        assert response.status_code == 200
        v2 = response.json
        assert v2['parent_id'] == v1_id

        # 5. Verify in history
        response = auth_client.get('/help/api/versions/history')
        assert response.status_code == 200
        history = response.json
        assert any(v['id'] == v2['id'] and v['parent_id'] == v1_id for v in history)

    finally:
        if os.path.exists(article_path):
            os.remove(article_path)
        # We don't remove blobs as they might be used by other tests if we are unlucky, 
        # but here it's in-memory DB so it should be fine.
