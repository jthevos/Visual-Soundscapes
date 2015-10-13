##
#   Author:     Katie May, John Thevos
#   Email:      mayka@g.cofc.edu, thevosjg@g.cofc.edu
#   Class:      CSCI 180, Section 1 
#   Assignment: Final Project
#   Due Date:   12/08/11
#
#   Certification of Authenticity:     
#
#      We certify that this lab is entirely our own work, but compiled
#         with parts of Professor Manaris' code.
#
#   Purpose: The purpose of this piece was to sonify an image that we had chosen.
#            We wanted to create an aestheically appealing song, using codes to find
#             notes within our chosen photo of a landscape from Iceland. We also aimed
#             to add our own parts, and creating a simple code to find specific rows and colums.
#
#   Input: What went into this piece was using the read.Image code to find rhythm inside our chosen photo.
#           We spent a lot of time trying to find the perfect rows and triads to create a piece that 
#           sounded nice and appealing.
#
#   Output: The program generates a melody produced by the whole image, while being layered
#           with the code that produces a specific row and colum. We also added some parts to
#           add more layering.

#Iceland2.py     version 1.1     25-Nov-2011     
#
# Demonstrates how to create a soundscape from an image.  It also demonstrates how to use functions.
# It loads a jpg image and scans it from left to right.  Pixels are mapped to notes, where:
# 
# * left-to-right pixel x position - width) is start time, 
# * top-to-bottom (pixel y position - height) is panoramic (top is left, bottom is right), 
# * luminosity (avg RGB value) is pitch (the brighter the pixel, the higher the pitch), 
# * redness (R value) is duration (the reder the pixel, the longer the note), and 
# * blueness (B value) is dynamic (the bluer the pixel, the louder the note).
#
# This creates a soundscape using overlapping sounds created through FM synthesis.
#

from music import *
from random import *
#import SimpleFMInst

# read in image (image origin (0, 0) is at upper left)
image = Image("iceland2.jpg")
width = image.getWidth()     # number of columns in the image
height = image.getHeight()   # number of rows in the image


# number of notes per image column to generate
numNotesPerColumn = 4

##### define synthesized instruments
FMSynthesisInst = SimpleFMInst(44100, 800, 34.4) # 44100Hz sample rate, 800 modulation index, and 34.4 modulation ratio
synthesizedInstruments = [FMSynthesisInst]       # synthesized instruments to render music

##### define data structure all Parts included with the synthesized instruments
synthesizedScore = Score("Image Soundscape", 60)
synthesizedPart  = Part ("FMSynthesisInst", 4, 0)   # index 0 means first instrument
synthesizedPart2 = Part ("FMSynthesisInst", 4, 1)
synthesizedPart3 = Part ("FMSynthesisInst", 4, 2)
synthesizedPart4 = Part ("FMSynthesisInst", 4, 3)
synthesizedPart5 = Part ("FMSynthesisInst", 4, 4)
synthesizedPart6 = Part ("FMSynthesisInst", 4, 5)

##### define needed functions
def sonifyPixelDiatonic(pixel, position, maxPosition, pitchSet):
   """It returns a note created from sonifying the red, green, and blue values of 'pixel', e.g., [255, 0, 0],
      using 'pitchSet'.
      This pixel comes from the given 'position' in the image, where the maximum is 'maxPosition'.
      
      NOTE: 'pitchSet' consists of pitch intervals within an octave (0 to 11).  The intervals are listed
             starting from 0 and should ordered, unique (i.e., no duplicates), and less than 12, 
             e.g., [0, 2, 4, 5, 7, 9, 11] (which happens to be the major scale).
   """
   # get pixel value (RGB)
   red, green, blue = pixel
   luminosity = (red + green + blue) / 3
      
   # map luminosity to MIDI pitch (dark is low, bright is high pitch)
   chromaticPitch = mapValue(luminosity, 0, 255, 0, 128 * len(pitchSet) / 12)   # the brighter the pixel, the higher the note
      
   scaleDegree = chromaticPitch % len(pitchSet)  # find index into pitchSet list
   register    = chromaticPitch / len(pitchSet)  # find pitch register (e.g. 4th, 5th, etc.)
   
   # calculate the octave (register) and add the pitch displacement from the octave.
   diatonicPitch = register * 12 + pitchSet[scaleDegree]
      
   duration = mapValue(red, 0, 255, 0.1, 4.0)     # the reder the pixel, the longer the note
   dynamic = mapValue(blue, 0, 255, 0, 127)       # the bluer the pixel, the louder the note
   panoramic = mapValue(position, 0, maxPosition, 0.0, 1.0) # the closer to the top the pixel, the left-er the note
         
   # create this note
   note = Note(diatonicPitch, duration, dynamic, panoramic)   

   return note

##### create musical data

# sonify image pixels, does entire image in Diatonic
for col in range(width):  # col is time
   # in the current time, create concurrent notes
   for row in range(0, height, height / numNotesPerColumn):  # row is panoramic
   
      # we are scanning (sonifying) the image left-to-right, so 
      # use the col value as the time value (e.g., 1.0, 2.0, etc.)
      time = float(col)   # convert it to a float

      # use a Phrase as a wrapper to a note, so we can set the note's start time
      phrase = Phrase(time)   # start at current time (col)
      
      # get pixel at current coordinates (col and row)
      pixel = image.getPixel(col, row)

      # sonify this pixel
      note = sonifyPixelDiatonic(pixel, row, height, MAJOR_SCALE)
               
      # put note in this phrase (to establish a start time for this note)
      phrase.addNote(note)
         
      # add note wrapped in phrase to the part
      synthesizedPart.addPhrase(phrase)
         
    # now, all notes in this image column have been generated

#Part that creates a melody from the row halfway through and the specific col's 
row = (height/2)  #capture music from particular row
for col in range(85,99,1):   #captures music from particular col's

   
   # use a Phrase as a wrapper to a note, so we can set the note's start time
   phrase5 = Phrase()   # start at current time (col)
     
    # get pixel at current coordinates (col and row)
   pixel = image.getPixel(col, row)

    # sonify this pixel
   note = sonifyPixelDiatonic(pixel, 1.0, 1.0, [0, 4, 7])
   note.setRhythmValue(1.0)
   note.setDuration(3.0)
   
   
    # put note in this phrase (to establish a start time for this note)
   
   phrase5.addNote(note)
         
    # add note wrapped in phrase to the part
   synthesizedPart5.addPhrase(phrase5)

print synthesizedPart5

# Phrases Created:
# Phrase containing slower arpeggio
phrase2 = Phrase()
pitches2 = [C2, G2, E3, G2]
rhythms2 = [HN, HN, HN, HN]

# Phrase containing bassnote
phrase3 = Phrase()
bassnote = Note(C2, 42)

# Phrase containing faster arpeggio
phrase4 = Phrase()
pitches3 = [G3, C4, E4, C4,REST,REST,REST,REST,REST,REST,REST]
rhythms3 = [QN, QN, QN, QN,QN,  QN,  QN,  QN,  QN,  QN,  QN]

# Phrase containing same phrase2 arpeggio but repeated later
phrase6 = Phrase()
pitches4 = [C2, G2, E3, G3]
rhythms4 = [HN, HN, HN, HN]

# Phrases creating Note and StartTime
phrase3.addNote(bassnote)               # Basenote phrase
synthesizedPart3.addPhrase(phrase3)

phrase2.addNoteList(pitches2, rhythms2) # Slower arpeggio phrase
synthesizedPart2.addPhrase(phrase2)
phrase2.setStartTime(15)

phrase4.addNoteList(pitches3, rhythms3)
synthesizedPart4.addPhrase(phrase4)     # Faster arpeggio phrase
phrase4.setStartTime(23)

phrase6.addNoteList(pitches4, rhythms4) # Slower arpeggio but repeated later
synthesizedPart6.addPhrase(phrase6)
phrase6.setStartTime(60)

# Combine musical material
# All consolidation
Mod.consolidate(synthesizedPart5)
Mod.consolidate(synthesizedPart)
Mod.tiePitches(synthesizedPart5)
Mod.tiePitches(synthesizedPart)

#Create all Mod.repeats
Mod.repeat(phrase2,10)  #slower arpeggio
Mod.repeat(phrase3,8)   #bassnote
Mod.repeat(phrase4,16)  #faster arpeggio
Mod.repeat(phrase5,18)  #col and row section

#add all part to the the Score
synthesizedScore.addPart(synthesizedPart)
synthesizedScore.addPart(synthesizedPart2)
synthesizedScore.addPart(synthesizedPart3)
synthesizedScore.addPart(synthesizedPart4)
synthesizedScore.addPart(synthesizedPart5)
synthesizedScore.addPart(synthesizedPart6)

# Set tempo for full score
synthesizedScore.setTempo(60)

#view score and write it as a MIDI files
View.sketch(synthesizedScore)
Write.midi(synthesizedScore, "iceland2.mid")  # built-in MIDI instruments
Write.au(synthesizedScore, "iceland2.au") 

