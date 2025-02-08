import praw
import requests
import os

# Reddit API Credentials
REDDIT_CLIENT_ID = "HJG70Y4rZ6SGk1F9unEY8g"
REDDIT_CLIENT_SECRET = "qFq5gT2tNjMfyHsX4aFNqNnXKKetnA"
REDDIT_USERNAME = "ExistingPain9212"
REDDIT_PASSWORD = "Mudar!@#12"
USER_AGENT = "script:copy_top_post:v1.0 (by u/your_username)"

# Define the target subreddit where the post will be copied
TARGET_SUBREDDIT = "100thupvote"

# Authenticate with Reddit
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    user_agent=USER_AGENT,
)

# Get the most upvoted post of the day from r/all
top_post = next(reddit.subreddit("all").top(time_filter="day", limit=1))

title = top_post.title
content = top_post.selftext  # Text content if available
url = top_post.url  # URL (for links and images)

# Check if the post is an image
image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".webp")

if url.endswith(image_extensions):
    # Download the image
    image_filename = "temp_image.jpg"
    response = requests.get(url)
    with open(image_filename, "wb") as f:
        f.write(response.content)

    # Upload image to target subreddit
    new_post = reddit.subreddit(TARGET_SUBREDDIT).submit_image(title, image_filename)

    # Delete the temp image after uploading
    os.remove(image_filename)

elif content:
    # If it's a text post, repost it as text
    new_post = reddit.subreddit(TARGET_SUBREDDIT).submit(title, selftext=content)

else:
    # Otherwise, it's a link post
    new_post = reddit.subreddit(TARGET_SUBREDDIT).submit(title, url=url)

print(f"Reposted: {new_post.title} - {new_post.shortlink}")
