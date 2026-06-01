from datetime import date


def test_list_empty_day(client):
    response = client.get("/api/tasks", params={"date": "2026-06-01"})
    assert response.status_code == 200
    assert response.json() == []


def test_list_invalid_date(client):
    response = client.get("/api/tasks", params={"date": "not-a-date"})
    assert response.status_code == 422


def test_create_and_list_timed_and_untimed(client):
    day = "2026-06-01"
    client.post(
        "/api/tasks",
        json={"title": "Untimed B", "task_date": day, "due_time": None},
    )
    client.post(
        "/api/tasks",
        json={"title": "Timed late", "task_date": day, "due_time": "14:00:00"},
    )
    client.post(
        "/api/tasks",
        json={"title": "Timed early", "task_date": day, "due_time": "09:30:00"},
    )

    response = client.get("/api/tasks", params={"date": day})
    assert response.status_code == 200
    titles = [task["title"] for task in response.json()]
    assert titles == ["Timed early", "Timed late", "Untimed B"]


def test_create_rejects_empty_title(client):
    response = client.post(
        "/api/tasks",
        json={"title": "   ", "task_date": "2026-06-01"},
    )
    assert response.status_code == 422


def test_toggle_done(client):
    create_response = client.post(
        "/api/tasks",
        json={"title": "Buy milk", "task_date": "2026-06-01"},
    )
    task_id = create_response.json()["id"]
    assert create_response.json()["is_done"] is False

    patch_response = client.patch(
        f"/api/tasks/{task_id}",
        json={"is_done": True},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["is_done"] is True


def test_delete_task(client):
    create_response = client.post(
        "/api/tasks",
        json={"title": "Temporary", "task_date": "2026-06-01"},
    )
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/tasks/{task_id}")
    assert delete_response.status_code == 204

    list_response = client.get("/api/tasks", params={"date": "2026-06-01"})
    assert list_response.json() == []


def test_delete_missing_task_returns_404(client):
    response = client.delete("/api/tasks/9999")
    assert response.status_code == 404


def test_cross_day_isolation(client):
    client.post(
        "/api/tasks",
        json={"title": "Monday", "task_date": "2026-06-01"},
    )
    client.post(
        "/api/tasks",
        json={"title": "Tuesday", "task_date": "2026-06-02"},
    )

    monday = client.get("/api/tasks", params={"date": "2026-06-01"}).json()
    tuesday = client.get("/api/tasks", params={"date": "2026-06-02"}).json()

    assert len(monday) == 1
    assert monday[0]["title"] == "Monday"
    assert len(tuesday) == 1
    assert tuesday[0]["title"] == "Tuesday"
