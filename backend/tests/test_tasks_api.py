def test_list_empty(client):
    response = client.get("/api/tasks", params={"reference_date": "2026-06-01"})
    assert response.status_code == 200
    assert response.json() == {"today": [], "future": []}


def test_list_invalid_reference_date(client):
    response = client.get("/api/tasks", params={"reference_date": "not-a-date"})
    assert response.status_code == 422


def test_list_today_and_future(client):
    reference = "2026-06-01"
    client.post(
        "/api/tasks",
        json={"title": "Future B", "task_date": "2026-06-03"},
    )
    client.post(
        "/api/tasks",
        json={"title": "Today A", "task_date": reference},
    )
    client.post(
        "/api/tasks",
        json={"title": "Future A", "task_date": "2026-06-02"},
    )
    client.post(
        "/api/tasks",
        json={"title": "Past", "task_date": "2026-05-30"},
    )

    response = client.get("/api/tasks", params={"reference_date": reference})
    assert response.status_code == 200
    body = response.json()
    assert [task["title"] for task in body["today"]] == ["Today A"]
    assert [task["title"] for task in body["future"]] == ["Future A", "Future B"]


def test_create_rejects_empty_title(client):
    response = client.post(
        "/api/tasks",
        json={"title": "   ", "task_date": "2026-06-01"},
    )
    assert response.status_code == 422


def test_create_task_fields(client):
    response = client.post(
        "/api/tasks",
        json={"title": "Buy milk", "task_date": "2026-06-01"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Buy milk"
    assert body["task_date"] == "2026-06-01"
    assert "id" in body
    assert "created_at" in body
    assert "due_time" not in body
    assert "is_done" not in body


def test_update_task_title_and_date(client):
    create_response = client.post(
        "/api/tasks",
        json={"title": "Original", "task_date": "2026-06-01"},
    )
    task_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/api/tasks/{task_id}",
        json={"title": "Updated", "task_date": "2026-06-05"},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["title"] == "Updated"
    assert patch_response.json()["task_date"] == "2026-06-05"


def test_delete_task(client):
    create_response = client.post(
        "/api/tasks",
        json={"title": "Temporary", "task_date": "2026-06-01"},
    )
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/tasks/{task_id}")
    assert delete_response.status_code == 204

    list_response = client.get(
        "/api/tasks", params={"reference_date": "2026-06-01"}
    )
    assert list_response.json() == {"today": [], "future": []}


def test_delete_missing_task_returns_404(client):
    response = client.delete("/api/tasks/9999")
    assert response.status_code == 404
