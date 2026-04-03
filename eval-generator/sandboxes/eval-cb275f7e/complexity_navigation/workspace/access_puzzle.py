# access_puzzle.py

data_store = {
    "users": {
        "alice": {"org_id": "org_a", "roles": ["editor_role"], "is_admin": False, "is_guest": False, "public_profile": False},
        "bob": {"org_id": "org_a", "roles": [], "is_admin": True, "is_guest": False, "public_profile": False},
        "charlie": {"org_id": "org_b", "roles": ["viewer_role"], "is_admin": False, "is_guest": False, "public_profile": True}, # User with public profile in org_b
        "guest_user": {"org_id": "org_a", "roles": [], "is_admin": False, "is_guest": True, "public_profile": False},
        "diana": {"org_id": "org_a", "roles": [], "is_admin": False, "is_guest": False, "public_profile": False}, # No roles, no public profile
        "eliza": {"org_id": "org_a", "roles": ["uploader_role"], "is_admin": False, "is_guest": False, "public_profile": True}, # User with public profile in org_a
    },
    "roles": {
        "editor_role": {"permissions": {"doc_a1": ["read", "write"], "report_a2": ["read"], "public_doc_a": ["read", "write"]}},
        "viewer_role": {"permissions": {"doc_b1": ["read"], "public_doc_b_by_owner": ["read"]}},
        "uploader_role": {"permissions": {"image_a3": ["upload"]}},
    },
    "resources": {
        "doc_a1": {"org_id": "org_a", "visibility": "private", "owner_user_id": "alice"},
        "report_a2": {"org_id": "org_a", "visibility": "private", "owner_user_id": "bob"},
        "image_a3": {"org_id": "org_a", "visibility": "private", "owner_user_id": "eliza"},
        "doc_b1": {"org_id": "org_b", "visibility": "private", "owner_user_id": "charlie"},
        "public_doc_a": {"org_id": "org_a", "visibility": "public", "owner_user_id": "alice"}, # Public by visibility
        "public_doc_b_by_owner": {"org_id": "org_b", "visibility": "private", "owner_user_id": "charlie"}, # Public by owner's public_profile=True
        "public_image_a_by_owner": {"org_id": "org_a", "visibility": "private", "owner_user_id": "eliza"}, # Public by owner's public_profile=True
        "resource_c1": {"org_id": "org_c", "visibility": "private", "owner_user_id": "nobody_exists"}, # Resource in different org, non-existent owner
        "missing_perms_doc_a": {"org_id": "org_a", "visibility": "private", "owner_user_id": "alice"}, # Resource in org_a, but no role grants access
    },
    "organizations": {
        "org_a": {"name": "Alpha Corp"},
        "org_b": {"name": "Beta Inc"},
        "org_c": {"name": "Gamma LLC"},
    }
}

TEST_CASES = [
    # --- Admin Checks (Bob is Admin in org_a) ---
    ("bob", "read", "doc_a1"),
    ("bob", "write", "image_a3"),
    ("bob", "delete", "resource_c1"), # Resource in different org
    ("bob", "read", "non_existent_resource"), # Resource does not exist

    # --- Guest Checks (Guest_user is Guest in org_a) ---
    ("guest_user", "read", "public_doc_a"), # Public by visibility
    ("guest_user", "read", "public_image_a_by_owner"), # Public by owner public profile
    ("guest_user", "write", "public_doc_a"), # Not 'read' action
    ("guest_user", "read", "doc_a1"), # Not public resource
    ("guest_user", "read", "public_doc_b_by_owner"), # Resource in different org

    # --- Regular User Checks (Alice is Editor in org_a) ---
    ("alice", "read", "doc_a1"),
    ("alice", "write", "doc_a1"),
    ("alice", "delete", "doc_a1"), # No 'delete' permission
    ("alice", "read", "report_a2"),
    ("alice", "write", "report_a2"), # No 'write' permission
    ("alice", "read", "public_doc_a"), # Public resource, but Alice has explicit role permission
    ("alice", "write", "public_doc_a"), # Public resource, but Alice has explicit role permission
    ("alice", "read", "public_image_a_by_owner"), # Public resource, but Alice has no explicit role permission
    ("alice", "read", "doc_b1"), # Resource in different org
    ("alice", "read", "missing_perms_doc_a"), # No role grants permission for this resource

    # --- Regular User Checks (Charlie is Viewer in org_b, has public_profile) ---
    ("charlie", "read", "doc_b1"),
    ("charlie", "write", "doc_b1"), # No 'write' permission
    ("charlie", "read", "public_doc_b_by_owner"),
    ("charlie", "read", "public_doc_a"), # Resource in different org

    # --- User with No Roles (Diana in org_a) ---
    ("diana", "read", "doc_a1"), # No roles, not admin/guest
    ("diana", "read", "public_doc_a"), # Not a guest, no roles assigned

    # --- User Eliza (has public_profile, in org_a, uploader_role) ---
    ("eliza", "upload", "image_a3"),
    ("eliza", "read", "public_image_a_by_owner"), # Public by owner, but Eliza has no 'read' role permission

    # --- Edge Cases ---
    ("non_existent_user", "read", "doc_a1"),
    ("alice", "read", "non_existent_resource"),
]

def access_check(user_id: str, action: str, resource_id: str, data_store: dict) -> bool:
    # 1. Existence Checks
    user = data_store['users'].get(user_id)
    resource = data_store['resources'].get(resource_id)
    if not user or not resource:
        return False

    # 3. Organizational Scope
    if user['org_id'] != resource['org_id']:
        return False

    # 2. Admin Bypass (after org check)
    if user.get('is_admin', False):
        return True

    # 5. Public Resources Check
    is_public = False
    if resource.get('visibility') == 'public':
        is_public = True
    else:
        owner_id = resource.get('owner_user_id')
        if owner_id in data_store['users']:
            owner = data_store['users'][owner_id]
            if owner.get('public_profile', False):
                is_public = True

    # 4. Guest Access
    if user.get('is_guest', False):
        return action == 'read' and is_public

    # 6. Regular User Permissions
    user_roles = user.get('roles', [])
    for role_id in user_roles:
        role = data_store['roles'].get(role_id)
        if role and 'permissions' in role:
            if resource_id in role['permissions']:
                if action in role['permissions'][resource_id]:
                    return True
    
    return False

# Main execution for output file generation
if __name__ == "__main__":
    with open("access_check_results.txt", "w") as f:
        for user_id, action, resource_id in TEST_CASES:
            result = access_check(user_id, action, resource_id, data_store)
            f.write(f"{user_id},{action},{resource_id},{result}\n")
