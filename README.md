# Flask Video Streaming App

This is a Flask web application for streaming video URLs. The app utilizes MongoDB for data storage and hashids for URL shortening. Below is a brief overview of the main components:

## Streaming Video

- **Telegram Stream**: Streams videos with Telegram metadata.

- **View**: Displays videos with a specific URL ID, fetching details from MongoDB.

## Dependencies

- Flask for web framework.
- MongoDB for data storage.
- Hashids for encoding and decoding URL IDs.

Feel free to explore the code for more details and customization options.

**Note:** Ensure that you have the required environment variables set, such as `HASH_SALT`, `MONGO_URL`.
