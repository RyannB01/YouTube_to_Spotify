import googleapiclient.discovery
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def display_menu_and_get_choice(items, prompt="Select an option:"):
    """
    Displays a menu from a list of items and prompts the user to select one.

    Parameters:
    - items (list): A list of items to display.
    - prompt (str): A custom prompt message for user input.

    Returns:
    - The selected item from the list.
    """
    while True:
        print("\nPlease select one of the following options:")
        for i, item in enumerate(items, start=1):
            print(f"{i}. {item}")
        print("x. Skip")
        try:
            
            choice = input(f"{prompt} ")
            if str(choice) == "x":
                return 11
            choice= int(choice)
            if 1 <= choice <= len(items):
                return choice - 1
            else:
                print(f"Invalid choice. Please choose a number between 1 and {len(items)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# YouTube API setup
def get_playlist_videos(playlist_id, api_key):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    videos = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            maxResults=50,
            playlistId=playlist_id,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            title = item['snippet']['title']
            videos.append({"title": title })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return videos


# Spotify API setup
def create_spotify_playlist(user_id, playlist_name):
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
    return playlist['id']

def add_tracks_to_playlist(playlist_id, track_titles):
    track_ids = []
    
    for title in track_titles:
        search = sp.search(q=title, type="track", limit=10)
        track_id = search['tracks']['items']
        track_names = [track['name'] for track in track_id]
        
        # Add a "Skip" option to the menu
        
        track_len=len(track_names)
        # Display menu and get user's choice
        index = display_menu_and_get_choice(track_names, f"Select a track for '{title}':")
        
        if index > track_len:  # If "Skip" was selected
            print(f"Skipping '{title}'...")
            continue  # Skip adding the track

        if track_id:
            track_ids.append(track_id[index]['id'])
    
    # Add the selected tracks to the playlist
    if track_ids:
        sp.playlist_add_items(playlist_id, track_ids)
        print(f"Added {len(track_ids)} tracks to the playlist.")
    else:
        print("No tracks were added.")


# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="",  # Replace with your actual Client ID
    client_secret="",  # Replace with your actual Client Secret
    redirect_uri="http://localhost:8888/callback",  # Make sure this matches your Redirect URI
    scope=["playlist-modify-public", "playlist-modify-private", "user-library-read"]))

# Get YouTube playlist videos
youtube_api_key = ""  # Replace with your YouTube API key
youtube_playlist_id = ""  # Replace with your YouTube playlist ID

videos = get_playlist_videos(youtube_playlist_id, youtube_api_key)

# Extract URLs from the YouTube playlist
track_titles = [video['title'] for video in videos]

# Get the user's Spotify user ID
user_id = sp.current_user()['id']

# Create a new playlist on Spotify
playlist_id = create_spotify_playlist(user_id, "My YouTube Playlist")

# Add tracks to the new Spotify playlist
add_tracks_to_playlist(playlist_id, track_titles)

print(f"Playlist created successfully with {len(track_titles)} tracks!")
