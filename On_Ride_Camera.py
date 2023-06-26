import cv2
import time

# Initialize the camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Failed to open camera")
    exit()

# Start the countdown
countdown_start = time.time()
countdown_duration = 5

# Load the image mask
image_mask = cv2.imread('image_mask.png', cv2.IMREAD_UNCHANGED)

while True:
    # Calculate the time remaining in the countdown
    countdown_remaining = countdown_duration - int(time.time() - countdown_start)

    # Read a frame from the camera
    ret, frame = cap.read()

    # Display the countdown on the frame
    cv2.putText(frame, str(countdown_remaining), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('On-Ride Camera', frame)

    # Break the loop when the countdown is complete
    if countdown_remaining <= 0:
        break

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Capture a frame after the countdown
ret, frame = cap.read()

# Check if the frame was captured successfully
if ret:
    # Resize the image mask to match the frame dimensions
    image_mask = cv2.resize(image_mask, (frame.shape[1], frame.shape[0]))

    # Create a 3-channel mask
    mask = cv2.cvtColor(image_mask, cv2.COLOR_BGRA2BGR)

    # Apply the image mask to the frame
    masked_frame = cv2.bitwise_and(frame, cv2.bitwise_not(mask))
    masked_frame = cv2.bitwise_or(masked_frame, mask)

    # Save the masked frame as an image file
    output_file = 'on_ride_image.png'
    cv2.imwrite(output_file, masked_frame)
    print(f"Image captured and saved as {output_file}")
else:
    print("Failed to capture frame")

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
