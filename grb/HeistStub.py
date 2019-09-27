from gurobipy import *

# List of pieces which are stored within a bounding rectangle
# Each piece has two entries, one for each side
# Coded as:
#   - is a blank square
#   . is a lock
#   X is a missing square
#   | is the end of the piece
#     other letters are colours White, Blue, Red, Green

PData = [
  ["-.-|.-X", "W-.|X.-"],
  [".XX|-.-|XX.", "XX-|.-.|-XX"],
  ["-.-|.XX|-XX", "-.-|XXW|XX-"],
  ["-X-|.-.", "-X-|.-R"],
  ["X.X|.-X|X.-", "X-X|X.-|.-X"],
  ["X.|.-|X.|X-", "-X|.-|-X|.X"],
  ["X.|.-|X.", ".X|-.|RX"],
  ["B-X|X.-|XX.", "X-.|-.X|.XX"],
  ["X-X|-.-|X-X", "X.X|.-.|X.X"],
  [".-.-.", ".-.-G"],
  ["X-|-.|.X|-X", ".X|-.|X-|X."],
  ["X.|X-|X.|.-", "-X|.X|-X|.-"],
  ["XX-|.-B|XX-", "-XX|.-.|-XX"]
]

# Challenge 1 is RBW in corner
BData1 = [
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-R",
  ".-.-.-B-",
  "-.-.-W-."]

BData2 = [
  ".-.-.-.-",
  "-R-.-.-.",
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-W-",
  "-.-.-.-."]

BData3 = [
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-W-",
  "-.-.-.-."]

BData4 = [
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-."]

BData = BData1

