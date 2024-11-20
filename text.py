import cv2
import numpy as np
from moviepy.editor import VideoClip, AudioFileClip, VideoFileClip
from gtts import gTTS

# Main function to drive the script
def main():
    text = "Welcome to the animated video. Here's your image in motion!"
    
    # Directly specify the image path here
    image_path = r"C:\\Users\\Junior\\Downloads\\clean_sekol_head.png"

    audio_file = "output_audio.mp3"
    video_file = "animated_video.mp4"
    output_file = "final_output.mp4"

    text_to_audio(text, audio_file)  # Generate the audio from the text
    duration = get_audio_duration(audio_file)  # Get the duration of the audio
    words = text.split()  # Split the text into words
    word_duration = duration / len(words)  # Duration of each word

    create_image_animation(image_path, duration, words, word_duration, video_file)  # Create the animation
    combine_audio_video(video_file, audio_file, output_file)  # Combine video and audio

    print(f"Animation with audio saved as {output_file}")

# Function to generate audio from text
def text_to_audio(text, output_audio):
    print("Generating audio from text...")
    tts = gTTS(text, lang="en")
    tts.save(output_audio)
    print(f"Audio saved as {output_audio}")

# Function to get the duration of the audio file
def get_audio_duration(audio_file):
    audio = AudioFileClip(audio_file)
    duration = audio.duration
    audio.close()
    return duration

# Function to create animation using a predefined image
def create_image_animation(image_path, duration, words, word_duration, output_video):
    # Load the image using OpenCV
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Unable to load image. Check the file path: {image_path}")
    
    # Convert the image from BGR to RGB to prevent color distortion
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_height, img_width, _ = img.shape

    # Define the region of interest (ROI)
    roi_x, roi_y, roi_w, roi_h = 228, 332, 135, 194  # Example coordinates for the ROI

    # The maximum allowed movement for the ROI
    max_movement_up = 50  # How far the ROI can move up
    max_movement_down = 100  # How far the ROI can move down

    def make_frame(t):
        # Create a copy of the image as the background
        frame = img.copy()

        # Draw a black rectangle behind the ROI (black background for the region)
        frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w] = [0, 0, 0]  # RGB color for black

        # Crop the region of interest (ROI) from the image (no resizing)
        roi_img = img[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

        # Find the index of the current word based on the time
        current_word_index = int(t / word_duration)
        if current_word_index >= len(words):
            current_word_index = len(words) - 1  # Ensure it doesn't exceed the word list

        # Calculate the vertical position for the ROI's animation (up and down)
        # Linear movement to allow the ROI to move down and up smoothly
        movement_factor = (t % word_duration) / word_duration  # Value from 0 to 1 for each word
        animated_y = roi_y + (max_movement_down * movement_factor)  # Moving down gradually

        # Limit upward movement to not exceed the starting position
        if animated_y > roi_y + max_movement_down:
            animated_y = roi_y + max_movement_down  # Make sure it doesn't go past the max downward limit

        # Convert animated_y to an integer
        animated_y = int(animated_y)

        # Ensure the region does not go out of bounds (if animated_y goes beyond image height)
        if animated_y + roi_h > img_height:
            animated_y = img_height - roi_h  # Make sure it fits within the image

        # Overlay the animated ROI on the image at the new vertical position
        frame[animated_y:animated_y + roi_h, roi_x:roi_x + roi_w] = roi_img

        return frame

    # Create a VideoClip from the frames
    animation_clip = VideoClip(make_frame, duration=duration)
    animation_clip.write_videofile(output_video, fps=24)

# Function to combine the audio and video
def combine_audio_video(video_file, audio_file, output_file):
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)
    video = video.set_audio(audio)
    video.write_videofile(output_file, codec="libx264", fps=24, audio_codec="aac")

# Run the main function
if __name__ == "__main__":
    main()
