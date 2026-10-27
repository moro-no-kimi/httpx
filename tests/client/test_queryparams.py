import httpx


def hello_world(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, text="Hello, world")


def test_client_queryparams():
    client = httpx.Client(params={"a": "b"})
    assert isinstance(client.params, httpx.QueryParams)
    assert client.params["a"] == "b"


def test_client_queryparams_string():
    client = httpx.Client(params="a=b")
    assert isinstance(client.params, httpx.QueryParams)
    assert client.params["a"] == "b"

    client = httpx.Client()
    client.params = "a=b"
    assert isinstance(client.params, httpx.QueryParams)
    assert client.params["a"] == "b"


def test_client_queryparams_echo():
    url = "http://example.org/echo_queryparams"
    client_queryparams = "first=str"
    request_queryparams = {"second": "dict"}
    client = httpx.Client(
        transport=httpx.MockTransport(hello_world), params=client_queryparams
    )
    response = client.get(url, params=request_queryparams)

    assert response.status_code == 200
    assert response.url == "http://example.org/echo_queryparams?first=str&second=dict"


def test_client_get_preserves_repeated_queryparams_in_order():
    requests = []

    def inspect_request(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200)

    with httpx.Client(transport=httpx.MockTransport(inspect_request)) as client:
        response = client.get(
            "http://example.org/", params=[("tag", "python"), ("tag", "ml")]
        )

    assert response.status_code == 200
    assert requests[0].url.params.multi_items() == [
        ("tag", "python"),
        ("tag", "ml"),
    ]


def test_client_get_with_empty_queryparams_has_no_query():
    requests = []

    def inspect_request(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200)

    with httpx.Client(transport=httpx.MockTransport(inspect_request)) as client:
        response = client.get("http://example.org/", params=[])

    assert response.status_code == 200
    assert requests[0].url.query == b""
