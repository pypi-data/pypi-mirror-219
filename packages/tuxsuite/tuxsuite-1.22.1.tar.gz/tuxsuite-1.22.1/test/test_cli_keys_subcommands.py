# -*- coding: utf-8 -*-

import sys
import json
import pytest
import tuxsuite


@pytest.fixture
def keys_json():
    keys = {
        "ssh": {"pub": "ecdsa-sha2-nistp256 AAAADianw="},
        "pat": [
            {"token": "****", "username": "test-user-2", "domain": "gitlab.com"},
            {"token": "****", "username": "test-user-4", "domain": "github.com"},
        ],
        "variables": [
            {"value": "****", "keyname": "test-key-2", "type": "file"},
            {"value": "****", "keyname": "test-key-4", "type": "variable"},
        ],
    }
    return json.dumps(keys, indent=True).encode("utf-8")


def test_keys_handle_get(mocker, keys_json, config, response, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "get"])
    response.status_code = 200
    response._content = keys_json
    get_req = mocker.patch("requests.get", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "ssh public key:" in output
    assert exc_info.value.code == 0
    assert get_req.call_count == 1

    # # Test json out
    monkeypatch.setattr(
        sys,
        "argv",
        ["tuxsuite", "keys", "get", "--json"],
    )
    response.status_code = 200
    response._content = keys_json
    get_req = mocker.patch("requests.get", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    assert exc_info.value.code == 0
    assert get_req.call_count == 1

    # Test failure case when the response is not 200
    response.status_code = 400
    response._content = {}
    get_req = mocker.patch("requests.get", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    assert get_req.call_count == 1
    assert exc_info.value.code == 1
    output, error = capsys.readouterr()
    assert "Error: Failed to get the keys\n" == error


def test_keys_handle_add(mocker, keys_json, config, response, monkeypatch, capsys):
    # wrong key kind
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "add", "unknown-kind"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()

    # without required options with kind 'pat'
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "add", "pat"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--domain is required for kind 'pat'" in error
    assert exc_info.value.code == 1

    # without required options with kind 'variables'
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "add", "variables"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--keyname is required for kind 'variables'" in error
    assert exc_info.value.code == 1

    # without username and domain options for kind 'pat'
    mocker.resetall()
    monkeypatch.setattr(
        sys, "argv", ["tuxsuite", "keys", "add", "pat", "--token", "test-token"]
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--domain is required for kind 'pat'" in error
    assert exc_info.value.code == 1

    # without keyname and type options for kind 'variables'
    mocker.resetall()
    monkeypatch.setattr(
        sys, "argv", ["tuxsuite", "keys", "add", "variables", "--vale", "test-value"]
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--keyname is required for kind 'variables'" in error
    assert exc_info.value.code == 1

    # without domain option for kind 'pat'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "add",
            "pat",
            "--token",
            "test-token",
            "--username",
            "test-user-1",
        ],
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--domain is required" in error
    assert exc_info.value.code == 1

    # without type option for kind 'variables'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "add",
            "variables",
            "--value",
            "test-token",
            "--keyname",
            "test-key-1",
        ],
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--type is required for kind 'variables'" in error
    assert exc_info.value.code == 1

    # happy flow for kind 'pat'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "add",
            "pat",
            "--token",
            "test-token",
            "--username",
            "test-user-1",
            "--domain",
            "gitlab.com",
        ],
    )
    response.status_code = 201
    response._content = {}
    post_req = mocker.patch("requests.post", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "'pat' key 'gitlab.com:test-user-1' added\n" == output
    assert post_req.call_count == 1
    assert exc_info.value.code == 0

    # happy flow for kind 'variables'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "add",
            "variables",
            "--value",
            "test-token",
            "--keyname",
            "test-key-1",
            "--type",
            "file",
        ],
    )
    response.status_code = 201
    response._content = {}
    post_req = mocker.patch("requests.post", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "'variables' key 'test-key-1:file' added\n" == output
    assert post_req.call_count == 1
    assert exc_info.value.code == 0

    # failed request for kind 'pat'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "add",
            "pat",
            "--token",
            "test-token",
            "--username",
            "test-user-1",
            "--domain",
            "gitlab.com",
        ],
    )
    response.status_code = 400
    response._content = {}
    post_req = mocker.patch("requests.post", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Error: Failed to add 'pat' key 'gitlab.com:test-user-1'\n" == error
    assert post_req.call_count == 1
    assert exc_info.value.code == 1

    # failed request for kind 'variables'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "add",
            "variables",
            "--value",
            "test-value",
            "--keyname",
            "test-key-1",
            "--type",
            "variable",
        ],
    )
    response.status_code = 400
    response._content = {}
    post_req = mocker.patch("requests.post", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Error: Failed to add 'variables' key 'test-key-1:variable'\n" == error
    assert post_req.call_count == 1
    assert exc_info.value.code == 1


def test_keys_handle_delete(mocker, keys_json, config, response, monkeypatch, capsys):
    # wrong key kind
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "delete", "unknown-kind"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()

    # without required options for kind 'pat'
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "delete", "pat"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--domain is required for kind 'pat'" in error
    assert exc_info.value.code == 1

    # without required options for kind 'variables'
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "delete", "variables"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--keyname is required for kind 'variables'" in error
    assert exc_info.value.code == 1

    # without required options for kind 'pat'
    monkeypatch.setattr(
        sys, "argv", ["tuxsuite", "keys", "delete", "pat", "--domain", "gitlab.com"]
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--username is required for kind 'pat'" in error
    assert exc_info.value.code == 1

    # happy flow for kind 'pat'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "delete",
            "pat",
            "--domain",
            "gitlab.com",
            "--username",
            "test-user-1",
        ],
    )
    response.status_code = 200
    response._content = {}
    delete_req = mocker.patch("requests.delete", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "'pat' key 'gitlab.com:test-user-1' deleted\n" == output
    assert delete_req.call_count == 1
    assert exc_info.value.code == 0

    # happy flow for kind 'variables'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        ["tuxsuite", "keys", "delete", "variables", "--keyname", "test-keyname"],
    )
    response.status_code = 200
    response._content = {}
    delete_req = mocker.patch("requests.delete", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "'variables' key 'test-keyname' deleted\n" == output
    assert delete_req.call_count == 1
    assert exc_info.value.code == 0

    # failed request for kind 'pat'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "delete",
            "pat",
            "--domain",
            "unknown",
            "--username",
            "test-user-1",
        ],
    )
    response.status_code = 400
    response._content = {}
    delete_req = mocker.patch("requests.delete", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Error: Failed to delete 'pat' key 'unknown:test-user-1'\n" == error
    assert delete_req.call_count == 1
    assert exc_info.value.code == 1

    # failed request for kind 'variables'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        ["tuxsuite", "keys", "delete", "variables", "--keyname", "unknown"],
    )
    response.status_code = 400
    response._content = {}
    delete_req = mocker.patch("requests.delete", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Error: Failed to delete 'variables' key 'unknown'\n" == error
    assert delete_req.call_count == 1
    assert exc_info.value.code == 1


def test_keys_handle_update(mocker, keys_json, config, response, monkeypatch, capsys):
    # wrong key kind
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "update", "unknown-kind"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    assert exc_info.value.code == 2

    # without required options for kind 'pat'
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "update", "pat"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--domain is required for kind 'pat'" in error
    assert exc_info.value.code == 1

    # without required options for kind 'variables'
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "update", "variables"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--keyname is required for kind 'variables'" in error
    assert exc_info.value.code == 1

    # without username and domain options for kind 'pat'
    mocker.resetall()
    monkeypatch.setattr(
        sys, "argv", ["tuxsuite", "keys", "update", "pat", "--token", "test-token"]
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--domain is required for kind 'pat'" in error
    assert exc_info.value.code == 1

    # without keyname and type options for kind 'variables'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        ["tuxsuite", "keys", "update", "variables", "--value", "test-value"],
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--keyname is required for kind 'variables'" in error
    assert exc_info.value.code == 1

    # without domain option for kind 'pat'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "update",
            "pat",
            "--token",
            "test-token",
            "--username",
            "test-user-1",
        ],
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--domain is required for kind 'pat'" in error
    assert exc_info.value.code == 1

    # without type option for kind 'variables'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "update",
            "variables",
            "--value",
            "test-value",
            "--keyname",
            "test-key-1",
        ],
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--type is required for kind 'variables'" in error
    assert exc_info.value.code == 1

    # happy flow for kind 'pat'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "update",
            "pat",
            "--token",
            "test-token",
            "--username",
            "test-user-1",
            "--domain",
            "gitlab.com",
        ],
    )
    response.status_code = 201
    response._content = {}
    put_req = mocker.patch("requests.put", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "'pat' key 'gitlab.com:test-user-1' updated\n" == output
    assert put_req.call_count == 1
    assert exc_info.value.code == 0

    # happy flow for kind 'variables'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "update",
            "variables",
            "--value",
            "test-value",
            "--keyname",
            "test-key-1",
            "--type",
            "variable",
        ],
    )
    response.status_code = 201
    response._content = {}
    put_req = mocker.patch("requests.put", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "'variables' key 'test-key-1:variable' updated\n" == output
    assert put_req.call_count == 1
    assert exc_info.value.code == 0

    # failed request for kind 'pat'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "update",
            "pat",
            "--token",
            "test-token",
            "--username",
            "test-user-1",
            "--domain",
            "gitlab.com",
        ],
    )
    response.status_code = 400
    response._content = {}
    put_req = mocker.patch("requests.put", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Error: Failed to update 'pat' key 'gitlab.com:test-user-1'\n" == error
    assert put_req.call_count == 1
    assert exc_info.value.code == 1

    # failed request for kind 'variables'
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "update",
            "variables",
            "--value",
            "test-value",
            "--keyname",
            "test-key-1",
            "--type",
            "file",
        ],
    )
    response.status_code = 400
    response._content = {}
    put_req = mocker.patch("requests.put", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Error: Failed to update 'variables' key 'test-key-1:file'\n" == error
    assert put_req.call_count == 1
    assert exc_info.value.code == 1
