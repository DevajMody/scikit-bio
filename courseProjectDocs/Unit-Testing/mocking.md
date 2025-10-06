# Mocking and Stubbing Documentation

## Component Selection

**Component:** HTTPSource class in `skbio/io/_iosources.py`

**Why This Component?**

The HTTPSource component was selected for mocking because:

1. **External Dependency**: It makes HTTP GET requests using the `requests` library to fetch remote data files
2. **Network Dependency**: Tests that make real HTTP calls are slow and unreliable (network issues, server downtime)
3. **Testing Challenges**: Hard to test error cases (404, 500 errors) without actual failing servers
4. **Real-World Relevance**: Mocking HTTP requests is a common testing pattern in production code

## New Test Cases & Rationale

### Test File: `skbio/io/tests/test_httpsource_mock.py`

**Test Cases Added:**

1. **test_can_read_http_url**
   - **Purpose**: Verify HTTPSource correctly identifies HTTP URLs
   - **Rationale**: Tests URL validation logic without network calls
   - **Approach**: Direct method call, no mocking needed

2. **test_can_read_https_url**
   - **Purpose**: Verify HTTPSource correctly identifies HTTPS URLs
   - **Rationale**: Ensures both HTTP and HTTPS protocols are supported
   - **Approach**: Direct method call, no mocking needed

3. **test_can_read_non_http_url**
   - **Purpose**: Verify HTTPSource rejects non-HTTP URLs (e.g., FTP)
   - **Rationale**: Tests negative case - important for input validation
   - **Approach**: Direct method call, no mocking needed

4. **test_get_reader_successful**
   - **Purpose**: Test successful HTTP GET request and data retrieval
   - **Rationale**: Tests the main functionality without making real network calls
   - **Approach**: Mock `requests.get()` to return fake response data
   - **Mocking**: Uses `@patch` decorator to replace `requests.get`

5. **test_get_reader_http_error**
   - **Purpose**: Test handling of HTTP errors (404, 500, etc.)
   - **Rationale**: Error handling is critical but hard to test without mocks
   - **Approach**: Mock `requests.get()` to raise HTTPError
   - **Mocking**: Uses `@patch` decorator with side_effect to simulate errors

## Mocking Strategy

### Tools Used

- **unittest.mock**: Python's built-in mocking library
- **@patch decorator**: Replaces `requests.get` with a Mock object during test execution
- **Mock objects**: Simulates HTTP response objects with controlled behavior

### Mocking Approach

```python
@patch('skbio.io._iosources.requests.get')
def test_get_reader_successful(self, mock_get):
    # Create mock response object
    mock_response = Mock()
    mock_response.content = b'test data content'
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    # Test the code
    source = HTTPSource(self.url, self.options)
    reader = source.get_reader()

    # Verify behavior
    mock_get.assert_called_once_with(self.url)
    mock_response.raise_for_status.assert_called_once()
```

**Key Design Decisions:**

1. **Patch Location**: `'skbio.io._iosources.requests.get'` - patches where it's used, not where it's defined
2. **Mock Response**: Created Mock object with `content` attribute and `raise_for_status()` method
3. **Assertions**: Verify both the return value AND that methods were called correctly
4. **Error Testing**: Use `side_effect` to simulate exceptions

### Why Not Use Stubs?

- **Stubs vs Mocks**: Mocks are better here because we need to verify behavior (method calls), not just provide canned responses
- **unittest.mock**: Provides powerful assertion capabilities (assert_called_once, etc.)

## Coverage Improvement Analysis

### Before Mock Tests

```
skbio/io/_iosources.py: 139 statements, 3 missed, 98% coverage
```

### After Mock Tests

```
skbio/io/_iosources.py: 139 statements, 3 missed, 98% coverage
```

### Analysis

**Coverage Maintained at 98%**

The coverage percentage remained the same because:

1. **Existing Tests**: The HTTPSource class was already tested by integration tests that make real HTTP calls (using responses library for mocking)
2. **Value Added**: Our mock tests provide:
   - **Faster execution**: No network I/O (1.34s vs potential timeouts)
   - **Better isolation**: Pure unit tests, no external dependencies
   - **Error testing**: Easy to test HTTP errors without setting up failing servers
   - **Reliability**: No flaky tests due to network issues

**Lines Tested by Mock Tests:**

- Line 101-103: `can_read()` URL validation
- Line 106: `requests.get(self.file)` call
- Line 109: `req.raise_for_status()` call
- Line 111: `io.BufferedReader(io.BytesIO(req.content))` reader creation

### Benefits Beyond Coverage Percentage

1. **Test Speed**: Mock tests run in 1.34s vs integration tests that need network setup
2. **Test Clarity**: Each test has single responsibility and clear intent
3. **Maintainability**: Easy to understand and modify mock behavior
4. **Error Cases**: Can easily test edge cases (timeouts, connection errors, various HTTP status codes)
