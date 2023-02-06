import sys

temperature = int(sys.argv[1])
if temperature > 80:
    print("Too hot")
elif 65 <= temperature <= 80:
    print("Quite nice")
else:
    print("Too cold")
