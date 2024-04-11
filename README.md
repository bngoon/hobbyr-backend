## Model Architecture

### Overview

Our Django backend uses a series of models to manage user profiles, projects, and interactions such as following, favorites, and comments. This section provides a breakdown of each model and its role within the application.

### Models

1. **UserProfile**

   - **Description**: Represents a user profile in our system.
   - **Fields**:
     - `user`: A one-to-one link to Django’s built-in User model.
     - `username`: The user's chosen username.
     - `profile_pic`: A URL to the user’s profile picture.
     - `bio`: A short text describing the user.

2. **Project**

   - **Description**: Represents a project created by a user.
   - **Fields**:
     - `user_profile`: A link to the UserProfile of the user who owns the project.
     - `project_title`: The title of the project.
     - `project_type`: The type of project (e.g., Tech, Carpentry, etc.), with predefined choices.
     - `project_img`: An image of the project, stored in a specified directory.
     - `body`: Detailed description of the project.
     - `link`: Optional link to additional project resources.
     - `created_at`: Timestamp for when the project was created.
     - `updated_at`: Timestamp for the last update to the project.

3. **Follow**

   - **Description**: Tracks the following relationships between users.
   - **Fields**:
     - `following`: The user who is being followed.
     - `followers`: The user who follows.

4. **Favorite**

   - **Description**: Represents the projects that a user has marked as favorite.
   - **Fields**:
     - `projects`: The project that has been favorited.
     - `user_profile`: The user profile that favorited the project.

5. **Comment**
   - **Description**: Represents comments made on projects.
   - **Fields**:
     - `projects`: The project on which the comment is made.
     - `user_profiles`: The user profile of the commenter.
     - `comment_body`: The text of the comment.
     - `created_at`: Timestamp for when the comment was created.
     - `updated_at`: Timestamp for the last update to the comment.

### Relationships

- **UserProfiles** and **Projects** are linked, allowing for a clear view of who created each project.
- **Follow**, **Favorite**, and **Comment** models facilitate interaction between users and content, enhancing the community aspect of the platform.

### Diagram

![Entity-Relationship Diagram](images/image-1.png)
