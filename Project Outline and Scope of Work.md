## Project Outline

### 1. Introduction
- **Purpose**: Building an image directory browser web app using FastAPI/Flask with ReactJS frontend, without a database for easy management.
- **Objective**: A file-based system to manage images across different directories, update JSON files for each feature.

### 2. Project Structure

#### Frontend (ReactJS)

1. Homepage: Image Viewer
   - Displays all images in the selected directory like a contact sheet [1].
   - URL: /
   - **Features:**
     - Pagination
     - Search functionality
     - Sorting by filename or rating
     - Icons beneath each photo for trash, star ratings (1-4), and checkmark (5)

2. Details Page:
   - Large image view with thumbnails of other images.
   - URL: /details?image={filename}
   - **Features:**
     - Navigation using left/right arrows or thumbnail slider
     - Clickable and touch-enabled slider for mobile responsiveness

3. Trash Page:
   - Contact sheet for trashed images with restore and permanent delete options.
   - URL: /trash
   - **Features:**
     - Restore button beneath each image
     - Erase all button at the top of page

4. Picks Page:
   - Viewer for images marked as picks.
   - URL: /picks
   - **Features:**
     - Contact sheet layout
     - Demote button beneath each image to move back to base directory and demote rating to 4 stars
     - Active checkmark for already picked images

5. Settings Page:
   - Navigate to different directories.
   - URL: /config

6. Login Screen
   - Just password input and submit button

#### Backend (FastAPI/Flask)

1. API Endpoints
   - Set Base Directory
      - path stored in global '.json' configuration file
   - Fetch images from directory.
   - Move image to base directory.
   - Move image to trash directory.
      - creates directory if it does not exist
   - Move image to pics directory.
      - also gives image a star rating of 5
      - creates directory if it does not exist
   - Delete all images in trash directory
   - Rate Image
      - Star rating 1-5
      - Star Rating of 5 is a pick
      - stored in {filename}.json file
      - creates file if it does not exits
   - Add Image Prompt
      - used for lora training
      - stored in plain text {filename}.txt file
      - creates file if it does not exits
   - Add Notes to Image
      - adds notes about image
      - stored in {filename}.json file
      - creates file if it does not exits
   - Authentication:
      - password protection, single password
      - stored in global .json configuration file

2. Configuration
   - CORS settings for security [1].

### 3. Features

#### Homepage/View Page
- Display all images with icons beneath each photo:
  - X icon: Move to trash directory.
  - Star rating icons: Rate image (1-4).
  - Checkmark: Move to picks directory, Rate image (5).

#### Trash Page
- Contact sheet layout for trashed images.
- Restore button to move image back to normal directory and homepage list.
- Erase button at the top to permanently delete all images in trash.

#### Picks Page
- Contact sheet layout for all Picked images.
- X icon: Move to trash directory.
- Star rating icons: Rate image (1-4).
- Checkmark: Move to picks directory, 
   - Rate image (5), 
   - Checkmark should be active

#### Details Page
- Large image view
- Star rating, Pick, and Delete icons.
- Notes Field.
- Prompt Field
- Navigation using left/right arrows to select next/previous image.
- Thumbnail slider of all images in the directory for easy navigation (click to select).

#### Configs Page
- Has ability to set base directory

#### Authentication Page
- Password Input
- Submit Button
   - Return Key will Submit

### 4. Tools & Technologies
- **Backend**: Python (FastAPI or Flask)
- **Frontend**: ReactJS
- **Styling**: Tailwind CSS

### 5. React Directory Structure

- **React Components**: 
   - Header
   - Footer
   - ImageCard
      - identifies page changes footer accordingly
   - ThumbnailSlider
   - ImageSidebar
      - Navigation Selector
         - Left, Right Arrows (selects previous, next image)
      - Star Rater
      - Prompt Textarea
      - Notes Textarea
   - Authentication

- **Pages**:
   - Homepage
   - DetailsPage
   - TrashPage
   - PicksPage
   - AuthenticationPage
   - SettingsPage (if kept separate).

- **Utilities**: 
   - API calls
   - Error handling
   - Helper functions
   - CORS configuration.

## Scope of Work

### Phase 1: Project Setup

1. **Environment Setup**
   - Set up FastAPI/Flask backend.
   - Set up React frontend project.
      - We are using Vite to make the install process faster
      - js files are .jsx

2. **Directory Structure**
   - Create folders for components, pages, and utilities.

3. **CORS Configuration**
   - Configure CORS settings in Flask/FastAPI to secure the API.

### Phase 2: Backend Development

1. **Image Handling Endpoints**
   - Fetch images from a specified directory.
   - Move images between directories (trash, picks).
   - Create and Update JSON metadata files stored next to image files.
   - Create and Update .txt files (Prompt) for Lora training.

2. **Authentication Endpoint**
   - Password Input
   - Submit Button
      - Return Key will Submit

3. **API Testing**
   - Test all endpoints using Postman or similar tools.

### Phase 3: Frontend Development
1. **Header Implementation**
   - Global Header
      - ImageViewer Top Left
      - Global Navigation Top Right
         - Home
         - Picks
         - Trash
         - Config
2. **Homepage/View Page Implementation**
   - Create the contact sheet layout with icons beneath each photo.
   - Pagination
   - Search Functionality
   - Sorting Options
3. **Trash Page Implementation**
   - Contact sheet for Trashed images 
   - Has Restore button beneath each Image
   - Has One 'Erase All' Button at top of page.
4. **Picks Page Implementation**
   - Page Layout Selector
      - Contact Sheet
      - Enlarged Active Image
         - Image Slider at bottom with all Picked Images
   - Has Demote button beneath each Image
      - Moves Image back to base directory
      - Demotes image to 4 Star 
5. **Details Page Implementation**
   - Large image view
   - Right side column has
      - Filename
      - Navigation controls (Left, Right Triangles or Arrows)
      - Star Rating
      - Notes Textarea
      - Prompt Textarea
   - Bottom Footer
      - Thumbnail Slider with all Images in Directory
6. **Configuration Page Implementation**
   - Various settings for current.
      - Currently sets Base Directory.
7. **Authentication Page Implementation**
   - 

### Phase 4: Integration
1. **API & Frontend Integration**
   - Connect React frontend to the FastAPI/Flask backend.
2. **Styling with Tailwind CSS**
   - Apply styling and layout using Tailwind CSS for all pages.

### Phase 5: Testing
- **Functional Testing**: Ensure all features work as intended.
   - Create testing directory with 20 images
   - Test each API endpoint and verify they function as expected
   - Create Testing suite for React (Jest???)
      - Verify all components exist and function
- **User Testing**: Gather feedback from users (if applicable).
   - Visual Function testing

### Phase 6: Deployment
1. **Local Deployment**
   - Test the application locally to ensure it runs smoothly.
2. **Production Deployment**
   - Consider deploying on AWS using a custom Docker image in the future if needed.
