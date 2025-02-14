import praw
import datetime
import requests
import os
import time

# 🔹 Reddit API Credentials
REDDIT_CLIENT_ID = "HJG70Y4rZ6SGk1F9unEY8g"
REDDIT_CLIENT_SECRET = "qFq5gT2tNjMfyHsX4aFNqNnXKKetnA"
REDDIT_USER_AGENT = "your_user_agent"
REDDIT_USERNAME = "ExistingPain9212"
REDDIT_PASSWORD = "Mudar!@#12"

# 🔹 Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD
)

# ✅ Debug: Check authentication
print(f"✅ Logged in as: {reddit.user.me()}")

# 🔹 Target subreddit for reposting
TARGET_SUBREDDIT = "100thupvote"

# 🔹 Ignore these subreddits
IGNORED_SUBREDDITS = {"AITAH"}

# 🔹 List of Countries to Fetch
COUNTRIES = ["South Africa", "Nigeria", "Kenya", "Somalia", "Sudan", "Ethiopia", "Madagascar", "Egypt", "Saudi Arabia", "UAE", "Yemen", "Oman", "Iran", "Iraq", "Syria", "Pakistan", "Turkey", "Thailand", "Indonesia", "Singapore", "Philippines", "South Korea", "Japan", "Brazil", "Argentina", "Colombia", "India", "Australia", "New Zealand", "China", "Russia", "Ukraine", "Germany", "Austria", "France", "Italy", "Spain", "Denmark", "Norway", "Sweden", "Finland", "UK", "Ireland", "Iceland", "Greenland", "Mexico", "Canada", "US"]  # Add more if needed

# 🔹 Flair Mapping (Customize as needed)
FLAIR_MAP = {
    "India": "India",
    "USA": "USA",
    "Canada": "Canada",
    "Germany": "Germany",
    "Australia":"Australia",
    "South Africa": "South Africa",
    "Nigeria": "Nigeria",
    "Kenya": "Kenya",
    "Somalia": "Somalia",
    "Sudan": "Sudan",
    "Ethiopia": "Ethiopia",
    "Madagascar": "Madagascar",
    "Egypt": "Egypt",
    "Saudi Arabia": "Saudi Arabia",
    "UAE": "UAE",
    "Yemen": "Yemen",
    "Oman": "Oman",
    "Iran": "Iran",
    "Iraq": "Iraq",
    "Syria": "Syria",
    "Pakistan": "Pakistan",
    "Turkey": "Turkey",
    "Thailand": "Thailand",
    "Indonesia": "Indonesia",
    "Singapore": "Singapore",
    "Philippines": "Philippines",
    "South Korea": "South Korea",
    "Japan": "Japan",
    "Brazil": "Brazil",
    "Argentina": "Argentina",
    "Colombia": "Colombia",
    "New Zealand": "New Zealand",
    "China": "China",
    "Russia": "Russia",
    "Ukraine": "Ukraine",
    "Austria": "Austria",
    "France": "France",
    "Italy": "Italy",
    "Spain": "Spain",
    "Denmark": "Denmark",
    "Norway": "Norway",
    "Sweden": "Sweden",
    "Finland": "Finland",
    "UK": "UK",
    "Ireland": "Ireland",
    "Iceland": "Iceland",
    "Greenland": "Greenland",
    "Mexico": "Mexico"
}

DEFAULT_FLAIR = "🌍 Global News"  # Used if no matching flair is found

def search_top_post(query, min_comments=1):
    """Search Reddit for a query, sorted by comments, and posted today, ignoring specific subreddits."""
    today_start = int(datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())

    print(f"🔍 Searching for: {query}")

    for post in reddit.subreddit("all").search(query, sort="comments", time_filter="day", limit=5):
        print(f"🔎 Checking post: {post.title} ({post.num_comments} comments) in r/{post.subreddit.display_name}")

        if post.num_comments >= min_comments and post.created_utc >= today_start:
            if post.subreddit.display_name not in IGNORED_SUBREDDITS:
                print(f"✅ Found match: {post.title}")
                return post

    print(f"❌ No matching post found for {query}.")
    return None

def get_flair_id(subreddit, flair_text):
    """Finds the flair ID based on text from the subreddit flair list."""
    try:
        for flair in subreddit.flair.link_templates:
            if flair["text"] == flair_text:
                return flair["id"]
    except Exception as e:
        print(f"⚠️ Error fetching flairs: {e}")
    return None

def repost_to_subreddit(post, country):
    """Reposts the found post into a target subreddit and assigns flair."""
    if not post:
        print("❌ No post to repost.")
        return

    title = post.title
    subreddit = reddit.subreddit(TARGET_SUBREDDIT)

    # 🔹 Determine Flair
    flair_text = FLAIR_MAP.get(country, DEFAULT_FLAIR)
    flair_id = get_flair_id(subreddit, flair_text)

    # 🔹 Post the text or image
    if post.selftext.strip():
        print(f"📝 Posting text post: {title}")
        new_post = subreddit.submit(title=title, selftext=post.selftext.strip(), flair_id=flair_id)
    else:
        print(f"🖼 Posting image post: {title}")
        new_post = subreddit.submit(title=title, url=post.url, flair_id=flair_id)

    # 🔹 Create a pinned comment with details
    post_details = (
        f"📌 **Original Post Details** 📌\n\n"
       # f"👤 **Author:** u/{post.author.name if post.author else '[Deleted]'}\n"
        f"📌 **Subreddit:** r/{post.subreddit.display_name}\n \n"
        f"👍 **Upvotes:** {post.score}\n \n"
        f"💬 **Comments:** {post.num_comments}\n \n"
        f"🔗 **Original Post:** [View Here](https://www.reddit.com{post.permalink})\n \n"
    )

    pinned_comment = new_post.reply(post_details)
    pinned_comment.mod.distinguish(sticky=True)  # Pin the comment
    print(f"✅ Reposted: {new_post.url}")
    print(f"📌 Pinned comment: {pinned_comment.permalink}")
    print(f"🏷️ Flair Applied: {flair_text}")

def fetch_and_post_all():
    """Fetches top posts for all countries and posts them one by one."""
    for country in COUNTRIES:
        query = f'"{country}" "news"'
        print(f"\n🌍 Searching for news in: {country}")

        top_post = search_top_post(query)

        if top_post:
            repost_to_subreddit(top_post, country)
            print(f"✅ Successfully reposted for {country}\n")
        else:
            print(f"⚠️ No post found for {country}, skipping...\n")

        time.sleep(40)  # Prevents hitting Reddit rate limits

# 🔹 Start the multi-country fetching & posting
fetch_and_post_all()


