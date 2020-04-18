def sendWarning(approaching, distanceFromUser):
    if (approaching and distanceFromUser < 100):
        print("obstacle in path")
