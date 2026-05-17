def create_user(users, username, password, role):
    if not username or username.strip() == "":
        return False, "Username cannot be empty.", None
    
    if not password or password.strip() == "":
        return False, "Password cannot be empty", None
    
    if not role or role.strip() == "":
        return False, "Role cannot be empty.", None
    
    username = username.strip()
    password = password.strip()
    role = role.strip()
    
    if any(user["name"] == username for user in users):
        return False, "Username already exists.", None
    
    new_user = {
        "name": username, 
        "password": password, 
        "role": role} 
    
    users.append(new_user)

    return True, f"Account for {username} created successfully.", new_user