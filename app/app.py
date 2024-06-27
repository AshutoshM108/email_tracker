from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import datetime
import urllib.request
from starlette.background import BackgroundTask

app = FastAPI()

# Serve a default page. This function is not required. Serving up a spy.gif for the homepage.
@app.get('/')
def my_function():
    spy_meme = "https://elasticbeanstalk-us-west-2-637423406470.s3.us-west-2.amazonaws.com/pixel.png"
    return FileResponse(spy_meme, media_type="image/gif")

@app.get('/image')
async def my_spy_pixel(request: Request):
    # File path and name for 1 x 1 pixel. Must be an absolute path to pixel.
    filename = "https://elasticbeanstalk-us-west-2-637423406470.s3.us-west-2.amazonaws.com/pixel.png"

    # Log the User-Agent String.
    user_agent = request.headers.get('User-Agent')

    # Get the current time of request and format time into readable format.
    current_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(current_time, "%Y-%m-%d %H:%M:%S")

    # Log the IP address of requester.
    get_ip = request.client.host

    # Lookup Geolocation of IP Address.
    with urllib.request.urlopen(f"https://geolocation-db.com/jsonp/{get_ip}") as url:
        data = url.read().decode()
        data = data.split("(")[1].strip(")")

    # Add User-Agent, Timestamp, and IP Address + Geolocation information to dictionary.
    log_entry = f"Email Opened:\nTimestamp: {timestamp}\nUser Agent: {user_agent}\nIP Address: {data}\n"

    # Write log to hardcoded path. Must be an absolute path to the log file.
    def write_log():
        with open(r"C:\Users\Lenovo\Desktop\spy-pixel-main\app\spy_pixel_logs.txt", 'a') as f:
            f.write(log_entry)

    # Serve a transparent pixel image when navigating to .../image URL. "image/png" displays the image in PNG format.
    return FileResponse(filename, media_type="image/png", background=BackgroundTask(write_log))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)