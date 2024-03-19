## 1. SignIn with root account

![](images/08_signin_with_root_account.png)

----------------

## 2. Create an admin account
- After first sign-in and create admin account you barely use root account.
- It is the best security practice not to use root account.

### 2.1. Create admin group
#### Open iam service
![](images/09_open_iam_service.png)

------------------

#### Create a user group

![](images/10_create_user_group.png)

--------------------

#### Attach permission to group
1. Name the group. Ih here **admin** used.
2. Filter permission policies. User AdministratorAccess filter.
3. Select built-in AdministratorAccess policy.

![](images/11_attach_permission_to_group.png)

----------------

- Click Create Group

#### See the group
![](images/12_see_the_user_group.png)

-------------------

### 2.2. Create admin user
#### Add user
![](images/13_create_a_user.png)

------------------

#### User details
![](images/14_add_user_details.png)

------------------

#### Set permissions
- Note that we have just created above this admin group.
![](images/15_set_permissions_to_user.png)

------------------

#### Continue with defaults following steps

#### Download credentials csv

![](images/16_download_credentials.png)

---------------

