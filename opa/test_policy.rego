package tests

import future.keywords
import data.policy.allow

admin_token := "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoic3RyaW5nIiwiZW1haWwiOiJzdHJpbmciLCJyb2xlIjp7InR5cGUiOiJhZG1pbiJ9fQ.dqJ25D7XOYmdNNdn46Qa89EAIq5nQshVZwkGAYo1x1Q"
regular_token := "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiam9obiBkb2UiLCJlbWFpbCI6InN0cmluZ0BtYWlsLmRvdCIsInJvbGUiOnsidHlwZSI6InJlZ3VsYXIifX0.BOwjeyGLfo-_wVqVObyiZuLI-XcTbpdzzdDWdhNP_1g"
invalid_admin_token := "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoic3RyaW5nIiwiZW1haWwiOiJzdHJpbmciLCJyb2xlIjp7InR5cGUiOiJhZG1pbiJ9fQ.dqJ25D7XOYmdNNdn46Qa89EAIq5nQshVZwkGAYo1x1Z"

test_allow_to_root_endpoint_no_auth if {
    allow with input as {
        "path": "/"
    }
}


test_get_request_authenticated_regular_user if {
    allow with input as {
        "method": "GET",
        "authorization": regular_token,
        "path": "/api/users"
    }
}

test_get_request_authenticated_admin_user if {
    allow with input as {
        "method": "GET",
        "authorization": admin_token,
        "path": "/api/users"
    }
}


test_invalid_token_request_authenticated if {
    not allow with input as {
        "method": "GET",
        "authorization": invalid_admin_token,
        "path": "/api/users"
    }
}

test_unauthenticated_get if {
    not allow with input as {
        "method": "GET",
        "path": "/api/users"
    }
}


test_unauthenticated_post if {
    not allow with input as {
        "method": "GET",
        "path": "/api/users"
    }
}

test_post_request_admin if {
    allow with input as {
        "authorization": admin_token,
        "method": "POST",
        "path": "/api/users"
    }
}

test_post_request_non_admin if {
    not allow with input as {
        "authorization": regular_token,
        "method": "POST",
        "path": "/api/users"
    }
}

test_post_request_non_admin if {
    not allow with input as {
        "authorization": invalid_admin_token,
        "method": "POST",
        "path": "/api/users"
    }
}
